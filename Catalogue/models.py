from django.db import models
## Importation de uuid pour avoir la possibilité d'utiliser des UUID au lieu des id
import uuid
## Importation de get_user_model pour avoir la possibilité d'utiliser les utilisateurs de la table User django
from django.contrib.auth import get_user_model

User = get_user_model()

## by @a_warrisw (16/02/2024)

## Modèle implémentant un livre
class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="UUID pour identifier le livre")
    title = models.CharField(max_length=100, help_text="Titre du livre")
    author = models.ForeignKey('Author', on_delete=models.CASCADE, help_text="l'id de l'auteur du livre")
    genre = models.ManyToManyField('Gender', help_text="l'id du genre du livre")
    summary = models.TextField(help_text="le résumé du livre", blank=True, default=None)
    price = models.DecimalField(max_digits=6, decimal_places=2, help_text="Le prix du livre")
    num_pages = models.IntegerField(help_text="Le nombre de pages du livre")
    cover_image = models.ImageField(upload_to='book_covers', help_text="L'image de couverture du livre",blank=True, default=None)
    published_date = models.DateField(help_text="La date de publication du livre")
    availibility = models.BooleanField(help_text="La disponibilité du livre")
    recommended_number = models.IntegerField(help_text="Le nombre de fois que le livre a été recommmandé")
    created_at = models.DateTimeField(auto_now_add=True, help_text="La date de création du livre")
    updated_at = models.DateTimeField(auto_now=True, help_text="La date de mise à jour du livre")

    ## Méthode pour afficher le titre du livre
    def __str__(self):
        return self.title

## Modèle implémentant un auteur
class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="UUID pour identifier l'auteur")
    name = models.CharField(max_length=255, help_text="Le nom de l'auteur", blank=True, default=None)
    biography = models.TextField(help_text="La biographie de l'auteur", blank=True, default=None)
    image = models.ImageField(upload_to='authorImage', blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True, help_text="La date de création de l'auteur")
    updated_at = models.DateTimeField(auto_now=True, help_text="La date de mise à jour de l'auteur")

    ## Méthode pour afficher le nom de l'auteur
    def __str__(self):
        return self.name

## Modèle implémentant un genre
class Gender(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="UUID pour identifier le genre")
    name = models.CharField(max_length=100, help_text="Le nom du genre")
    created_at = models.DateTimeField(auto_now_add=True, help_text="La date de création du genre")
    updated_at = models.DateTimeField(auto_now=True, help_text="La date de mise à jour du genre")

    ## Méthode pour afficher le nom du genre
    def __str__(self):
        return self.name

## Modèle implémentant un commentaire d'un livre
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="UUID pour identifier le commentaire")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, help_text="L'id du livre")
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="L'id de l'utilisateur")
    content = models.TextField(max_length=1000, help_text="Le contenu du commentaire")
    created_at = models.DateTimeField(auto_now_add=True, help_text="La date de création du commentaire")
    updated_at = models.DateTimeField(auto_now=True, help_text="La date de mise à jour du commentaire")


class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="UUID pour identifier la réponse")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, help_text="L'id du commentaire")
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="L'id de l'utilisateur")
    content = models.TextField(max_length=1000, help_text="Le contenu de la réponse")
    created_at = models.DateTimeField(auto_now_add=True, help_text="La date de création de la réponse")
    updated_at = models.DateTimeField(auto_now=True, help_text="La date de mise à jour de la réponse")


## Modèle implémentant un panier
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="UUID pour identifier le panier")
    updated_at = models.DateTimeField(auto_now=True, help_text="La date de mise à jour du panier")
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="L'utilisateur du panier")
    book = models.ManyToManyField(Book, help_text="Le livre du panier")
    created_at = models.DateTimeField(auto_now_add=True, help_text="La date de création du panier")
    updated_at = models.DateTimeField(auto_now=True, help_text="La date de mise à jour du panier")


## Modèle implémentant une commande
class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="UUID pour identifier la commande")
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="L'utilisateur de la commande")
    total_price = models.DecimalField(max_digits=6, decimal_places=2, help_text="Le prix total de la commande")
    order_status = models.CharField(max_length=100, help_text="Le statut de la commande")
    created_at = models.DateTimeField(auto_now_add=True, help_text="La date de création de la commande")
    updated_at = models.DateTimeField(auto_now=True, help_text="La date de mise à jour de la commande")

## Modèle implémentant un article d'une commande
class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="UUID pour identifier l'article")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, help_text="L'id de la commande")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, help_text="L'id du livre")
    quantity = models.IntegerField(help_text="La quantité de l'article")
    price = models.DecimalField(max_digits=6, decimal_places=2, help_text="Le prix de l'article")
    created_at = models.DateTimeField(auto_now_add=True, help_text="La date de création de l'article")
    updated_at = models.DateTimeField(auto_now=True, help_text="La date de mise à jour de l'article")