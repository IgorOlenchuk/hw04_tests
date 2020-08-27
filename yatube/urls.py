from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path


urlpatterns = [
    # регистрация и авторизация
    path('auth/', include('Users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    # flatpages
    path('about/', include('django.contrib.flatpages.urls')),
    # импорт из приложения posts
    path('', include('posts.urls')),
    # раздел администратора
    path('admin/', admin.site.urls),
]

#добавим новые пути
urlpatterns += [
        path('about-us/', views.flatpage, {'url': '/about-us/'}, name='about'),
        path('terms/', views.flatpage, {'url': '/terms/'}, name='terms'),
        path('about-author/', views.flatpage, {'url': '/about-author/'}, name='about-author'),
        path('about-spec/', views.flatpage, {'url': '/about-spec/'}, name='about-spec'),
]
