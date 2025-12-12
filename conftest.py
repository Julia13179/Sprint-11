import allure
import pytest
import requests


from helpers import (
    headers_for_multipart,
    image_file,
    generate_valid_unique_email,
    generate_random_string,
    build_user_payload,
)
from service import SIGNUP_URL, SIGNIN_URL, CREATE_LISTING_URL, IMG_FALLBACK_URL
from data import img_path as IMG_PATH, pancakes_data


    
@pytest.fixture
def unique_valid_email():
    return generate_valid_unique_email()

@pytest.fixture
def user_data(unique_valid_email):
    email = unique_valid_email
    password = generate_random_string(10)
    submitPassword = password
    payload = build_user_payload(email, password, submitPassword)
    return payload

@pytest.fixture
def signup_signin_user(user_data):
    requests.post(SIGNUP_URL, json=user_data)

    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    signin_response = requests.post(SIGNIN_URL, json=login_data)
    body = signin_response.json()

    token = body.get("token", {}).get("access_token")
    if not token:
        raise ValueError("Token not received during signin")
    return { 
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
@pytest.fixture
def get_id_create_announcement(signup_signin_user):
        headers = headers_for_multipart(signup_signin_user)
        files = image_file(IMG_PATH, fallback_url=IMG_FALLBACK_URL)

        with allure.step("Создаем объявление"):
            ann_response = requests.post(CREATE_LISTING_URL, data=pancakes_data, headers=headers, files=files)

        if ann_response.status_code != 201:
            raise ValueError(f"Failed to create announcement: {ann_response.status_code}")
        return ann_response.json()["id"]
