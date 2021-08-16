from django import forms
from .models import Post, Comment


# formsではadminで使う編集フォームを簡単に作れる！

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)
