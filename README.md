# 📋 ToDoアプリ（Django）

Djangoフレームワークを使って作成した、シンプルなToDo管理アプリケーションです。
タスクの登録・編集・削除が可能で、基本的なCRUD操作を学びながら実装しています。

---

## 🚀 使用技術

- Python 3.x
- Django 4.x
- HTML（テンプレート）
- Bootstrap（スタイル調整、※CDN利用）
- SQLite（開発用DB）

---

## 🧩 主な機能

- タスクの一覧表示（トップページ）
- タスクの新規登録（フォーム）
- タスクの編集・更新
- タスクの削除（確認あり）
- 完了フラグの設定
- 登録日／完了日表示（任意）

---

## 🌐 URL構成

- `/` - タスク一覧（トップページ）
- `/create/` - タスク新規作成
- `/<task_id>/update/` - タスク編集
- `/<task_id>/delete/` - タスク削除

---

## 📁 ディレクトリ構成（抜粋）
```
プロジェクトルート/
├── config/                  # プロジェクト設定
│   ├── settings.py          # 設定ファイル
│   ├── urls.py              # プロジェクトURL設定
│   └── ...
├── todos/                   # アプリ本体
│   ├── models.py            # モデル（Todo定義）
│   ├── views.py             # ビュー関数
│   ├── forms.py             # フォーム
│   ├── urls.py              # URLルーティング
│   └── templates/
│       └── todos/
│           ├── index.html   # 一覧表示
│           ├── create.html  # 新規作成
│           ├── update.html  # 編集
│           └── delete.html  # 削除確認
├── static/                  # CSS/JS
├── manage.py                # 管理スクリプト
└── requirements.txt         # 依存パッケージ
```

---

## ⚙️ セットアップ手順（ローカル開発環境）

```bash
# リポジトリのクローン
git clone https://github.com/Ogimatsu/MyTodoApp
cd MyTodoApp

# 仮想環境の作成と有効化
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate

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
4. 各タスクの「削除」リンクからタスクを削除

---

## 👨‍💻 開発者向け情報

- テストの実行: `python manage.py test`
- コードスタイル: PEP 8に準拠
- 開発環境: `.editorconfig`ファイルを参照