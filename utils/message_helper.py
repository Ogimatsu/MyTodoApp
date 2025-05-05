from django.contrib import messages
from .messages_def import MESSAGES

ICON_MAP = {
    "success": "<i class='bi bi-check-circle-fill'></i> ",
    "danger": "<i class='bi bi-x-circle-fill'></i> ",
    "info": "<i class='bi bi-info-circle-fill'></i> ",
    "warning": "<i class='bi bi-exclamation-triangle-fill'></i> ",
}

def add_message(request, code, **kwargs):
    if code in MESSAGES:
        # メッセージ、状態、アイコンの情報を取得
        msg = MESSAGES[code]['text']
        level = MESSAGES[code]['level']
        icon = ICON_MAP.get(level, '')
        # メッセージ内部の、変数となっている箇所を埋める
        text = msg.format(**kwargs)
        full_message = icon + text
        getattr(messages, level)(request, full_message)
    else:
        messages.error(request, f"未定義のメッセージコード: {code}")