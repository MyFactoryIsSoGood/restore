from django.contrib import admin
from .models import Gadget, Comment


class GadgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'date_published', 'to_item')


admin.site.register(Gadget, GadgetAdmin)
admin.site.register(Comment, CommentAdmin)
