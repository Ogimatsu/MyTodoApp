from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from .forms import CustomUserCreationForm, MypageUpdateForm
from utils.message_helper import add_message, ICON_MAP

# ログイン時の処理
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('todos:index')

    def form_valid(self, form):
        # ログイン成功時にメッセージを表示。
        add_message(self.request, 'MSG_1202')
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if 'account_deleted' in request.GET:
            # アカウント削除時にメッセージを表示。
            add_message(request, 'MSG_1206')
        return super().get(request, *args, **kwargs)

# ユーザー登録時の処理
class SignUpView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        self.object = form.save()
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

    def get_success_url(self):
        # ユーザー登録成功時にメッセージを表示。併せてログインも済ませる。
        add_message(self.request, 'MSG_1201')
        return reverse('todos:index')

# ログアウト時の処理
class CustomLogoutView(LogoutView):
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        add_message(request, 'MSG_1203')
        return super().dispatch(request, *args, **kwargs)

# アカウント削除時の処理
class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    def get_success_url(self):
        # アカウント削除後にメッセージを表示するため、クエリパラメータを付与する。
        return str(reverse_lazy('login')) + '?account_deleted=1'

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        # ユーザーアカウントを削除する前に、明示的にログアウト処理を行う
        logout(request)
        return super().delete(request, *args, **kwargs)

# マイページの処理
class Mypage(LoginRequiredMixin, TemplateView):
    template_name = 'registration/mypage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MypageUpdateForm(instance=self.request.user) # type: ignore # VS Code用、実害なし
        return context

# マイページ編集の処理
class MypageUpdate(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'registration/mypage_update.html'
    form_class = MypageUpdateForm
    success_url = reverse_lazy('mypage')
    def form_valid(self, form):
        add_message(self.request, 'MSG_1204')
        return super().form_valid(form)

    def get_object(self):
        return self.request.user

# パスワード変更の処理
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change.html'
    success_url = reverse_lazy('mypage')

    def form_valid(self, form):
        add_message(self.request, 'MSG_1205')
        return super().form_valid(form)
