from django.urls import path
from .admin_api_views import (
    CreateRoleView,
    CreateElementView,
    SetPermissionView,
    AssignRoleView
)
from accounts.views import RegisterView, LoginView, TestView, OrdersView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('test/', TestView.as_view()),
    path('orders/', OrdersView.as_view()),
    path('logout/', LogoutView.as_view()),

    path('admin/create-role/', CreateRoleView.as_view()),
    path('admin/create-element/', CreateElementView.as_view()),
    path('admin/set-permission/', SetPermissionView.as_view()),
    path('admin/assign-role/', AssignRoleView.as_view()),
]