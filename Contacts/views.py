# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact, Answer
from .forms import ContactForm, AnswerForm


# Définition de la méthode indexContact
def indexContact(request, contact_id=None):
    active_page = "contacts"
    # Si la requête est de type POST
    if request.method == "POST":
        # On crée un formulaire avec les données de la requête
        form = ContactForm(request.POST)
        # Si le formulaire est valide
        if form.is_valid():
            # Si un contact_id est fourni
            if contact_id:
                # On récupère le contact correspondant
                contact = get_object_or_404(Contact, id=contact_id)
                # On met à jour le contact avec les données du formulaire
                form = ContactForm(request.POST, instance=contact)
                form.save()
            else:
                # On crée un nouveau contact avec les données du formulaire
                form.save()
            # On redirige vers la page des contacts
            return redirect("contacts:contacts")
    else:
        # Si la requête n'est pas de type POST
        if contact_id:
            # Si un contact_id est fourni, on pré-remplit le formulaire avec les données du contact
            contact = get_object_or_404(Contact, id=contact_id)
            form = ContactForm(instance=contact)
        else:
            # Sinon, on fournit un formulaire vide
            form = ContactForm()
    # On récupère tous les contacts
    contacts = Contact.objects.all()
    # On rend le template avec le formulaire et les contacts
    return render(request, "Contacts/index.html", {"form": form, "contacts": contacts, "active_page": active_page})


# Définition de la méthode deleteContact
def deleteContact(request, contact_id):
    # On récupère le contact correspondant à l'id
    contact = get_object_or_404(Contact, id=contact_id)
    if contact_id:
        # On supprime le contact
        contact.delete()
        return redirect('contacts:contacts')
    # On récupère tous les contacts restants
    contacts = Contact.objects.all()
    # On fournit un formulaire vide
    form = ContactForm()
    # On rend le template avec le formulaire et les contacts
    return render(request, "Contacts/index.html", {"form": form, "contacts": contacts})


# Création d'une réponse
def create_answer(request, contact_id):
    # Si la requête est de type POST
    if request.method == "POST":
        # On crée un formulaire avec les données de la requête
        form = AnswerForm(request.POST)
        # Si le formulaire est valide
        if form.is_valid():
            # On récupère le contact correspondant
            contact = get_object_or_404(Contact, id=contact_id)
            # On crée une nouvelle réponse avec les données du formulaire et le contact
            Answer.objects.create(
                contact=contact, answer_text=form.cleaned_data["answer_text"]
            )
            # On redirige vers la page du contact
            return redirect("contacts:contacts")
    # Si la requête n'est pas de type POST, on fournit un formulaire vide
    form = AnswerForm()
    # On récupère toutes les réponses
    answers = Answer.objects.filter(id=contact_id)
    # On rend le template avec le formulaire et les réponses
    return render(request, "Contacts/index.html", {"form": form, "answers": answers})


# Modification d'une réponse
def update_answer(request, contact_id, answer_id):
    # On récupère la réponse correspondante
    answer = get_object_or_404(Answer, id=answer_id, contact_id=contact_id)
    # Si la requête est de type POST
    if request.method == "POST":
        # On crée un formulaire avec les données de la requête et la réponse existante
        form = AnswerForm(request.POST, instance=answer)
        # Si le formulaire est valide
        if form.is_valid():
            # On met à jour la réponse avec les données du formulaire
            form.save()
            # On redirige vers la page du contact
            return redirect("contacts:contacts")
    # Si la requête n'est pas de type POST, on pré-remplit le formulaire avec les données de la réponse
    form = AnswerForm(instance=answer)
    # On récupère toutes les réponses
    answers = Answer.objects.filter(contact_id=contact_id)
    # On rend le template avec le formulaire et les réponses
    return render(request, "Contacts/edit.html", {"form": form, "answers": answers})


# Suppression d'une réponse
def delete_answer(request, contact_id, answer_id):
    # On récupère la réponse correspondante
    answer = get_object_or_404(Answer, id=answer_id, contact_id=contact_id)
 
    if answer_id:
        # On supprime la réponse
        answer.delete()
        return redirect("contacts:contacts")
    # On récupère toutes les réponses restantes
    answers = Answer.objects.filter(contact_id=contact_id)
    # On fournit un formulaire vide
    form = AnswerForm()
    # On rend le template avec le formulaire et les réponses
    return render(request, "Contacts/index.html", {"form": form, "answers": answers})
