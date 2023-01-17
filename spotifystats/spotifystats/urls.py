from django.contrib import admin
from django.urls import path
from spotifystatsapp.views import WelcomePage, AuthURL, Congrats

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get-auth-url/', AuthURL.as_view(), name='getauth'),
    path('', WelcomePage.as_view(), name='welcomepage'),
    path('congrats', Congrats.as_view()),
]
