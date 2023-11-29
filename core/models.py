from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django import forms
from api.models import Department

class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s: %s" % (obj.application_type, obj.name)


class User(AbstractUser):
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    middle_name = models.CharField(max_length=30, blank=True)
    email = models.CharField(max_length=100, blank=False, unique=True)
    phone_number = PhoneNumberField(null=False,
                                    blank=False,
                                    unique=True,
                                    default="")
    username = models.CharField(max_length=30, blank=False, unique=True)
    department = models.ForeignKey("api.Department",
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True)
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'phone_number']


class MyUserAdminForm(forms.ModelForm):
    department = CustomModelChoiceField(queryset=Department.objects.all())

    class Meta:
        model = User
        fields = '__all__'

    # def save(self, commit=True):
    #     user = super(MyUserAdminForm, self).save(commit=False)
    #     check = user.check_password(self.cleaned_data["password"])
    #     print('lorem', check)
    #     user.set_password(self.cleaned_data["password"])
    #     if commit:
    #         user.save()
    #     return user
