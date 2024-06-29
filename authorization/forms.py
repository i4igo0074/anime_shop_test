from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


from .models import CustomerUser

class CustomerUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomerUser    # Где будем использовать это?
        fields = ('username', 'email', 'phone_number')


class CustomerAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )


    
