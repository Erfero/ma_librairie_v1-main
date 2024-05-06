from django.contrib import admin
from  .models import *

# Register your models here.

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Gender)
admin.site.register(Comment)
from .models import Author

# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'biography', 'image')
    
    def display_image(self, obj):
        return f'<img src="{obj.image.url}" width="50" height="50" />'
    
    display_image.allow_tags = True
    display_image.short_description = "image"
