# Generated by Django 5.0.2 on 2024-02-20 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Catalogue', '0004_alter_book_cover_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='biography',
            field=models.TextField(blank=True, default=None, help_text="La biographie de l'auteur"),
        ),
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(blank=True, default=None, help_text="Le nom de l'auteur", max_length=255),
        ),
    ]
