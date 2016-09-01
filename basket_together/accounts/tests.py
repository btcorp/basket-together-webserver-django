from django.test import TestCase

import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone

data = {'date': timezone.now()}

# DjangoJSONEncode 클래스를 추가하지 않으면 TypeError가 발생.
json_data = json.dumps(data, cls=DjangoJSONEncoder)

print(json_data)