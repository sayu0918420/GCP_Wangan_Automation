import requests
from google.cloud import storage
from datetime import datetime
from lxml import html
import time
import pytz

def get_image_from_storage(bucket_name, file_name):
    # Google Cloud Storageクライアントの初期化
    client = storage.Client()

    # バケットの取得
    bucket = client.get_bucket(bucket_name)

    # ファイルの取得
    blob = bucket.blob(file_name)

    # ファイルのダウンロード
    image_data = blob.download_as_bytes()

    return image_data

def send_line_notify(token, message, image_data=None):
    # Line Notify APIのエンドポイント
    line_notify_api = "https://notify-api.line.me/api/notify"

    # ヘッダーにトークンを指定
    headers = {"Authorization": "Bearer " + token}

    # ペイロードにメッセージを指定
    payload = {"message": message}

    # 画像データがある場合はファイルとして添付
    if image_data:
        files = {"imageFile": image_data}
        response = requests.post(line_notify_api, headers=headers, data=payload, files=files)
    else:
        response = requests.post(line_notify_api, headers=headers, data=payload)

    return response

def frame_name_get(month,day):
    # 日付の調整（12日の画像を取得したければ、14とxpathに設定する必要があるため）
    day = day+1

    # スクレイピング対象のURL
    url = "https://wikiwiki.jp/wmmt/%E3%83%93%E3%83%B3%E3%82%B4%E3%83%81%E3%83%A3%E3%83%AC%E3%83%B3%E3%82%B8#l8d69939"

    # HTTPリクエストを送信してHTMLを取得
    response = requests.get(url)
    tree = html.fromstring(response.content)

    # 入手できるネームフレームの名前取得
    frame_name_xpath = "/html/body/div[2]/div[3]/div[1]/div/div[4]/div[16]/div[2]/div[{}]/div[2]/div/table/tbody/tr[{}]/td[2]".format(month,day)
    frame_name = tree.xpath(frame_name_xpath)[0].text

    return frame_name

def main(request):
    # 日本のタイムゾーンを取得
    jst = pytz.timezone('Asia/Tokyo')

    # 現在の日時を取得
    now = datetime.now(jst)

    # 月と日を取得
    month = now.month
    day = now.day

    # 保存された画像を取得
    bucket_name = "wangan_frame_image"
    file_name = "image.jpg"
    image_data = get_image_from_storage(bucket_name, file_name)

    # Line Notifyに送信
    line_notify_token = "my-token" # LINE Notifyから取得したトークンを入力してください
    message = "本日のネームプレートは「{}」です。".format(frame_name_get(month,day))
    time.sleep(10)
    response = send_line_notify(line_notify_token, message, image_data)

    return "Line Notify sent successfully."