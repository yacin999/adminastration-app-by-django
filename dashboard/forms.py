from .models import Enseignant, Module, Salle, Niveau, EmploiTemps, Material
from user.models import Staff, StaffPermission
from django import forms
from django.core.validators import MinValueValidator

CHOICES =  [('1', 'TP'), ('2', 'TD'), ('3', 'Cours')]
SEMESTRES = [('1', 'S1'), ('2', 'S2'), ('3', 'S3'),('4', 'S4'), ('5', 'S5'), ('6', 'S6'), ('7', 'M1'), ('8', 'M2'), ('9', 'M3'), ('10', 'M4')]
UNITES = [('1', 'Fondamentale'), ('2', 'Methodologie')]
BLOCKS = [('1', 'Bloc 30Salles'), ('2', 'Bloc 22Salles')]
DEPARTMENT = [("1", "informatique"), ("2", "mathématique"), ('3', "autre")]





    

class EnseignantModelForm(forms.ModelForm):

    dep_list = []
    ens = {}
    el = {}
    for ens in Enseignant.objects.all():
        dep_list.append(ens.get_departement_display())

    new_dep_list = list(set(dep_list))
    for el in new_dep_list:
        if el not in DEPARTMENT:
            DEPARTMENT.insert(0, ("{}".format(el), "{}".format(el)))
    
    # tel = forms.IntegerField(validators=[MinValueValidator(0)])
    departement = forms.ChoiceField(label="departement" ,choices=DEPARTMENT, widget=forms.Select(attrs={"class": "teacher-input", "id": "department"}))
    departement2 = forms.CharField(label="departement2" ,widget=forms.TextInput(attrs={"class": "teacher-input", 'placeholder': 'ajouter department', "id": "department2", "hidden": "true"}))
    class Meta:
        model = Enseignant
        fields = ['email', 'nom', 'prenom', 'grade', 'tel', 'departement', 'departement2']
        widgets = {
            'email' : forms.EmailInput(attrs={'class': 'teacher-input', 'placeholder': 'email', 'id': 'email-teacher'}),
            'nom' : forms.TextInput(attrs={'class': 'teacher-input', 'placeholder': 'nom'}),
            'prenom' : forms.TextInput(attrs={'class': 'teacher-input', 'placeholder': 'prenom'}),
            'grade' : forms.TextInput(attrs={'class': 'teacher-input', 'placeholder': 'grade'}),
            'tel' : forms.NumberInput(attrs={'class': 'teacher-input', 'placeholder': 'numero de telephone', 'id': 'tel-teacher'}),
        }

        


class ModuleModelForm(forms.ModelForm):
    designation = forms.CharField(label='nom de module',  widget=forms.TextInput(attrs={"class": "module-input", "placeholder": "designation", "id": "designation-module"}))
    semestre = forms.ChoiceField(label="semestre", widget=forms.Select(attrs={"class": "module-select-input", "placeholder": "semestre"}), choices=SEMESTRES)
    niveau = forms.ModelChoiceField(queryset=Niveau.objects.all(), empty_label=None, label="niveau", widget=forms.Select(attrs={"class": "module-select-input", "placeholder": "niveau"}))
    unite = forms.ChoiceField(label="unite", widget=forms.Select(attrs={"class": "module-select-input", "placeholder": "unite"}), choices=UNITES)
    class Meta:
        model = Module
        fields = fields = ['code', 'designation', 'credit', 'coeff', 'cours', 'tp', 'td' , 'niveau', 'semestre', 'unite']
        widgets = {
            "code": forms.TextInput(attrs={"class": "module-input", "placeholder": "code", "id": "code-module"}),
            "unite": forms.Select(attrs={"class": "module-input", "placeholder": "unite", "id": "unite-module"}),
            "coeff": forms.NumberInput(attrs={"class": "module-input", "placeholder": "coeff", "id": "coeff-module"}),
            "niveau": forms.Select(attrs={"class": "module-select-input", "placeholder": "niveau", "id": "niveau-module"}),
            "credit": forms.NumberInput(attrs={"class": "module-input", "placeholder": "credit", "id": "credit-module"}),
            "cours": forms.NumberInput(attrs={"class": "module-input", "placeholder": "cours", "id": "cours-module"}),
            "tp": forms.NumberInput(attrs={"class": "module-input", "placeholder": "tp", "id": "tp-module"}),
            "td": forms.NumberInput(attrs={"class": "module-input", "placeholder": "td", "id": "td-module"}),
        }

        def clean_designation(self, *args, **kwargs):
            name = self.cleaned_data['designation']
            all_modules = Module.objects.all()

            for module in all_modules:
                if name == module.designation:
                    raise forms.ValidationError("this module already exists !!")
            return name


class UpdateModuleModelForm(forms.ModelForm):
    designation = forms.CharField(label='nom de module',  widget=forms.TextInput(attrs={"class": "module-input", "placeholder": "designation", "id": "designation-module"}))
    semestre = forms.ChoiceField(label="semestre", widget=forms.Select(attrs={"class": "module-select-input", "placeholder": "semestre"}), choices=SEMESTRES)
    niveau = forms.ModelChoiceField(queryset=Niveau.objects.all(), empty_label=None, label="niveau", widget=forms.Select(attrs={"class": "module-select-input", "placeholder": "niveau"}))
    unite = forms.ChoiceField(label="unite", widget=forms.Select(attrs={"class": "module-select-input", "placeholder": "unite"}), choices=UNITES)
    class Meta:
        model = Module
        fields = fields = ['designation', 'credit', 'coeff', 'cours', 'tp', 'td' , 'niveau', 'semestre', 'unite']
        widgets = {
            # "code": forms.TextInput(attrs={"class": "module-input", "placeholder": "code", "id": "code-module"}),
            "unite": forms.Select(attrs={"class": "module-input", "placeholder": "unite", "id": "unite-module"}),
            "coeff": forms.NumberInput(attrs={"class": "module-input", "placeholder": "coeff", "id": "coeff-module"}),
            "niveau": forms.Select(attrs={"class": "module-select-input", "placeholder": "niveau", "id": "niveau-module"}),
            "credit": forms.NumberInput(attrs={"class": "module-input", "placeholder": "credit", "id": "credit-module"}),
            "cours": forms.NumberInput(attrs={"class": "module-input", "placeholder": "cours", "id": "cours-module"}),
            "tp": forms.NumberInput(attrs={"class": "module-input", "placeholder": "tp", "id": "tp-module"}),
            "td": forms.NumberInput(attrs={"class": "module-input", "placeholder": "td", "id": "td-module"}),
        }

    




class SalleModelForm(forms.ModelForm):
    design = forms.CharField(label='nom de class', widget=forms.TextInput(attrs={
        'placeholder':'nom de class',
        'class': 'module-input', 
    }))
    type_of = forms.ChoiceField(label= "selectioner le type de cette salle",choices=CHOICES, widget=forms.Select(attrs={
        "class": "bullets-style",
        }))
    bloc = forms.ChoiceField(label= "selectioner le bloc de cette salle", choices=BLOCKS,  widget=forms.Select(attrs={
        "class": "module-input", 
        "placeholder": "bloc"
        }))
    class Meta:
        model = Salle
        fields = ['bloc', 'design', 'type_of']

    def clean_design(self, *args, **kwargs):
        pre_names = Salle.objects.all()
        name = self.cleaned_data.get('design')

        for pre_name in pre_names:
            if name == pre_name.design:
                raise forms.ValidationError("this classroom already exists")
        

        return name

class UpdateSalleModelForm(forms.ModelForm):
    design = forms.CharField(label='nom de class', widget=forms.TextInput(attrs={
        'placeholder':'nom de class',
        'class': 'module-input', 
    }))
    typeS = forms.ChoiceField(label= "selectioner le type de cette salle",choices=CHOICES, widget=forms.Select(attrs={
        "class": "bullets-style",
        }))
    bloc = forms.ChoiceField(label= "selectioner le bloc de cette salle", choices=BLOCKS,  widget=forms.Select(attrs={
        "class": "module-input", 
        "placeholder": "bloc"
        }))
    class Meta:
        model = Salle
        fields = ['bloc', 'design', 'typeS']

   

class MaterialModelForm(forms.ModelForm):
    
    class Meta:
        model = Material
        fields = ["name"]


        















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
        

