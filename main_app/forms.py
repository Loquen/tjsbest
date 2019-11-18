from django import forms

from .models import Comment, Item

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ('text',)

