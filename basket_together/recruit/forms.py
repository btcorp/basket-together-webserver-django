from django import forms
from recruit.models import Post, Comment
from recruit.widgets import GoogleMapWidget
from django_summernote.widgets import SummernoteWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'recruit_count', 'latlng', )
        widgets = {
            # 'content': SummernoteWidget,
            'latlng': GoogleMapWidget,
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content', )
