from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
path('upload/', views.upload_zip, name = 'upload'),
path('download/', views.download_zip, name = 'download'),
path('store_emails/', views.create_new_users, name = 'store_emails'),

path("", views.log_in, name="home"),
path('login', views.log_in, name="login"),
path('logout/', views.logout_view, name="logout"),
path('activate/<slug:uidb64>/<slug:token>', views.activate, name='activate'),
path("download/<int:id>/delete", views.delete_zip, name = "delete")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
