from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('login/', views.log_in, name="login"),
    path('activate/<slug:uidb64>/<slug:token>', views.activate, name='activate'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)