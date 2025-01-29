from django.urls import path

from . import views

urlpatterns = [
    path("<pk>/toggle-flag", views.ToggleFlagApiView.as_view(), name="toggle-flag"),
    path("<pk>/click", views.ClickApiView.as_view(), name="click"),
    path("<pk>", views.GameApiView.as_view(), name="game"),
    path("", views.GameListApiView.as_view()),
]
