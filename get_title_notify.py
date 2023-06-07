import requests
from bs4 import BeautifulSoup
import re

def get_title():
    url = 'https://muepoint.jp/kmr/wmmt/5title.html'

    response = requests.get(url, headers={"Content-Type": "text/html; charset=Shift_JIS"})
    html_text = response.content.decode("Shift_JIS")

    # HTML全体を取得
    # 正規表現で指定された部分を抜き出す
    pattern = r'<br>\n<br>\n(.*?)\n<font color="#666666">？</font>'
    result = re.findall(pattern, html_text, re.DOTALL)

    html_text = result[0]
    # 不必要な部分を正規表現で削除
    html_text = re.sub(r'<.*?>', '', html_text)
    html_text = re.sub(r'※.*\n', '', html_text)

    # 結果を表示
    return html_text

def main(request):
    token = "my-token" # LINE Notifyから取得したトークンを入力してください
    endpoint = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": "Bearer " + token}
    params = {"message": get_title()}
    requests.post(endpoint, headers=headers, data=params)