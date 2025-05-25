from django.contrib.auth.password_validation import MinimumLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class CustomMinimumLengthValidator(MinimumLengthValidator):
    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("このパスワードは短すぎます。最低でも %(min_length)d 文字以上で入力してください。"),
                code='password_too_short',
                params={'min_length': self.min_length},
            )
