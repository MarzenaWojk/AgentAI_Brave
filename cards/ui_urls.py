from django.urls import path

from .ui_views import dashboard_page, home_page, login_page, logout_page, register_page


urlpatterns = [
	path("", home_page, name="home"),
	path("register/", register_page, name="register"),
	path("login/", login_page, name="login"),
	path("logout/", logout_page, name="logout"),
	path("dashboard/", dashboard_page, name="dashboard"),
]
