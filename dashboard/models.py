from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import redirect
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
from univv.utils import unique_slug_generator 
from user.models import Staff
from django.utils import timezone


# the level class <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

class Niveau(models.Model):
    Nv = models.CharField(max_length=30)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.Nv

    class Meta:
        db_table = "Niveau"




# the teacher class <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

class Enseignant(models.Model):
    email = models.EmailField(max_length=254, primary_key=True)
    slug = models.SlugField(unique=True)
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    grade = models.CharField(max_length=30)
    tel = models.PositiveIntegerField(unique=True)
    active = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.prenom} {self.nom}'

    def get_absolute_url(self):
        return redirect("all_teachers")

    class Meta:
        db_table = "Enseignant"


def pre_save_enseignant_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_enseignant_receiver, sender=Enseignant)   

# class module <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
UNITES = [('1', 'Fondamentale'), ('2', 'Methodologie')]

class Module(models.Model):
    operateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modules')
    code = models.CharField(max_length=30, primary_key=True)
    slug = models.SlugField(unique=True)
    designation = models.CharField(max_length=40)
    unite = models.CharField(max_length=40, choices=UNITES)
    credit = models.PositiveIntegerField()
    coeff = models.PositiveIntegerField()
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name='nivaux')
    prof = models.ForeignKey(Enseignant, on_delete=models.CASCADE, related_name='profs')
    active = models.BooleanField(default=False)
    semestre = models.CharField(max_length=10) 

    cours = models.PositiveSmallIntegerField()
    td = models.PositiveSmallIntegerField()
    tp = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.designation
    
    class Meta:
        ordering = ['-niveau']
        db_table = "module"
    

#create a complete slug for module
def create_module_slug(instance, new_slug=None):
    slug = slugify(instance.designation)
    if new_slug is not None:
        slug = new_slug

    qs_exists = Module.objects.filter(slug=slug).exists()
    if not qs_exists:
        return slug
    else:
        new_slug = "{}-{}".format(slug, instance.code)
        return create_module_slug(instance, new_slug=new_slug)    

def pre_save_module_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_module_slug(instance)

pre_save.connect(pre_save_module_receiver, sender=Module)      

# class Salle <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
CHOICES =  [('TP', 'TP'), ('TD', 'TD'), ('Amphi', 'Amphi')]
BLOCKS = [('1', 'Bloc 30Salles'), ('2', 'Bloc 22Salles')]
class Salle(models.Model):
    enseignants = models.ForeignKey(Enseignant, on_delete=models.DO_NOTHING)
    bloc = models.CharField(max_length=30, choices=BLOCKS)
    design = models.CharField(max_length=20)
    type_of = models.CharField(max_length=10, choices=CHOICES)
    active = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.design

    class Meta:
        db_table = "salle"


# timetable classes <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# TYPE_OF_GROUP = ("TP", "TD")
class Periode (models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='modules')
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE, related_name='enseignants')
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE, related_name='salles')
    groupe = models.CharField(max_length=10, blank=True, null=True) 
    groupe_type = models.CharField(max_length=10, blank=True, null=True)
    
class EmploiTemps(models.Model):

    first_first = models.ManyToManyField(Periode, blank=True,  related_name='peride_one')
    first_second = models.ManyToManyField(Periode, blank=True, related_name='perides_two')
    first_third = models.ManyToManyField(Periode, blank=True, related_name='perides_three')
    first_forth = models.ManyToManyField(Periode, blank=True, related_name='perides_four')

    second_first = models.ManyToManyField(Periode, blank=True, related_name='peride_five')
    second_second = models.ManyToManyField(Periode, blank=True,  related_name='perides_six')
    second_third = models.ManyToManyField(Periode, blank=True,  related_name='perides_seven')
    second_forth = models.ManyToManyField(Periode, blank=True,  related_name='perides_eight')
    
    third_first = models.ManyToManyField(Periode, blank=True,  related_name='perides_nine')
    third_second = models.ManyToManyField(Periode, blank=True,  related_name='perides_ten')
    third_third = models.ManyToManyField(Periode, blank=True,  related_name='perides_eleven')
    third_forth = models.ManyToManyField(Periode, blank=True,  related_name='perides_twelve')
    
    forth_first = models.ManyToManyField(Periode, blank=True,  related_name='perides_thirteen')
    forth_second = models.ManyToManyField(Periode, blank=True,  related_name='perides_fourteen')
    forth_third = models.ManyToManyField(Periode, blank=True,  related_name='perides_fifteen')
    forth_forth = models.ManyToManyField(Periode, blank=True,  related_name='perides_sixteen')
    
    fifth_first = models.ManyToManyField(Periode, blank=True,  related_name='perides_seventeen')
    fifth_second = models.ManyToManyField(Periode, blank=True,  related_name='perides_eighteen')
    fifth_third = models.ManyToManyField(Periode, blank=True,  related_name='perides_nineteen')
    fifth_forth = models.ManyToManyField(Periode, blank=True,  related_name='perides_twenty')

    level = models.ForeignKey(Niveau, on_delete = models.CASCADE)
    semestree = models.CharField(max_length=10)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(default=timezone.now)
    apdated_time = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.slug

    class Meta:
        db_table = "emploiTemps"
        

def create_slug_emp(instance):
    slug = slugify(instance.level) + "-" + instance.semestree
    return slug

def pre_save_emp_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug_emp(instance)

pre_save.connect(pre_save_emp_receiver, sender=EmploiTemps)     
    

#Canvas for Emploi <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# class CanvasTimeTable (models.Model):
#     modules = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='canvas')
#     semestre = models.CharField(max_length=10)
#     cours = models.PositiveSmallIntegerField()
#     td = models.PositiveSmallIntegerField()
#     tp = models.PositiveSmallIntegerField()
#     niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
#     slug = models.SlugField()
#     active = models.BooleanField(default=True)


#     def __str__(self):
#         return self.slug
    
#     class Meta:
#         db_table = "canvasTimeTable"


# def create_Canvas_slug(instance, new_slug=None):

#     slug = "{}-{}".format(instance.niveau, instance.semestre)
#     return slug

# def pre_save_canvas_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = create_Canvas_slug(instance) 

# pre_save.connect(pre_save_canvas_receiver, sender=CanvasTimeTable)    


# Material class <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

class Material(models.Model):
    name = models.CharField(max_length=10, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to="Materil_pic", default="default.jpg")
    salles = models.ForeignKey(Salle, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name
    


    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url
       


class Order(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="staff")
    ordering_date = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="orders")
    returned = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    retering_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.staff.user.username



# chrge horaire class <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
class Science(models.Model):
    nature = models.CharField(max_length=20, choices=CHOICES)
    groupe = models.CharField(max_length=3, blank=True)
    occupe = models.BooleanField(default=False)


    


SEMESTRES = [('S1', 'S1'), ('S2', 'S2'), ('S3', 'S3'),('S4', 'S4'), ('S5', 'S5'), ('S6', 'S6'), ('M1', 'M1'), ('M2', 'M2')]

class ChargeHoraire(models.Model):
    enseignant = models.OneToOneField(Enseignant, on_delete=models.CASCADE)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    semestre = models.CharField(max_length=20, choices=SEMESTRES)
    active = models.BooleanField(default=True) 

    science1_J1 = models.ForeignKey(Science, on_delete=models.DO_NOTHING, related_name="science1_J1", blank=True, null=True)
    science2_J1 = models.ForeignKey(Science, on_delete=models.DO_NOTHING, related_name="science2_J1", blank=True, null=True)
    science3_J1 = models.ForeignKey(Science, on_delete=models.DO_NOTHING, related_name="science3_J1", blank=True, null=True)
    science4_J1 = models.ForeignKey(Science, on_delete=models.DO_NOTHING, related_name="science4_J1", blank=True, null=True)

    science1_J2 = models.ForeignKey(Science, on_delete=models.DO_NOTHING, related_name="science1_J2", blank=True, null=True)
    science2_J2 = models.ForeignKey(Science, on_delete=models.DO_NOTHING, related_name="science2_J2", blank=True, null=True)
    science3_J2 = models.ForeignKey(Science, on_delete=models.DO_NOTHING, related_name="science3_J2", blank=True, null=True)
    science4_J2 = models.ForeignKey(Science, on_delete=models.DO_NOTHING, related_name="science4_J2", blank=True, null=True)

    science1_J3 = models.ForeignKey(Science, on_delete=models.DO_NOTHING, related_name="science1_J3", blank=True, null=True)
    science2_J3 = models.ForeignKey(Science, on_delete=models.DO_NOTHING, related_name="science2_J3", blank=True, null=True)
    science3_J3 = models.ForeignKey(Science, on_delete=models.DO_NOTHING, related_name="science3_J3", blank=True, null=True)
    science4_J3 = models.ForeignKey(Science, on_delete=models.DO_NOTHING, related_name="science4_J3", blank=True, null=True)

    science1_J4 = models.ForeignKey(Science, on_delete=models.DO_NOTHING, related_name="science1_J4", blank=True, null=True)
    science2_J4 = models.ForeignKey(Science, on_delete=models.DO_NOTHING, related_name="science2_J4", blank=True, null=True)
    science3_J4 = models.ForeignKey(Science, on_delete=models.DO_NOTHING, related_name="science3_J4", blank=True, null=True)
    science4_J4 = models.ForeignKey(Science, on_delete=models.DO_NOTHING, related_name="science4_J4", blank=True, null=True)

    science1_J5 = models.ForeignKey(Science, on_delete=models.DO_NOTHING, related_name="science1_J5", blank=True, null=True)
    science2_J5 = models.ForeignKey(Science, on_delete=models.DO_NOTHING, related_name="science2_J5", blank=True, null=True)
    science3_J5 = models.ForeignKey(Science, on_delete=models.DO_NOTHING, related_name="science3_J5", blank=True, null=True)
    science4_J5 = models.ForeignKey(Science, on_delete=models.DO_NOTHING, related_name="science4_J5", blank=True, null=True)

    science5_J1 = models.ForeignKey(Science, on_delete=models.DO_NOTHING, related_name="science5_J1", blank=True, null=True)
    science5_J2 = models.ForeignKey(Science, on_delete=models.DO_NOTHING, related_name="science5_J2", blank=True, null=True)
    science5_J3 = models.ForeignKey(Science, on_delete=models.DO_NOTHING, related_name="science5_J3", blank=True, null=True)
    science5_J4 = models.ForeignKey(Science, on_delete=models.DO_NOTHING, related_name="science5_J4", blank=True, null=True)
    science5_J5 = models.ForeignKey(Science, on_delete=models.DO_NOTHING, related_name="science5_J5", blank=True, null=True)



    def __str__(self):
        return self.enseignant.nom
    
