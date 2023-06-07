import requests
from lxml import html
from datetime import datetime
from google.cloud import storage
import pytz

def frame_get(month, day):
    # 日付の調整（12日の画像を取得したければ、13とxpathに設定する必要があるため）
    day = day + 1

    # スクレイピング対象のURL
    url = "https://wikiwiki.jp/wmmt/%E3%83%93%E3%83%B3%E3%82%B4%E3%83%81%E3%83%A3%E3%83%AC%E3%83%B3%E3%82%B8#l8d69939"
    # スクレイピング対象のXPATH
    frame_xpath = "/html/body/div[2]/div[3]/div[1]/div/div[4]/div[16]/div[2]/div[{}]/div[2]/div/table/tbody/tr[{}]/td[3]/a/img/@src".format(month, day)
    # HTTPリクエストを送信してHTMLを取得
    response = requests.get(url)
    tree = html.fromstring(response.content)

    # 画像のURLを取得
    image_link = tree.xpath(frame_xpath)[0]

    # 画像をダウンロード
    image_data = requests.get(image_link).content

    return image_data

def main(request):
    # 日本のタイムゾーンを取得
    jst = pytz.timezone('Asia/Tokyo')

    # 現在の日時を取得
    now = datetime.now(jst)

    # 月と日を取得
    month = now.month
    day = now.day
    
    # 画像データを取得
    image_data = frame_get(month, day)

    # 保存先のバケット名とファイル名を指定
    bucket_name = "wangan_frame_image"
    file_name = "image.jpg"

    # Google Cloud Storageクライアントの初期化
    client = storage.Client()

    # バケットの取得
    bucket = client.get_bucket(bucket_name)

    # ファイルの保存
    blob = bucket.blob(file_name)
    blob.upload_from_string(image_data, content_type="image/jpeg")

    return "Image uploaded successfully."