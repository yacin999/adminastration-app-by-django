from .models import Enseignant, Module, Salle, CanvasTimeTable, Niveau, EmploiTemps
from django import forms
from django.core.validators import MinValueValidator

CHOICES =  [('1', 'TP'), ('2', 'TD'), ('3', 'Amphi')]
SEMESTRES = [('1', 'S1'), ('2', 'S2'), ('3', 'S3'),('4', 'S4'), ('5', 'S5'), ('6', 'S6'), ('7', 'M1'), ('8', 'M2')]



class EnseignantModelForm(forms.ModelForm):
    # tel = forms.IntegerField(validators=[MinValueValidator(0)])
    class Meta:
        model = Enseignant
        fields = ['email', 'nom', 'prenom', 'grade', 'tel']
        widgets = {
            'email' : forms.EmailInput(attrs={'class': 'module-input', 'placeholder': 'email'}),
            'nom' : forms.TextInput(attrs={'class': 'module-input', 'placeholder': 'nom'}),
            'prenom' : forms.TextInput(attrs={'class': 'module-input', 'placeholder': 'prenom'}),
            'grade' : forms.TextInput(attrs={'class': 'module-input', 'placeholder': 'grade'}),
            'tel' : forms.NumberInput(attrs={'class': 'module-input', 'placeholder': 'numero de telephone'}),
        }


class ModuleModelForm(forms.ModelForm):
    designation = forms.CharField(label='nom de module',  widget=forms.TextInput(attrs={"class": "module-input", "placeholder": "designation"}))
    semestre = forms.ChoiceField(label="semestre", widget=forms.Select(attrs={"class": "module-select-input", "placeholder": "semestre"}), choices=SEMESTRES)
    prof = forms.ModelChoiceField(queryset=Enseignant.objects.all(), empty_label=None, label="prof", widget=forms.Select(attrs={"class": "module-select-input", "placeholder": "prof"}), to_field_name="nom")
    niveau = forms.ModelChoiceField(queryset=Niveau.objects.all(), empty_label=None, label="niveau", widget=forms.Select(attrs={"class": "module-select-input", "placeholder": "niveau"}))
    class Meta:
        model = Module
        fields = fields = ['code', 'designation', 'unite', 'credit', 'coeff', 'niveau', 'semestre', 'prof']
        widgets = {
            "code": forms.TextInput(attrs={"class": "module-input", "placeholder": "code"}),
            "unite": forms.TextInput(attrs={"class": "module-input", "placeholder": "unite"}),
            "coeff": forms.NumberInput(attrs={"class": "module-input", "placeholder": "coeff"}),
            "niveau": forms.Select(attrs={"class": "module-select-input", "placeholder": "niveau"}),
            "credit": forms.NumberInput(attrs={"class": "module-input", "placeholder": "credit"}),
            "prof": forms.Select(attrs={"class": "module-select-input", "placeholder": "prof"}),
        }

    def clean_designation(self, *args, **kwargs):
        name = self.cleaned_data['designation']
        all_modules = Module.objects.all()

        for module in all_modules:
            if name == module.designation:
                raise forms.ValidationError("this module already exists !!")
        return name




class SalleModelForm(forms.ModelForm):
    design = forms.CharField(label='nom de class', widget=forms.TextInput(attrs={
        'placeholder':'nom de class',
        'class': 'module-input', 
    }))
    typeS = forms.ChoiceField(label= "select type of classroom", choices=CHOICES, widget=forms.RadioSelect(attrs={
        "class": "bullets-style",
        }))
    bloc = forms.CharField(widget=forms.TextInput(attrs={
        "class": "module-input", 
        "placeholder": "bloc"
        }))
    class Meta:
        model = Salle
        fields = ['bloc', 'design', 'typeS']

    def clean_design(self, *args, **kwargs):
        pre_names = Salle.objects.all()
        name = self.cleaned_data.get('design')

        for pre_name in pre_names:
            if name == pre_name.design:
                raise forms.ValidationError("this name already exists")
        

        return name



# class CanvasTimetableForm(forms.ModelForm):
#     modules = forms.ModelChoiceField(queryset=Module.objects.filter(active=False))
#     semestre = forms.ChoiceField(widget=forms.Select, choices=CHOICES2)
#     niveau = forms.ModelChoiceField(queryset=Niveau.objects.all())

#     class Meta:
#         model = CanvasTimeTable
#         fields = ['niveau', 'semestre', 'modules', 'cours', 'td', 'tp']
#         widgets = {
#             'modules': forms.Select(attrs={'clsss': 'form-control'}),
#             'semestre': forms.TextInput(attrs={'clsss': 'form-control'}),
#             'cours': forms.NumberInput(attrs={'clsss': 'form-control'}),
#             'td': forms.NumberInput(attrs={'clsss': 'form-control'}),
#             'tp': forms.NumberInput(attrs={'clsss': 'form-control'}),
#             'niveau': forms.Select(attrs={'clsss': 'form-control'})
#         }
        

