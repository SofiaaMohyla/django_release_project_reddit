from django import forms
from .models import Commentary, Post


class CommentaryCreationForm(forms.ModelForm):
    class Meta:
        model = Commentary
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super(CommentaryCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'rows': 1})


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description']

    def __init__(self, *args, **kwargs):
        super(PostCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'rows': 5})