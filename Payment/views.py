from django.shortcuts import render

# Create your views here.


## Méthode récupérant tous les livres disponibles par ordre de date de publication avec le nombre de commentaires associé à chaque livre
def paymentForm(request):
    return render(request, "payment.html")

def paymentSuccess(request):
    return render(request, "payment_success.html")

def paymentCancel(request):
    return render(request, "payment_cancel.html")