from django.urls import path
# from authentication.views import *
from django.contrib.auth import views as auth_views
from .views import *
urlpatterns = [
    path('', home,name="homepage"),
    path('staff/<str:uname>', staffFunction,name="staff"),
    path('printform/<str:uname>', printUserForm,name="print-form"),
    path('register/', RegisterPage,name="register"),
    path('login/', LoginPage,name="login"),
    path('logout/', Logout,name="logout"),
    path('baseview/', baseview,name="baseview"),
    path('eventviewer/', events,name="Events"),
    path('notauthorized/', nonauthorizedview,name="notauthorized"),
    path(r'set-new-password/<uidb64>/<token>',PasswordReset.as_view(),name='new-password'),
    path(r'passwordreset',RequestPasswordResetEmail.as_view(),name="password-reset"),
    path(r'setup-users',SetupUsers.as_view(),name="setup-users"),
    path(r'switch',switchUserType,name="switch"),
    path(r'randomizer',randomizer,name="randomizer"),


]