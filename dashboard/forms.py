from .models import Enseignant, Module, Salle, CanvasTimeTable, Niveau, EmploiTemps
from django import forms
from django.core.validators import MinValueValidator

CHOICES =  [('1', 'TP'), ('2', 'TD'), ('3', 'amphi')]
SEMESTRES = [('1', 'S1'), ('2', 'S2'), ('3', 'S3'), ('4', 'M1'), ('5', 'M2')]



class EnseignantModelForm(forms.ModelForm):
    # tel = forms.IntegerField(validators=[MinValueValidator(0)])
    class Meta:
        model = Enseignant
        fields = ['email', 'nom', 'prenom', 'grade', 'tel']


class ModuleModelForm(forms.ModelForm):
    designation = forms.CharField(label='nom de module')
    semestre = forms.ChoiceField(widget=forms.Select, choices=SEMESTRES)
    class Meta:
        model = Module
        fields = fields = ['code', 'designation', 'unite', 'credit', 'coeff', 'niveau', 'semestre', 'prof']

    def clean_designation(self, *args, **kwargs):
        name = self.cleaned_data['designation']
        all_modules = Module.objects.all()

        for module in all_modules:
            if name == module.designation:
                raise forms.ValidationError("this module already exists !!")
        return name




class SalleModelForm(forms.ModelForm):
    design = forms.CharField(label='nom de class', widget=forms.TextInput(attrs={
        'style': 'width: 300px'
    }))
    typeS = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
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
        

