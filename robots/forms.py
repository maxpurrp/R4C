from django import forms


class RobotForm(forms.Form):
    serial = forms.CharField(max_length=5)
    model = forms.CharField(max_length=2)
    version = forms.CharField(max_length=2)
    created = forms.DateTimeField()
