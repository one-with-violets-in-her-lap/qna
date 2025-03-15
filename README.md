![image](https://github.com/crucials/qna/assets/83793845/309e9de7-b4ef-4807-9a09-b2eb06157e89)

# qna

survey management website with responsive modern interface and advanced functionality like statistics and form builder

[:eye: view the app](https://qna.sorry.run/)

https://github.com/crucials/qna/assets/83793845/a7c2953e-50be-46e8-bc93-3e31b50c9f83

## main features

- survey analysis page with survey **activity chart**, responses stats and answers view
- survey creation through convenient **form builder**
- different types of questions to choose: short text, multi-line text, single choice
- convenient auth via **Google**
- product landing page

## tech info

### frontend

built with vue (nuxt), using **pinia** for global state and **github actions + cypress** for end-to-end testing. page visits chart made with chart.js

### backend

built as rest api with python and flask. most of the data are stored in **mongo db**, code formatted with flake8 and has unit tests made with pytest

using json web tokens for auth and **redis** for ip-based rate limiting

deployed with **docker**
