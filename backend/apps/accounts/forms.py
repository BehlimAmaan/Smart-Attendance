from django import forms
from .models import User


class AdminTeacherCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "role")

    def clean_role(self):
        role = self.cleaned_data.get("role")
        if role != "TEACHER":
            raise forms.ValidationError("Only TEACHER accounts can be created")
        return role
