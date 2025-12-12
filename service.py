from pathlib import Path


BASE_URL = 'https://qa-desk.stand.praktikum-services.ru'
API_URL = f'{BASE_URL.rstrip("/")}/api'

SIGNUP_URL = f'{API_URL}/signup'
SIGNIN_URL = f'{API_URL}/signin'
CREATE_LISTING_URL = f'{API_URL}/create-listing'


def edit_listing_url(listing_id):
    return f'{API_URL}/update-offer/{listing_id}'


def delete_listing_url(listing_id):
    return f'{API_URL}/listings/{listing_id}'


ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
IMG_PATH = ASSETS_DIR / "pancakes.jpg"
IMG_FALLBACK_URL = "https://qa-foodgram.s3.yandex.net/pancakes.jpg"
