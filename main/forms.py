from django.forms import ModelForm

from .models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text', 'rating', 'author_name')
        initial = {'to_item': 1}
