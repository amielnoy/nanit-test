# Testing MOBILE UI using mocked mobile session and mocked streaming server

# Testing API's on Mocked streaming server on http://127.0.0.1:8082 

## See .env for urls

## Instalation(for mac):

1. Install Python 3.12
2. install pip
3. python3 -m venv .venv
4. source .venv/bin/activate
5. pip install -r requirements.txt
6. brew install allure(for mac only)
7. run chmod +x /run_tests_and_report_allure.sh

## Run Tests and report Allure report:
./run_tests_and_report_allure.sh


The framework supports:

1)retries on failed api calls
2)Allure reporting
3)Friendly for ci by pytest.ini & .env
4)BaseSession abstract class to share functionality on mobile and api sessions

## .env & login_users.json were added
to repository although not recommended to do so.
It is recommended to use a .gitignore file to exclude it from version control. 

But only for test purposes, i included them for ease of use