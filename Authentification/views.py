from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserRegistrationForm
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout
from django.contrib.auth.models import User
import re
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from Catalogue.models import *
from Contacts.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.



# Méthode pour l'affichage de la page d'accueil pour tout utilisateur


def home(request, page=1):
    # Les livres par date de parution
    liste_books = Book.objects.order_by('-published_date')
    
    # Les livres par recommendation
    liste_books_recommender = Book.objects.order_by('-recommended_number')
    

    # Paginer la liste d'objets
    paginator = Paginator(liste_books, 8)  # 10 éléments par page
    paginator_recommender = Paginator(liste_books_recommender, 3)  # 10 éléments par page
    page = request.GET.get('page')

    try:
        liste_books = paginator.page(page)
        liste_books_recommender = paginator_recommender.page(page)
    except PageNotAnInteger:
        # Si la page n'est pas un entier, afficher la première page
        liste_books = paginator.page(1)
        liste_books_recommender = paginator_recommender.page(1)
    except EmptyPage:
        # Si la page est hors de portée (par exemple, page 9999), afficher la dernière page
        liste_books = paginator.page(paginator.num_pages)
        liste_books_recommender = paginator_recommender.page(paginator_recommender.num_pages)

    # Passer la liste paginée au contexte
    contexte = {
        'liste_books': liste_books,
        'liste_books_recommender': liste_books_recommender,
        }
    # Redirection vers la page d'accueil
    return render(request, 'accueil.html', contexte)


# Méthode pour l'inscription
def signup(request):
    # Vérification de la methode POST
    # Si la methode est POST
    if request.method == 'POST':
        # Creation du formulaire d'inscription avec les informations de la requête
        signup_form = UserRegistrationForm(request.POST)
        # Vérification de la validité du formulaire
        # Si le formulaire est valide
        if signup_form.is_valid():
            # Créer un nouvel utilisateur
            new_user = signup_form.save(commit=False)
            new_user.set_password(signup_form.cleaned_data['password1'])
            # Enregistrer l'utilisateur
            new_user.save()
            # Redirection vers la page du tableau de bord
            return redirect('login')
    # Si la methode n'est pas POST
    else:
        # Creation du formulaire d'inscription
        signup_form = UserRegistrationForm()
    return render(request, 'Authentification/Signup.html', {'signup_form': signup_form})


def user_account(request):
    contacts = Contact.objects.all()
    answers = Answer.objects.all()
    
    context = {
        "contacts" :  contacts,
        "answers" :  answers
    }
    
    return render(request, 'Authentification/Profile.html', context)




@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']

        # Mettre à jour les données de l'utilisateur
        user = request.user
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        # Afficher un message de succès
        messages.success(request, 'Votre profil a été mis à jour avec succès!')

        # Rediriger l'utilisateur vers la page d'accueil ou une autre page
        return redirect('home')  # Assurez-vous d'avoir la bonne URL ici

    else:
        # Afficher le formulaire avec les données actuelles de l'utilisateur
        return render(request, 'Profile.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Mettre à jour la session de l'utilisateur pour éviter de le déconnecter après avoir changé le mot de passe
            update_session_auth_hash(request, user)
            messages.success(
                request, 'Votre mot de passe a été mis à jour avec succès!')
            # Rediriger vers la page d'accueil ou une autre page après la modification du mot de passe
            return redirect('home')
        else:
            error_message = ""
            form_errors = form.errors.values()
            for error in form_errors:
                error_message += " " + error
            return render(request, 'Authentification/Profile.html', {'form': form, 'error_message': error_message})
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'Authentification/Profile.html', {'form': form})


def logout_view(request):
    logout(request)
    # Rediriger vers la page d'accueil ou une autre page après la déconnexion
    return redirect('home')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Rediriger l'utilisateur vers la page d'accueil ou une autre page après la connexion réussie
            return redirect('home')
        else:
            error_message = 'Identifiants incorrects. Veuillez reessayer.'
            return render(request, 'Authentification/Login.html', {'error_message': error_message})
    return render(request, 'Authentification/Login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Vérifier si les mots de passe correspondent
        if password1 != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, 'Authentification/Signup.html', {'error_message': "Les mots de passe ne correspondent pas."})

        # Vérifier si l'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur est déjà pris.")
            return render(request, 'Authentification/Signup.html', {'error_message': "Ce nom d'utilisateur est déjà pris."})

        # Vérifier si l'e-mail est déjà utilisé
        if User.objects.filter(email=email).exists():
            messages.error(request, "Cet e-mail est déjà utilisé.")
            return render(request, 'Authentification/Signup.html', {'error_message': "Cet e-mail est déjà utilisé."})

        # Vérifier si le nom d'utilisateur est assez long
        if len(username) < 5:
            messages.error(
                request, "Le nom d'utilisateur doit contenir au moins 5 caractères.")
            return render(request, 'Authentification/Signup.html', {'error_message': "Le nom d'utilisateur doit contenir au moins 5 caractères."})

        # Vérifier si le mot de passe respecte le motif avec une expression régulière
        pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=])(?!\s).{8,}$"
        if not re.match(pattern, password1):
            messages.error(
                request, "Le mot de passe doit contenir au moins 8 caractères, dont au moins une lettre minuscule, une lettre majuscule, un chiffre et un caractère spécial.")
            return render(request, 'Authentification/Signup.html', {'error_message': "Le mot de passe doit contenir au moins 8 caractères, dont au moins une lettre minuscule, une lettre majuscule, un chiffre et un caractère spécial."})

        # Vérifier si le mot de passe ressemble trop au nom d'utilisateur
        if username.lower() in password1.lower():
            messages.error(
                request, "Le mot de passe ne doit pas contenir le nom d'utilisateur.")
            return render(request, 'Authentification/Signup.html', {'error_message': "Le mot de passe ne doit pas contenir le nom d'utilisateur."})

        # Créer un nouvel utilisateur
        user = User.objects.create_user(
            username=username, email=email, password=password1)
        user.save()

        # Connecter l'utilisateur après l'inscription
        login(request, user)

        # Rediriger l'utilisateur vers la page d'accueil ou une autre page après l'inscription
        return redirect('home')
    else:
        # Afficher le formulaire d'inscription
        return render(request, 'Authentification/Signup.html')


def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(
                    request, "Aucun utilisateur n'est associé à cette adresse email.")
                return render(request, 'Authentification/password_reset_form.html', {'error_message': "Aucun utilisateur n'est associé à cette adresse email."})

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            # Remplacez par l'URL de votre site
            reset_link = f"http://{request.META['HTTP_HOST']}/password-reset/{uid}/{token}/"
            subject = "Réinitialisation de mot de passe"
            message = f"Bonjour,\n\nVous avez demandé une réinitialisation de mot de passe. Veuillez cliquer sur le lien suivant pour réinitialiser votre mot de passe :\n\n{reset_link}\n\nSi vous n'avez pas demandé cette réinitialisation, ignorez simplement cet email.\n\nCordialement,\nVotre équipe de support"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
            messages.success(
                request, "Un email vous a été envoyé avec des instructions pour réinitialiser votre mot de passe.")
            return render(request, 'Authentification/Login.html')
    else:
        form = PasswordResetForm()
    return render(request, 'Authentification/password_reset_form.html', {'form': form})
