# Generated by Django 5.0.1 on 2024-03-01 09:47

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Catalogue", "0007_merge_0006_answer_0006_lbook"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text="UUID pour identifier le panier",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="La date de création du panier"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, help_text="La date de mise à jour du panier"
                    ),
                ),
                (
                    "book",
                    models.ManyToManyField(
                        help_text="Le livre du panier", to="Catalogue.book"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text="L'utilisateur du panier",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text="UUID pour identifier la commande",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "total_price",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Le prix total de la commande",
                        max_digits=6,
                    ),
                ),
                (
                    "order_status",
                    models.CharField(
                        help_text="Le statut de la commande", max_length=100
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="La date de création de la commande",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, help_text="La date de mise à jour de la commande"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text="L'utilisateur de la commande",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text="UUID pour identifier l'article",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("quantity", models.IntegerField(help_text="La quantité de l'article")),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, help_text="Le prix de l'article", max_digits=6
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="La date de création de l'article"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, help_text="La date de mise à jour de l'article"
                    ),
                ),
                (
                    "book",
                    models.ForeignKey(
                        help_text="L'id du livre",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Catalogue.book",
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        help_text="L'id de la commande",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Catalogue.order",
                    ),
                ),
            ],
        ),
    ]
