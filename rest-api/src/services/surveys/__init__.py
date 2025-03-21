from bson import ObjectId
from pymongo import ReturnDocument

from errors.resource_not_found_error import ResourceNotFoundError
from models.account_dto import Account
from mongo_database import (
    accounts_collection,
    questions_collection,
    responses_collection,
    survey_stats_collection,
)
from services.surveys.stats import survey_stats_service
from utils.find_item import find_item


class InvalidResponseDataError(Exception):
    pass


class SurveysService:
    def create_survey(self, account_id: ObjectId, survey):
        questions = survey.pop("questions")
        survey["_id"] = ObjectId()

        for question in questions:
            question["survey_id"] = survey["_id"]

        questions_collection.insert_many(questions)

        survey_stats_service.create_initial_survey_stats(survey["_id"], survey["title"])

        return accounts_collection.find_one_and_update(
            {"_id": account_id},
            {"$push": {"surveys": survey}},
            return_document=ReturnDocument.AFTER,
        )

    def get_survey_with_questions(self, survey_id: str):
        if not ObjectId.is_valid(survey_id):
            return None

        account_with_requested_survey = accounts_collection.find_one(
            {"surveys._id": ObjectId(survey_id)}, {"surveys.$": 1}
        )

        if account_with_requested_survey is None:
            return None

        survey = account_with_requested_survey["surveys"][0]

        survey["questions"] = list(
            questions_collection.find({"survey_id": survey["_id"]})
        )

        return survey

    def delete_survey(self, survey_id: str):
        if not ObjectId.is_valid(survey_id):
            raise ResourceNotFoundError()

        survey_object_id = ObjectId(survey_id)
        print(survey_object_id)

        account_update_result = accounts_collection.update_many(
            {}, {"$pull": {"surveys": {"_id": survey_object_id}}}
        )

        if account_update_result == 0:
            raise ResourceNotFoundError()

        self.delete_data_related_to_surveys([survey_object_id])

    def delete_data_related_to_surveys(self, surveys_ids: list[ObjectId]):
        questions_collection.delete_many({"survey_id": {"$in": surveys_ids}})

        responses_collection.delete_many({"survey_id": {"$in": surveys_ids}})

        survey_stats_collection.delete_many({"survey_id": {"$in": surveys_ids}})

    def is_survey_owner(self, account: Account, survey_id: str):
        found_survey_on_account = find_item(
            account["surveys"], lambda survey: survey["_id"] == ObjectId(survey_id)
        )

        if found_survey_on_account is None:
            return False
        else:
            return True


surveys_service = SurveysService()
