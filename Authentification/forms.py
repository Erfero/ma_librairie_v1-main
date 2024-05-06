############### Ce fichier contient les classes de formulaire pour l'authentification ###############
from django import forms
from django.contrib.auth.models import User


# classe de formulaire pour la connexion
class LoginForm(forms.Form):
    # Champ pour le nom d'utilisateur
    username = forms.CharField(max_length=100)
    # Champ pour le mot de passe
    password = forms.CharField(widget=forms.PasswordInput)

# classe de formulaire pour l'inscription


class UserRegistrationForm(forms.ModelForm):
    ## Champ pour le mot de passe
    password1 = forms.CharField(
        label='Mot de passe', widget=forms.PasswordInput)
    ## Champ pour la confirmation du mot de passe
    password2 = forms.CharField(
        label='Confirmer le mot de passe', widget=forms.PasswordInput)

    class Meta:
        ## Reutilisation de l'utilisateur
        model = User
        # Champs de l'utilisateur
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    ## Vérification du mot de passe
    def clean_password2(self):
        ## Récupération des mots de pass
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        ## Vérification des mots de passe
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "Les mots de passe ne sont pas identiques")
        return password2
