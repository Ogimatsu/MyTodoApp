from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from .forms import CustomUserCreationForm, MypageUpdateForm

# ログイン時の処理
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('todos:index')

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
            return reverse('todos:index')

# アカウント削除時の処理
class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('login')

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return super().delete(request, *args, **kwargs)

# マイページの処理
class Mypage(LoginRequiredMixin, TemplateView):
    template_name = 'registration/mypage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MypageUpdateForm(instance=self.request.user) # type: ignore
        return context

# マイページ編集の処理
class MypageUpdate(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'registration/mypage_update.html'
    form_class = MypageUpdateForm
    success_url = reverse_lazy('mypage')

    def get_object(self):
        return self.request.user

# パスワード変更の処理
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change.html'
    success_url = reverse_lazy('mypage')