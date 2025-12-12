import allure
import pytest
import requests

from helpers import (
    headers_for_multipart,
    image_file,
    generate_valid_unique_email,
    generate_random_string,
)
from service import SIGNUP_URL, SIGNIN_URL, CREATE_LISTING_URL, edit_listing_url, delete_listing_url, IMG_PATH, IMG_FALLBACK_URL
from data import pancakes_data, pancakes_data_edit, img_path, ANNOUNCEMENT_DELETED_MESSAGE


@allure.epic("Объявления")
@allure.feature("Объявления")
class TestAnnouncement:


    @allure.title("Создание объявления")
    def test_create_announcement(self, signup_signin_user):

        headers = headers_for_multipart(signup_signin_user)
        files = image_file(img_path, fallback_url=IMG_FALLBACK_URL)

        with allure.step("Создаем объявление"):
            ann_response = requests.post(CREATE_LISTING_URL, data=pancakes_data, headers=headers, files=files)

        assert ann_response.status_code == 201
        body = ann_response.json()
        assert body.get("name") == pancakes_data["name"]

    @allure.title("Редактирование объявления")
    def test_edit_announcement(self, get_id_create_announcement, signup_signin_user):
        headers = {k: v for k, v in signup_signin_user.items() if k.lower() != "content-type"}

        response = requests.patch(edit_listing_url(get_id_create_announcement),
                                  data=pancakes_data_edit,
                                  headers=headers)
        
        assert response.status_code == 200
        body = response.json()
        assert body.get("name") == pancakes_data_edit["name"]
        assert body.get("id") == get_id_create_announcement

    @allure.title("Удаление объявления")
    def test_delete_announcement(self, get_id_create_announcement, signup_signin_user):
        headers = {k: v for k, v in signup_signin_user.items() if k.lower() != "content-type"}

        response = requests.delete(delete_listing_url(get_id_create_announcement), headers=headers)

        assert response.status_code == 200
        body = response.json()
        assert body.get("message") == ANNOUNCEMENT_DELETED_MESSAGE

    @allure.title("Редактирование чужого объявления запрещено")
    def test_edit_foreign_announcement(self, get_id_create_announcement, signup_signin_user):
        ann_id = get_id_create_announcement

        email2 = generate_valid_unique_email("yandexpr.ru")
        password2 = generate_random_string(10)
        name2 = "Stranger"
        requests.post(SIGNUP_URL, json={"email": email2, "password": password2, "name": name2})

        signin_response = requests.post(SIGNIN_URL, json={"email": email2, "password": password2})
        token2 = signin_response.json().get("token", {}).get("access_token")
        stranger_headers = {"Authorization": f"Bearer {token2}", "Accept": "application/json"}
        stranger_headers = {k: v for k, v in stranger_headers.items() if k.lower() != "content-type"}

        patch_data = {"name": "Блинчики (ред.)", "price": "999"}
        with allure.step("Чужой пользователь пытается редактировать"):
            resp_forbidden = requests.patch(
                edit_listing_url(ann_id),
                data=patch_data, 
                headers=stranger_headers,
                timeout=30
            )
        assert resp_forbidden.status_code == 401
        body = resp_forbidden.json()
        assert body is not None
