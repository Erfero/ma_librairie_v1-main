from django import forms
from .models import Comment, Answer


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "content",
        ] 


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = [
            "content",
        ]  

# class BookSearchForm(forms.Form):
#     title = forms.CharField(label='Titre', required=False)
#     author = forms.CharField(label='Auteur', required=False)
#     category = forms.CharField(label='Catégorie', required=False)


class BookSearchForm(forms.Form):
    OPTION_CHOICES = [
        ('', '---'),  # Option vide par défaut
        ('title', 'Title'),
        ('author', 'Author'),
        ('category', 'Category'),
    ]
    option = forms.ChoiceField(choices=OPTION_CHOICES, required=False)
    q = forms.CharField(label='Search', required=False)


class AdvancedSearchForm(forms.Form):
    min_price = forms.DecimalField(label='Min Price', required=False)
    max_price = forms.DecimalField(label='Max Price', required=False)
    sort_by_price = forms.ChoiceField(choices=(('ascending', 'Ascending'), ('descending', 'Descending')), required=False)
    sort_by_author = forms.ChoiceField(choices=(('ascending', 'A to Z'), ('descending', 'Z to A')), required=False)
    sort_by_title = forms.ChoiceField(choices=(('ascending', 'A to Z'), ('descending', 'Z to A')), required=False)
