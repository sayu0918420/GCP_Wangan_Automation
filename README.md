# GCPでアーケードゲーム（湾岸ミッドナイト6RR）の情報を取得する

## 取得する情報
- その日に取得することのできるアイテム・称号

## 通知方法
- LINE Notify

## 実行環境
- GCP

## GCPを採用した理由
- GCP学習のため

## GCP内で利用する機能
- Google Cloud Functions
- Google Cloud Storage
- Google Cloud Sheduler

## 実行環境（ランタイム）
Python3.9

## GCPでの設定について
### Cloud Functionsの設定
- GitHub上にアップロードされている.pyファイルの関数を、Cloud Functionsに設置します
- requirements.txtは、Git Hub上にアップロードされているものを設定してください
- エントリポイントはすべてmain
- main関数の引数に設定されているrequestは、Cloud Functionsの仕様上必要になるものです
    - ローカル環境でテストする場合、main関数の引数を空にしてから実行してください
- バケット名・トークンIDなど、書き換えるべき場所は書き換えてください


## 各関数についての説明
### frame_image_get.py
- その日ゲットできるアイテムの画像を取得して、その画像をCloud Storageに保存します

### frame_image_notify.py
- Cloud Storageに保存した画像と、そのアイテム名をLINE Notifyで通知します

### get_title_notify.py
- その日ゲットできる称号をLINE Notifyで通知します

