from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class GuestForm(forms.Form):
    email = forms.EmailField(
		widget=forms.EmailInput(
			attrs={
				'class': 'form-control',
				'id': 'guest-form-email',
				'placeholder': 'Your email'
			}))


class GuestRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(
                    label='Confirm password',
                    widget=forms.PasswordInput
                    )

    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = CustomUser.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


class LoginForm(forms.Form):
    email = forms.EmailField(
		widget=forms.TextInput(
			attrs={
				'class': 'form-control',
				'id': 'form-username',
				'placeholder': 'Your Email',
				'name': 'email'
			}))
    password = forms.CharField(
		widget=forms.PasswordInput(
			attrs={
				'class': 'form-control',
				'id': 'form-password',
				'placeholder': 'Your password',
				'name': 'password'
			}))


class CustomUserCreationForm(UserCreationForm):
#class CustomUserCreationForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email')

    first_name = forms.CharField(
	    label='First Name',
	    widget=forms.TextInput(
		    attrs={
			    'class':'form-control',
			    'id':'first-name',
			    'placeholder':'First Name'
		    }))

    last_name = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(
	        attrs={
				'class': 'form-control',
				'id': 'last-name',
				'placeholder': 'Last Name'
	        }))

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
	        attrs={
				'class': 'form-control',
				'id': 'guest-form-email',
				'placeholder': 'Your email'
			}))
    password1 = forms.CharField(
		label='Password',
		widget=forms.PasswordInput(
		    attrs={
			    'class': 'form-control',
			    'id': 'form-password',
			    'placeholder': 'Your password'
		    }))
    password2 = forms.CharField(
	    label='Password Confirmation',
	    widget=forms.PasswordInput(
		    attrs={
			    'class': 'form-control',
			    'id': 'form-password2',
			    'placeholder': 'Your password again'
		    }))


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    first_name = forms.CharField(
		label='First Name',
		widget=forms.TextInput(
			attrs={
				'class': 'form-control',
				'id': 'first-name',
				'placeholder': 'First Name'
			}))
    last_name = forms.CharField(
	    label='Last Name',
	    widget=forms.TextInput(
		    attrs={
			    'class': 'form-control',
			    'id': 'last-name',
			    'placeholder': 'Last Name'
		    }))
    email = forms.EmailField(
		label='Email',
		widget=forms.EmailInput(
		    attrs={
			    'class': 'form-control',
			    'id': 'guest-form-email',
			    'placeholder': 'Your email'
		    }))
