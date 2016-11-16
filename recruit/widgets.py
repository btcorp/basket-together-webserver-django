# -*- coding:utf-8 -*-

import re
from django import forms
from django.template.loader import render_to_string


class GoogleMapWidget(forms.HiddenInput):
    def render(self, name, value, attrs=None):
        lat, lng = '37.497921', '127.027636'    # default center of map

        if value:
            lat, lng = re.findall(r'[\d\.]+', value)

        html = render_to_string('recruit/google_map_widget.html', {
            'id': attrs['id'],
            'base_lat': lat,
            'base_lng': lng,
        })

        return super(GoogleMapWidget, self).render(name, value, attrs) + html