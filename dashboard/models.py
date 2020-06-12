from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import redirect
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
from univv.utils import unique_slug_generator 


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
    password = models.CharField(max_length=100, blank=True)
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

class Module(models.Model):
    operateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modules')
    code = models.CharField(max_length=30, primary_key=True)
    slug = models.SlugField(unique=True)
    designation = models.CharField(max_length=40)
    unite = models.CharField(max_length=40)
    credit = models.PositiveIntegerField()
    coeff = models.PositiveIntegerField()
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name='nivaux')
    prof = models.ForeignKey(Enseignant, on_delete=models.CASCADE, related_name='profs')
    active = models.BooleanField(default=False)
    semestre = models.CharField(max_length=10) 

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

class Salle(models.Model):
    enseignants = models.ManyToManyField(Enseignant)
    opr = models.ForeignKey(User, on_delete=models.CASCADE)
    bloc = models.CharField(max_length=30)
    design = models.CharField(max_length=20)
    type_of = models.CharField(max_length=10)
    active = models.BooleanField(default=False)

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
    #canvas = models.ForeignKey(CanvasTimeTable, on_delete=models.PROTECT, related_name='emplois')
    
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

class CanvasTimeTable (models.Model):
    modules = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='canvas')
    semestre = models.CharField(max_length=10)
    cours = models.PositiveSmallIntegerField()
    td = models.PositiveSmallIntegerField()
    tp = models.PositiveSmallIntegerField()
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    slug = models.SlugField()


    def __str__(self):
        return self.slug
    
    class Meta:
        db_table = "canvasTimeTable"


def create_Canvas_slug(instance, new_slug=None):

    slug = "{}-{}".format(instance.niveau, instance.semestre)
    return slug

def pre_save_canvas_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_Canvas_slug(instance) 

pre_save.connect(pre_save_canvas_receiver, sender=CanvasTimeTable)    




