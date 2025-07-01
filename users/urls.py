from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .views import CustomLoginView, SignUpView, AccountDeleteView, Mypage, MypageUpdate, CustomPasswordChangeView, CustomLogoutView
from .forms import PasswordResetCaptchaForm

urlpatterns = [
    # ログイン
    path('login/', CustomLoginView.as_view(), name='login'),
    # ログアウト
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    # 新規登録
    path('signup/', SignUpView.as_view(), name='signup'),
    # パスワード再発行フォーム
    path('password_reset/', auth_views.PasswordResetView.as_view(
        form_class=PasswordResetCaptchaForm,
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.txt',
        success_url=reverse_lazy('password_reset_done'),
    ), name='password_reset'),
    # パスワード再発行メール送信完了
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # パスワード再設定
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # パスワード再設定完了
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # マイページ
    path('mypage/', Mypage.as_view(), name='mypage'),
    # マイページ編集
    path('mypage/update/', MypageUpdate.as_view(), name='mypage_update'),
    # パスワード変更
    path('mypage/password_change/', CustomPasswordChangeView.as_view(), name='mypage_password_change'),
    # アカウント削除
    path('mypage/delete/', AccountDeleteView.as_view(), name='mypage_account_delete'),
]