from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from .views import CustomLoginView, SignUpView, AccountDeleteView, Mypage, MypageUpdate, CustomPasswordChangeView, CustomLogoutView

urlpatterns = [
    path('', RedirectView.as_view(url='/login/')),
    path('login/', CustomLoginView.as_view(), name='login'), # ログイン
    path('logout/', CustomLogoutView.as_view(), name='logout'), # ログアウト
    path('signup/', SignUpView.as_view(), name='signup'), # 新規登録
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'), # パスワード再発行フォーム
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'), # パスワード再発行メール送信完了
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'), # パスワード再設定
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'), # パスワード再設定完了
    path('mypage/', Mypage.as_view(), name='mypage'), # マイページ
    path('mypage/update/', MypageUpdate.as_view(), name='mypage_update'), # マイページ編集
    path('mypage/password_change/', CustomPasswordChangeView.as_view(), name='mypage_password_change'), # パスワード変更
    path('mypage/delete/', AccountDeleteView.as_view(), name='mypage_account_delete'), # アカウント削除
]