############################ Importation des ressources ##############################

import json
from .models import *
from typing import Any
from django.views import View
from django.views.generic import *
from django.db.models import Count, Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import CommentForm, AnswerForm, AdvancedSearchForm
from django.shortcuts import get_object_or_404, render, redirect

# Create your views here.

############################ Books ##############################


## Méthode récupérant tous les livres disponibles par ordre de date de publication avec le nombre de commentaires associé à chaque livre
def books(request):
    ## récupérer la liste des livres en ordonnant par date de publication
    books = Book.objects.order_by("-published_date")
    ## parcourir le tableau des livres pour ajouter le nombre de commentaires dans chaque objet représentant un livre
    for book in books:
        ## récupérer le nombre de commentaire associé à chaque livre
        comment_count = Comment.objects.filter(book_id=book.id).count()
        ## ajoute la clé number_comments dans chaque objet de livre
        book.number_comments = comment_count
    ## Pagination pour avoir 4 livres par page
    paginator = Paginator(books, 8)
    page = request.GET.get("page")
    books = paginator.get_page(page)
    ## retourner la vue d'affichage des livres avec les livres triés et leur nombre de commentaires
    return render(request, "Books/books.html", {"books": books})


############################ Authors ##############################


## Méthode récupérant tous les auteurs disponibles par ordre de date de publication
def authors(request):
    authors = Author.objects.all()

    ## Pagination pour avoir 4 livres par page
    paginator = Paginator(authors, 4)
    page = request.GET.get("page")
    authors = paginator.get_page(page)
    return render(request, "Authors/authors.html", {"authors": authors})

def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    books = author.book_set.all()  # Récupérez les livres associés à l'auteur
    genres = author.book_set.values_list("genre__name", flat=True).distinct()  # Récupérez les genres de livres associés à l'auteur

    context = {
        "author": author,
        "books": books,
        "genres": genres,
    }

    return render(request, "Authors/author_detail.html", context)


############################ Authors ##############################


## Méthode récupérant tous les auteurs disponibles par ordre de date de publication
def authors_list(request):
    authors = Author.objects.all()
    return render(request, "authors_list.html", {"authors": authors})


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def search(request):
    books = Book.objects.all()
    query = request.GET.get("search_value", "")

    # Si aucun filtre n'est spécifié, rechercher dans tous les champs pertinents
    books = books.filter(
    Q(title__icontains=query) |
    Q(author__name__icontains=query) |
    Q(genre__name__icontains=query)
    )

    ## Pagination pour avoir 4 livres par page
    paginator = Paginator(books, 4)
    page = request.GET.get("page")
    books = paginator.get_page(page)

    return render(request, "Books/books.html", {"books": books})


def advanced_search(request):
    if request.method == "POST":
        form = AdvancedSearchForm(request.POST)
        if form.is_valid():
            # Récupérer les données soumises par le formulaire
            min_price = form.cleaned_data.get("min_price")
            max_price = form.cleaned_data.get("max_price")
            sort_by_price = form.cleaned_data.get("sort_by_price")
            sort_by_author = form.cleaned_data.get("sort_by_author")
            sort_by_title = form.cleaned_data.get("sort_by_title")
            print(
                min_price,
                max_price,
                sort_by_author,
                sort_by_price,
            )
            # Filtrer les livres en fonction des critères choisis
            books = Book.objects.all()

            if min_price:
                books = books.filter(price__gte=min_price)
            if max_price:
                books = books.filter(price__lte=max_price)

            if sort_by_price == "ascending":
                books = books.order_by("price")
            elif sort_by_price == "descending":
                books = books.order_by("-price")

            if sort_by_author == "ascending":
                books = books.order_by("author__name")
            elif sort_by_author == "descending":
                books = books.order_by("-author__name")

            if sort_by_title == "ascending":
                books = books.order_by("title")
            elif sort_by_title == "descending":
                books = books.order_by("-title")
                
            ## Pagination pour avoir 4 livres par page
            paginator = Paginator(books, 4)
            page = request.GET.get("page")
            books = paginator.get_page(page)

            # Renvoyer les résultats à afficher dans le template
            return render(request, "Books/books.html", {"books": books})
    else:
        form = AdvancedSearchForm()
    return render(request, "Books/advanced_search.html", {"form": form})


#############################################################################


def my_books(request, page=1):
    # Récupérer la liste d'objets à afficher
    liste_items = Book.objects.all()

    # Paginer la liste d'objets
    paginator = Paginator(liste_books, 3)  # 10 éléments par page
    page = request.GET.get("page")

    try:
        liste_books = paginator.page(page)
    except PageNotAnInteger:
        # Si la page n'est pas un entier, afficher la première page
        liste_books = paginator.page(1)
    except EmptyPage:
        # Si la page est hors de portée (par exemple, page 9999), afficher la dernière page
        liste_books = paginator.page(paginator.num_pages)

    # Passer la liste paginée au contexte
    contexte = {"liste_books": liste_books}

    # Utiliser la fonction render pour rendre la vue avec le contexte
    return render(request, "homebooks.html", contexte)


def book_detail(request, book_id):
    # Récupérer le livre et les commentaires associés
    book = get_object_or_404(Book, id=book_id)
    comments = Comment.objects.filter(book=book)
    book.author = Author.objects.get(id=book.author_id)
    otherBooks = Book.objects.filter(author=book.author).exclude(id=book_id)

    # Récupérer les catégories associées au livre
    categories = book.genre.all()

    # Initialiser le formulaire de commentaire
    form = CommentForm(initial={"content": ""})
    # variable d'édition
    editing = False
    # Vérifier si la requête est de type POST
    if request.method == "POST":
        # Créer une instance de formulaire et la remplir avec les données de la requête
        form = CommentForm(request.POST)
        # Vérifier si le formulaire est valide
        if form.is_valid():
            # Créer un commentaire sans l'enregistrer dans la base de données
            comment = form.save(commit=False)
            # Ajouter le livre et l'utilisateur au commentaire
            comment.book = book
            comment.user = request.user
            # Enregistrer le commentaire dans la base de données
            comment.save()
            # Rediriger l'utilisateur vers la même page
            return redirect("book_detail", book_id=book_id)
    # Rendre la page de détail du livre avec le formulaire de commentaire
    return render(
        request,
        "Books/book_detail.html",
        {
            "book": book,
            "comments": comments,
            "form": form,
            "editing": editing,
            "otherBooks": otherBooks,
            "categories": categories,
        },
    )



# Ajout d'un livre
# @login_required


def authors_list(request):
    authors = Author.objects.all()
    return render(request, "authors_list.html", {"authors": authors})


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.user:
        return redirect("book_detail", book_id=comment.book.id)
    form = CommentForm(instance=comment)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("book_detail", book_id=comment.book.id)

    return render(request, "Books/book_detail.html", {"form": form})


@login_required
def delete_comment(request, comment_id):
    # Récupérer le commentaire
    comment = get_object_or_404(Comment, id=comment_id)
    # Vérifier si l'utilisateur est l'auteur du commentaire
    if request.user != comment.user:
        return redirect("book_detail", book_id=comment.book.id)
    # Stocker l'ID du livre avant de supprimer le commentaire
    book_id = comment.book.id
    # Supprimer le commentaire
    comment.delete()
    # Rediriger l'utilisateur vers la page de détail du livre
    return redirect("book_detail", book_id=book_id)


@login_required
def reply_to_comment(request, comment_id, answer_id=None):
    comment = get_object_or_404(Comment, id=comment_id)
    form = AnswerForm()
    editing = False

    if answer_id:
        answer = get_object_or_404(Answer, id=answer_id)
        form = AnswerForm(instance=answer)
        editing = True

    if request.method == "POST":
        if editing:
            form = AnswerForm(request.POST, instance=answer)
        else:
            form = AnswerForm(request.POST)

        if form.is_valid():
            answer = form.save(commit=False)
            answer.comment = comment
            answer.user = request.user
            answer.save()
            return redirect("book_detail", book_id=comment.book.id)

    return render(
        request,
        "Books/book_detail.html",
        {"comment": comment, "form": form, "editing": editing},
    )


# Vue pour éditer une réponse
@login_required
def edit_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    if request.user != answer.user:
        return redirect("book_detail", book_id=answer.comment.book.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            return redirect("book_detail", book_id=answer.comment.book.id)
    else:
        form = AnswerForm(instance=answer)
    return render(request, "Books/book_detail.html", {"form": form})


# Vue pour supprimer une réponse
@login_required
def delete_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    if request.user != answer.user:
        return redirect("book_detail", book_id=answer.comment.book.id)
    if request.method == "POST":
        book_id = answer.comment.book.id
        answer.delete()
        return redirect("Books/book_detail.html", book_id=book_id)
    return render(request, "Books/book_detail.html", {"answer": answer})



@login_required
def add_to_cart(request, bookId):
    try:
        # Récupérer le livre à partir de l'identifiant bookId
        book = get_object_or_404(Book, id=bookId)
        
        # Récupérer l'utilisateur connecté
        user = request.user
        
        # Vérifier si l'utilisateur a déjà un panier, sinon en créer un nouveau
        cart, created = Cart.objects.get_or_create(user=user)
        
        # Ajouter le livre au panier
        cart.book.add(book)
        
        # Envoyer un message de succès
        messages.success(request, "Livre ajouté au panier avec succès!")
    
    except Exception as e:
        # Envoyer un message d'erreur
        messages.error(request, "Une erreur s'est produite lors de l'ajout au panier.")
    
    # Rediriger l'utilisateur vers la même page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def get_cart_books(request):
    try:
        # Récupérer l'utilisateur connecté
        user = request.user
        
        # Récupérer le panier de l'utilisateur
        cart = Cart.objects.get(user=user)
        
        # Récupérer la liste des livres dans le panier
        cart_books = cart.book.all()
        
        # Retourner la liste des livres du panier
        return render(request, "Cart/Cart.html", {"cart_books": cart_books})
    
    except Cart.DoesNotExist:
        # Si le panier n'existe pas, retourner une liste vide
        cart_books = []
        return render(request, "Cart/Cart.html", {"cart_books": cart_books})

@login_required
def remove_from_cart(request, bookId):
    try:
        # Récupérer le livre à partir de l'identifiant bookId
        book = get_object_or_404(Book, id=bookId)
        
        # Récupérer l'utilisateur connecté
        user = request.user
        
        # Vérifier si l'utilisateur a déjà un panier
        cart = Cart.objects.get(user=user)
        
        # Vérifier si le livre est présent dans le panier
        if book in cart.book.all():
            # Retirer le livre du panier
            cart.book.remove(book)
            messages.success(request, "Livre retiré du panier avec succès!")
        else:
            messages.error(request, "Ce livre n'est pas dans votre panier.")
    
    except Cart.DoesNotExist:
        # Si le panier n'existe pas, envoyer un message d'erreur
        messages.error(request, "Votre panier est vide.")
    
    # Rediriger l'utilisateur vers la même page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def checkout(request):
    if 'cart' in request.GET and 'quantities' in request.GET:
        cart_content = json.loads(request.GET['cart'])
        quantities = json.loads(request.GET['quantities'])
        
        try:
            # Récupérer l'utilisateur connecté
            user = request.user

            # Récupérer le panier de l'utilisateur connecté s'il existe
            cart = get_object_or_404(Cart, user=user)

            # Créer une commande
            order = Order.objects.create(user=user, total_price=0, order_status="Accepté")

            # Calculer le prix total de la commande en fonction des éléments du panier
            total_price = 0
            for book_data, quantity in zip(cart_content, quantities):
                book_id = book_data['id']
                book_price = float(book_data['price'].replace(',', '.'))  # Remplacer la virgule par un point
                # Créer un élément de commande pour chaque livre dans le panier
                order_item = OrderItem.objects.create(order=order, book_id=book_id, quantity=quantity, price=book_price)
                # Mettre à jour le prix total de la commande
                total_price += quantity * book_price

            # Mettre à jour le prix total de la commande
            order.total_price = total_price
            order.save()

            # Supprimer le panier de l'utilisateur après la création de la commande
            cart.delete()

             # Si le paiement n'est pas réussi, envoyer un message d'erreur
            messages.success(request, "Paiement effectué avec succès !")

        except Exception as e:
            messages.error(request, "Une erreur est survenue lors du paiement !")
        
        # Rediriger l'utilisateur vers la même page
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        # Si les paramètres cart ou quantities sont manquants, envoyer un message d'erreur
        messages.error(request, "Une erreur est survenue lors du paiement !")

    # Rediriger l'utilisateur vers la même page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
## Fonction permettant d'afficher les livres par recommendations
def books_by_recommended(request, page=1):
    # Les livres par recommendation
    liste_books_recommended = Book.objects.order_by('recommended_number')

    # Paginer la liste d'objets
    paginator = Paginator(liste_books_recommended, 12)  # 10 éléments par page
    page = request.GET.get('page')

    try:
        liste_books_recommended = paginator.page(page)
    except PageNotAnInteger:
        # Si la page n'est pas un entier, afficher la première page
        liste_books_recommended = paginator.page(1)
    except EmptyPage:
        # Si la page est hors de portée (par exemple, page 9999), afficher la dernière page
        liste_books_recommended = paginator.page(paginator.num_pages)

    # Passer la liste paginée au contexte
    contexte = {
        'our_books_recommended': liste_books_recommended,
        }
    # Redirection vers la page d'accueil
    return render(request, 'Books/recommende.html', contexte)

