from django import forms

from django.contrib.auth import get_user_model
from .models import Category, Meal, User

User = get_user_model()

class UserRegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, help_text="Enter your first name")
    last_name = forms.CharField(max_length=50, help_text="Enter your last name")
    email = forms.EmailField(min_length=5, required=True, help_text="Enter your Symphony e-mail address")
    password = forms.CharField(min_length=5 ,widget=forms.PasswordInput(), help_text="Enter your password")
    password_confirm = forms.CharField(widget=forms.PasswordInput(), help_text="Enter the same password again")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

    def clean(self):
        email = self.cleaned_data.get('email')

        # if email and email.split('@')[1] != "symphony-solutions.eu":
        #     raise forms.ValidationError("You are not using your Symphony e-mail address!")

        email_exist = User.objects.filter(email=email).first()
        if email_exist:
            raise forms.ValidationError("There is account associated with that e-mail address!")

        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password != password_confirm:
            raise forms.ValidationError("Passwords don't match!")

        return self.cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(min_length=5, required=True, help_text="Enter your Symphony Solutions e-mail address")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Enter your password")

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):

        # Un-comment to allow only Symphony Solution e-mails
        # email = self.cleaned_data.get('email')
        # if email and email.split('@')[1] != "symphony-solutions.eu":
        #     raise forms.ValidationError("You are not using your Symphony e-mail address!")

        return self.cleaned_data


class MealPickForm(forms.Form):
    categories = forms.ModelChoiceField(queryset=Category.objects.all(), required=True, initial=1)
    meals = forms.ModelChoiceField(queryset=Meal.objects.filter(category=1), initial=0)
    comment = forms.CharField(widget=forms.Textarea(attrs={'cols':45, 'rows':2, 'style':'resize:none;'}), required=False)