from DjangoApp.models import User, Task, Team
from django import forms


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('task_name', 'task_description', 'end_date', 'user')

class LoginForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()


class PersonalAreaForm(forms.Form):
    ROLE_CHOICES = [
        ('עובד', 'עובד'),
        ('מנהל', 'מנהל'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, label="תפקיד")

    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        label="קבוצה",
        empty_label="בחר קבוצה"
    )