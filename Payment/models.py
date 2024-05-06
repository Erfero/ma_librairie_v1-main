from django.db import models

## Importation de uuid pour avoir la possibilité d'utiliser des UUID au lieu des id
import uuid
# Importation de Order pour avoir la possibilité d'utiliser l'id de la commande
from Catalogue.models import Order



# by @a_warrisw (16/02/2024)

# Modèle implémentant un paiement
class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="UUID pour identifier le paiement")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, help_text="L'id de la commande")
    amount = models.DecimalField(max_digits=6, decimal_places=2, help_text="Le montant du paiement")
    payment_method = models.CharField(max_length=100, help_text="Le moyen de paiement")
    created_at = models.DateTimeField(auto_now_add=True, help_text="La date de création du paiement")
    updated_at = models.DateTimeField(auto_now=True, help_text="La date de mise à jour du paiement")


## Modèle implémentant une facture
class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="UUID pour identifier la facture")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, help_text="L'id de la commande")
    invoice_number = models.CharField(max_length=100, help_text="Le numéro de facture")
    amount = models.DecimalField(max_digits=6, decimal_places=2, help_text="Le montant de la facture")
    created_at = models.DateTimeField(auto_now_add=True, help_text="La date de création de la facture")
    updated_at = models.DateTimeField(auto_now=True, help_text="La date de mise à jour de la facture")

   