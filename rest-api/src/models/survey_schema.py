from marshmallow import Schema, fields, validate

from models.question_schema import QuestionValidationSchema


class SurveyValidationSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    anonymous = fields.Bool(required=True)
    questions = fields.List(fields.Nested(lambda: QuestionValidationSchema()),
                            validate=validate.Length(1, 30))
