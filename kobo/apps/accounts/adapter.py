from allauth.account.adapter import DefaultAccountAdapter
from constance import config
from django.db import transaction

from .forms import SignupForm


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return config.REGISTRATION_OPEN

    def save_user(self, request, user, form, commit=True):
        standard_fields = set(SignupForm().fields.keys())
        extra_fields = set(form.fields.keys()).difference(standard_fields)
        with transaction.atomic():
            user = super().save_user(request, user, form, commit)
            extra_data = {k: form.cleaned_data[k] for k in extra_fields}
            user.extra_details.data.update(extra_data)
            if commit:
                user.extra_details.save()
        return user
