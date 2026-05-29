from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView


class StaticPageView(TemplateView):
    """Базовый класс для статичных страниц."""


class AboutPageView(StaticPageView):
    template_name = 'pages/about.html'


class RulesPageView(StaticPageView):
    template_name = 'pages/rules.html'


def csrf_failure(request, reason=""):
    """Обработчик ошибки CSRF."""
    return render(request, 'pages/403csrf.html', status=403)


def page_not_found(request, exception):
    """Обработчик ошибки 404."""
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    """Обработчик ошибки 500."""
    return render(request, 'pages/500.html', status=500)


def registration(request):
    """Страница регистрации."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration_form.html', {
        'form': form,
    })


@login_required
def edit_profile(request, username):
    """Редактирование профиля пользователя."""
    User = get_user_model()
    profile_user = get_object_or_404(User, username=username)

    if request.user != profile_user:
        raise PermissionDenied

    class ProfileEditForm(UserChangeForm):
        class Meta:
            model = User
            fields = ('username', 'first_name', 'last_name', 'email')

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=profile_user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', username=profile_user.username)
    else:
        form = ProfileEditForm(instance=profile_user)

    return render(request, 'blog/user.html', {
        'form': form,
    })
