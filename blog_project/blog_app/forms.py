from django import forms

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



# 채림님 작성중이던 form
# class ArticleForm(forms.ModelForm):
#     class Meta:
#         model = Article
#         fields = ['title', 'content']