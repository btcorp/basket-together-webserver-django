import re
from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class GoogleMapWidget(forms.TextInput):
    def render(self, name, value, attrs=None):
        self.attrs['type'] = 'hidden'

        lat, lng = '37.497921', '127.027636'    # 강남역

        if value:
            lat, lng = re.findall(r'[\d\.]+', value)

        html = render_to_string('recruit/google_map_widget.html', {
            'id': attrs['id'],
            'base_lat': lat,
            'base_lng': lng,
        })

        # return mark_safe(html)
        return super(GoogleMapWidget, self).render(name, value, attrs) + html