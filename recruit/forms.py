from django import forms
from recruit.models import Comment, Post
from recruit.widgets import GoogleMapWidget
from django_summernote.widgets import SummernoteWidget
from datetimewidget.widgets import DateTimeWidget
from django.utils.translation import ugettext_lazy as _

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
            'title': _('title'),
            'content': _('content'),
            'meeting_date': _('meeting date'),
            'recruit_count': _('recruit count'),
            'address1': _('address'),
            'address2': _('detail address'),
        }
        help_texts = {

        }
        error_messages = {

        }
        widgets = {
            'content': SummernoteWidget,
            'meeting_date': DateTimeWidget(usel10n=True, bootstrap_version=3, options=dateTimeOptions),
            'latlng': GoogleMapWidget,
            'address1': forms.HiddenInput(attrs={'readonly': True})
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content', )
        labels = {
            'content': '',
        }
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': _('comment registration')}),
        }
