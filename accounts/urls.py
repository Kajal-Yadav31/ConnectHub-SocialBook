from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('reset_password_validate/<uidb64>/<token>/',
         views.reset_password_validate, name='reset_password_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('my-profile/', views.my_profile, name='my-profile'),
    path("profile/<username>/", views.friend_profile, name="profile"),

    # path("profile-update/", views.profile_update, name="profile-update"),

]
