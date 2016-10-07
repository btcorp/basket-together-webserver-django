from django import forms
from recruit.models import Comment, Post
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
        fields = ('title', 'content', 'meeting_date', 'recruit_count', 'latlng', 'address1', 'address2')
        labels = {
            'title': '제목',
            'content': '내용',
            'meeting_date': '모임날짜',
            'recruit_count': '모집인원',
            'address1': '주소',
            'address2': '상세주소'
        }
        help_texts = {

        }
        error_messages = {

        }
        widgets = {
            'content': SummernoteWidget,
            'meeting_date': DateTimeWidget(usel10n=True, bootstrap_version=3, options=dateTimeOptions),
            'latlng': GoogleMapWidget,
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )
