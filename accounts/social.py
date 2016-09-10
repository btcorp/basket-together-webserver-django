from .models import Profile

USER_FIELDS = ['email', ]

"""
def create_user(strategy, details, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    # fields = dict((name, kwargs.get(name, details.get(name)))
    #               for name in strategy.setting('USER_FIELDS', USER_FIELDS))
    fields = {'email': details.get('email')}

    if not fields:
        return

    return {
        'is_new': True,
        'user': strategy.create_user(**fields)
    }
"""


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        profile = user.get_profile()
        if profile is None:
            profile = Profile(user_id=user.id)

        user.email = response.get('email')
        user.first_name = response.get('first_name')
        user.last_name = response.get('first_name')
        profile.nickname = response.get('name')
        profile.join_path = 'facebook'

        profile.save()
        user.save()