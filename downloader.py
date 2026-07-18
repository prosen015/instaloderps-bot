import requests

API_URL = "https://co.wuk.sh/api/json"

def download_instagram(url):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "url": url
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return None

    data = response.json()

    if data.get("status") != "success":
        return None

    download_url = data.get("url")

    file = requests.get(download_url)

    filename = "instagram_download.mp4"

    with open(filename, "wb") as f:
        f.write(file.content)

    return filename
