from django import forms
from .models import Article

#로그인 form
class LoginForm(forms.Form):
    username = forms.CharField(
        widget = forms.TextInput(attrs={'placeholder' : 'Username', 'class':'login-input'}),
        label='',
    )
    password = forms.CharField(
         widget = forms.PasswordInput(attrs={'placeholder' : 'Password', 'class':'login-input'}),
        label='',
    )

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'topic']
        exclude = ['published_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['topic'].required = False 