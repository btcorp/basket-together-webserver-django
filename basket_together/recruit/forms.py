from django import forms
from recruit.models import Post, Comment
from recruit.widgets import GoogleMapWidget
from django_summernote.widgets import SummernoteWidget
from crispy_forms.helper import FormHelper


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'recruit_count', 'latlng', )
        widgets = {
            'content': SummernoteWidget,
            'latlng': GoogleMapWidget,
        }

    # def __init__(self, *args, **kwargs):
    #     super(PostForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_class = 'form-horizontal'
    #     self.helper.label_class = 'col-lg-2'
    #     self.helper.field_class = 'col-lg-10'


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content', )
