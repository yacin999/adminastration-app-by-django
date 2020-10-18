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
    DEPARTMENT = [("1", "informatique"), ("2", "mathématique"), ('3', "autre")]


    email = models.EmailField(max_length=254, primary_key=True)
    slug = models.SlugField(unique=True)
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    grade = models.CharField(max_length=30)
    tel = models.PositiveIntegerField(unique=True)
    departement = models.CharField(max_length=30, choices=DEPARTMENT)
    active = models.BooleanField(default=False)



    def save(self, *args, **kwargs):

        exist_dep = Enseignant.objects.filter(departement=self.departement).exists()

        if not exist_dep :
            new_dep = ("{}".format(self.departement), "{}".format(self.departement))
            self.DEPARTMENT.insert(0, new_dep)
        super().save(*args, **kwargs)

    
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
SEMESTRES = [('1', 'S1'), ('2', 'S2'), ('3', 'S3'),('4', 'S4'), ('5', 'S5'), ('6', 'S6'), ('7', 'M1'), ('8', 'M2'), ('9', 'M3'), ('10', 'M4')]

class Module(models.Model):

    operateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modules')
    code = models.CharField(max_length=30, primary_key=True)
    slug = models.SlugField(unique=True)
    designation = models.CharField(max_length=40)
    unite = models.CharField(max_length=40, choices=UNITES)
    credit = models.PositiveIntegerField()
    coeff = models.PositiveIntegerField()
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name='nivaux')
    active = models.BooleanField(default=False)
    semestre = models.CharField(max_length=10, choices=SEMESTRES) 
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
CHOICES =  [('1', 'TP'), ('2', 'TD'), ('3', 'Cours')]
BLOCKS = [('1', 'Bloc 30Salles'), ('2', 'Bloc 22Salles')]
class Salle(models.Model):
    
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
    group_number = models.PositiveSmallIntegerField(default=1)
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
    


# Material class <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

class Material(models.Model):
    name = models.CharField(max_length=10, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    salles = models.ForeignKey(Salle, on_delete=models.CASCADE, default=None, null=True)

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


SEMESTRES = [('S1', 'S1'), ('S2', 'S2'), ('S3', 'S3'),('S4', 'S4'), ('S5', 'S5'), ('S6', 'S6'), ('M1', 'M1'), ('M2', 'M2')]
