from django import forms
from django.forms import ModelForm, PasswordInput

# import Models from models.py
from .models import Server, Project, Profile

# create a forms.Form
class ServerForm(forms.ModelForm):
# specify the name of model to use
#     password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Server
        fields = "__all__"
        # widgets = {
        #     'password': PasswordInput(),
        # }

        # exclude = ('key',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            self.fields['online'].widget.attrs.update({'class': 'form-control col-sm-1'})
            self.fields['key'].widget.attrs.update({'readonly': 'readonly'})
            # self.fields['password'].widget.attrs.update({'readonly': 'readonly'})


# class ServerAdminForm(forms.ModelForm):
# # specify the name of model to use
#     class Meta:
#         model = Server
#         widgets = {
#             'key': ,
#         }
#         fields = "__all__"


# class ServerForm(forms.Form):
#     cpu = forms.CharField(label='CPU', max_length=150)
#     ram = forms.IntegerField(label='RAM', required=False)
#     storage = forms.IntegerField(label='Storage')
#     private_ip = forms.GenericIPAddressField(label='Private IP', required=False)
#     public_ip = forms.GenericIPAddressField(label='Public IP', required=False)
#     type = forms.CharField(label='Type', max_length=150, required=False)
#     platform_hosted = forms.CharField(label='Platform hosted On', max_length=150, required=False)
#     owner = forms.CharField(label='Owner', max_length=150, required=False)
#     storage_type = forms.CharField(label='Storage Type', max_length=150, required=False)


# create a ModelForm
class ProjectForm(forms.ModelForm):
# specify the name of model to use
    class Meta:
        model = Project
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class ProfileForm(forms.ModelForm):
# specify the name of model to use
    class Meta:
        model = Profile
        fields = "__all__"
