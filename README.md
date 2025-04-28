# 📋 タスク管理アプリ（Django）

Django フレームワークを使って作成した、タスク管理アプリケーションです。
タスクを設定して管理・編集する機能はもちろん、
緊急度・重要度も設定できるため、タスクの優先順位も設定できます。
また、目標及び実績を設定し、進捗率を管理できるため、
タスクの進捗状況を視覚的に確認可能です。

---

## 🚀 使用技術

- Python 3.x
- Django 4.x
- HTML（テンプレート）
- Bootstrap（スタイル調整、※CDN 利用）
- SQLite（開発用 DB）

---

## 🧩 主な機能

- タスクの一覧表示（トップページ）
- タスクの新規登録（フォーム）
- タスクの編集・更新
- タスクの削除（モーダルより確認あり）
- 完了ステータスの設定
- 緊急度・重要度の設定
- 目標・実績の設定（任意）
- 進捗率の自動計算（目標・実績がともに設定されている場合）
- 更新日時／作成日時／締切日時（任意）／完了日時（タスク完了時）表示
- タスク完了ボタンによる状態切り替え（進捗率・完了日時の自動補完）
- 未入力・未設定項目へのデフォルト表示（例：「-」で表示）

---

## 🌐 URL 構成

- `/` - タスク一覧（トップページ）
- `/create/` - タスク新規作成
- `/<task_id>/update/` - タスク編集
- `/<task_id>/delete/` - タスク削除
- `/<task_id>/complete/` - タスクを完了にする
- `/<task_id>/uncomplete/` - タスクの完了状態を取り消す

---

## 📁 ディレクトリ構成（抜粋）

```
プロジェクトルート/
├── config/                  # プロジェクト設定
│   ├── settings.py          # 設定ファイル
│   ├── urls.py              # プロジェクトURL設定
│   └── ...
├── static/                  # CSS/JS
│   └── style.css            # CSSファイル
├── templates/
│   └── base.html            # アプリ表示のテンプレート
├── todos/                   # アプリ本体
│   ├── models.py            # モデル（Todo定義）
│   ├── views.py             # ビュー関数
│   ├── forms.py             # フォーム
│   ├── urls.py              # URLルーティング
│   └── templates/
│       └── todos/
│           ├── index.html   # 一覧表示
│           ├── create.html  # 新規作成
│           └── update.html  # 編集
├── manage.py                # 管理スクリプト
└── requirements.txt         # 依存パッケージ
```

---

## ⚙️ セットアップ手順（ローカル開発環境）

```bash
# リポジトリのクローン
git clone https://github.com/Ogimatsu/MyTodoApp
cd MyTodoApp

# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化（OS別）
# Mac/Linuxの場合
source venv/bin/activate

# Windowsの場合
venv\Scripts\activate

# 必要パッケージのインストール
pip install -r requirements.txt

# マイグレーション実行
python manage.py migrate

# サーバー起動
python manage.py runserver
```

---

## 🔍 使い方

1. トップページにアクセスして、タスク一覧を確認
2. 「新規作成」ボタンからタスクを追加
3. 各タスクの「編集」リンクからタスクを更新
4. 各タスクの「削除」ボタンを押すとモーダルが表示されるので、
   モーダルの「削除」ボタンを押すとタスクを削除可能
5. タスクの完了・取消は、それぞれのボタンでワンタッチ操作が可能

---

## 📷 画面キャプチャ

### 1．タスクの一覧表示画面

![一覧表示画面](static/index.png)

### 2．タスクの新規登録画面

![新規登録画面](static/create.png)

### 3．タスクの編集画面

![編集画面](static/update.png)

---

## 👨‍💻 開発者向け情報

- テストの実行: `python manage.py test`
- コードスタイル: PEP 8 に準拠
- 開発環境: `.editorconfig`ファイルを参照
- 管理画面の利用（オプション）:
  - 管理ユーザーの作成: `python manage.py createsuperuser`
  - 管理画面アクセス: http://127.0.0.1:8000/admin/
  - ※ `Todo` モデルを `admin.py` に登録しておくと、GUI でデータ確認・編集も可能です
