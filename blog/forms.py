from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={
                                                                    'placeholder': 'Name',
                                                                    'id': 'sharepost-name',
                                                                    'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
                                                        'placeholder': 'Email',
                                                        'id': 'sharepost-email',
                                                        'class': 'form-control'}))
    to = forms.EmailField(widget=forms.EmailInput(attrs={
                                                    'placeholder': 'To',
                                                    'id': 'sharepost-to',
                                                    'class': 'form-control'}))
    comments = forms.CharField(required=False,
                                widget=forms.Textarea(attrs={
                                                        'placeholder': 'Comments',
                                                        'id': 'sharepost-comments',
                                                        'class': 'form-control'}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
            'name': forms.TextInput(attrs={'id': 'comment-name',
                                            'class': 'form-control',
                                            'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'id': 'comment-email',
                                                'class': 'form-control',
                                                'placeholder': 'Email'}),
            'body': forms.Textarea(attrs={'id': 'comment-body',
                                            'class': 'form-control',
                                            'placeholder': 'Comment'})
        }


class SearchForm(forms.Form):
    query = forms.CharField()