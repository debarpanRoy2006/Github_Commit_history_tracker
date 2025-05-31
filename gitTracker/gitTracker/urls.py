from django.contrib import admin
from django.urls import path
from tracker import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_commits/', views.get_commits, name='get_commits'),
    path('api/commits/', views.get_commits_api, name='get_commits_api'),  # ✅ NEW API endpoint
    path('admin/', admin.site.urls),
]
