from django import forms
from recruit.models import Post, Comment
from recruit.widgets import GoogleMapWidget
from django_summernote.widgets import SummernoteWidget
from datetimewidget.widgets import DateTimeWidget


dateTimeOptions = {
    'format': 'yyyy-mm-dd P HH:ii',
    'autoclose': True,
    'showMeridian': True,
}


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'meeting_date', 'recruit_count', 'latlng')
        widgets = {
            'content': SummernoteWidget,
            'meeting_date': DateTimeWidget(usel10n=True, bootstrap_version=3, options=dateTimeOptions),
            'latlng': GoogleMapWidget,
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content', )
