from django.urls import path
from Userapp.api.views import RegisterView, LoginView, LogoutView ,ForgotPasswordView, ResetPasswordView
#from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Registration
    path('auth/register/', RegisterView.as_view(), name='register'),
    # Login (JWT)
    path('auth/login/', LoginView.as_view(), name='login'),
    # Token Refresh
    #path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #Logout
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    #forget-password
    path('forgot-password/', ForgotPasswordView.as_view(), name="forgot-password"),
    #reset-password
    path('reset-password/<uidb64>/<token>/', ResetPasswordView.as_view(), name="reset-password"),
]




# from django.urls import path
# #from django.contrib.auth import views as auth_views
# from Userapp.api.views import RegisterView, LoginView, LogoutView
# from rest_framework_simplejwt.views import TokenRefreshView

# urlpatterns = [
#     # Registration
#     path('auth/register/', RegisterView.as_view(), name='register'),
#     # Login (JWT)
#     path('auth/login/', LoginView.as_view(), name='login'),
#     # Refresh Token
#     path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     # Logout
#     path('auth/logout/', LogoutView.as_view(), name='logout'),
    
    
#     # #reset
#     # path('auth/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
#     # path('auth/password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
#     # path('auth/password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
#     # path('auth/password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
# ]




