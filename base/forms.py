from .models import *
from django import forms
from django.forms.widgets import DateInput, Select 

class RepairRequestForm(forms.ModelForm):

    class Meta:
        model = RepairRequest
        fields = ['first_name', 'department', 'office', 'description']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input your name ...', 'style': 'margin-bottom: 10px'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input the details about the problems ..'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'office': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Requested By',
            'last_name': '',
            'description': 'Description',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'department' in self.data:
            self.fields['office'].queryset = Office.objects.filter(department_id=self.data['department'])
        elif self.instance.pk:
            self.fields['office'].queryset = self.instance.department.office_set.all()
            
class StaffForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        # self.fields['staff'].widget = forms.RadioSelect()
        self.fields['staff'].queryset = User.objects.filter(groups__name='staff')

    class Meta:
        model = RepairRequest
        fields = ['staff']

        widgets = {
            'staff': Select(attrs={'class': 'form-control'}),
        }

class RepairRequestInfoForm(forms.ModelForm):

    class Meta:
        model = RepairRequest
        fields = ['equip_type', 'property_num', 'serial_num', 'kind_of_work', 'description_staff']

        widgets = {
            'equip_type': Select(attrs={'class': 'form-control'}),
            'property_num': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'serial_num': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'kind_of_work': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'description_staff': forms.CheckboxSelectMultiple()
        }

        labels = {
            'equip_type': 'Equioment Type',
            'property_num': 'Property Number',
            'serial_num': 'Serial Number',
            'description_staff': 'Description'
        }

class StatusForm(forms.ModelForm):

    class Meta:
        model = RepairRequest
        fields = ['status']

        widgets = {
            'status': Select(attrs={'class': 'form-control'}),
        }

# Add user______________________________________________
from django.contrib.auth.forms import UserCreationForm

class AddUserForm(UserCreationForm):

    ROLES = (
        ('','Select a role'),
        ('staff', 'Staff'),
        ('controller', 'Controller'),
    )
    role = forms.ChoiceField(choices=ROLES)

    class Meta:
        model = User 
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            role = self.cleaned_data.get('role')
        
            try:
                group = Group.objects.get(name=role)
                user.groups.add(group)
            except Group.DoesNotExist:
                user.delete()
                raise forms.ValidationError('Invalid role. Please select a valid role.')

        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'First name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last name'})
        # self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'your number'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Re-type password'})
        self.fields['role'].widget.attrs.update({'class': 'form-control'})

        self.fields['username'].error_messages['unique'] = 'This username is already taken. Please choose a different one.'