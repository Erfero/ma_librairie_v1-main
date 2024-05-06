from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    ## Route pour l'accueil
    path("", views.home, name="home"),

    ########## Route pour l'authentification ##########

    ## Route pour l'inscription
    path("signup/", views.signup_view, name="signup"),
    ## Route pour la connexion
    path("login/", views.login_view, name="login"),
    ## Route pour la deconnexion
    path("logout/", views.logout_view, name="logout"),

    ########## Route pour la réinitialisation du mot de passe ##########
    path("reset_password/", auth_views.PasswordResetView.as_view(template_name="Authentification/Password_reset_form.html"), name="reset_password"),
    path("reset_password_send/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset_password_complete", auth_views.PasswordResetCompleteView.as_view(), name="reset_password_complete"),

    ######### Route pour le changement du mot de passe #########
    path ('change-password/', views.change_password, name='change-password'),

    ######### Route pour le profil #########
    path('account/', views.user_account, name='account'),


    ######### Route pour l'édition du profil #########
    path('edit-profile/', views.edit_profile, name='edit_profile'),

]
