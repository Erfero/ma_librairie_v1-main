from django.urls import path
from . import views

app_name = "contacts"

urlpatterns = [
    # urls définis pour les contacts
    path('', views.indexContact, name='contacts'),
    path('edit/<int:contact_id>/', views.indexContact, name='edit_contact'),
    path('delete/<int:contact_id>/', views.deleteContact, name='delete_contact'),
    
    # urls définis pour les réponses associées à un contact
    path('<int:contact_id>/new_answer/', views.create_answer, name='new_answer'),
    path('<int:contact_id>/edit_answer/<int:answer_id>/', views.update_answer, name='edit_answer'),
    path('<int:contact_id>/delete_answer/<int:answer_id>/', views.delete_answer, name='delete_answer'),
]