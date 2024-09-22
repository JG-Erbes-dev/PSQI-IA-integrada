from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from psqi.views import TestListView, NewTestView, TestDetailView
from accounts.views import register_view, login_view, logout_view
from .views import HomeView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', HomeView.as_view(), name='home'),    
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('test-list/', TestListView.as_view(), name='test_list'),
    path('new-test/', NewTestView.as_view(), name='new_test'),
    path('test/<int:pk>/', TestDetailView.as_view(), name='test_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
