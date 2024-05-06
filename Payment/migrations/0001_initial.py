# Generated by Django 5.0.1 on 2024-03-01 17:15

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("Catalogue", "0008_cart_order_orderitem"),
    ]

    operations = [
        migrations.CreateModel(
            name="Invoice",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text="UUID pour identifier la facture",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "invoice_number",
                    models.CharField(help_text="Le numéro de facture", max_length=100),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Le montant de la facture",
                        max_digits=6,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="La date de création de la facture"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, help_text="La date de mise à jour de la facture"
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
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text="UUID pour identifier le paiement",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Le montant du paiement",
                        max_digits=6,
                    ),
                ),
                (
                    "payment_method",
                    models.CharField(help_text="Le moyen de paiement", max_length=100),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="La date de création du paiement"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, help_text="La date de mise à jour du paiement"
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
