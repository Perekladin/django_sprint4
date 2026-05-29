from django.contrib import admin
from django.urls import include, path
from pages import views as pages_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/registration/', pages_views.registration, name='registration'),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'profile/<str:username>/edit/',
        pages_views.edit_profile,
        name='edit_profile',
    ),
    path('', include('blog.urls')),
    path('pages/', include('pages.urls')),
]

# Обработчики ошибок
handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'
handler403 = 'pages.views.csrf_failure'
