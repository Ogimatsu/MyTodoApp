from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, SignUpView, AccountDeleteView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'), # ログイン
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), # ログアウト
    path('signup/', SignUpView.as_view(), name='signup'), # 新規登録
    path('account/delete', AccountDeleteView.as_view(), name='account_delete'), # アカウント削除
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'), # パスワード再発行フォーム
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'), # パスワード再発行メール送信完了
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'), # パスワード再設定
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'), # パスワード再設定完了
]