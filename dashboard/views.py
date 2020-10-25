from django.shortcuts import get_object_or_404, redirect, render
from .models import Enseignant, Module, Salle, EmploiTemps, Periode, Niveau, Material, Order
from user.models import Staff, StaffPermission
from django.views.generic import CreateView
from .forms import EnseignantModelForm, ModuleModelForm, SalleModelForm, MaterialModelForm, UpdateModuleModelForm, UpdateSalleModelForm
from user.forms import UserForm , StaffForm, UpdateUserForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from univv.utils import render_to_pdf
from django.core import serializers
import re
import random
import datetime
from re import sub
import json
from dashboard import forms






# global variables ""_"" ""_"" ""_"" ""_"" ""_"" ""_"" ""_"" ""_"" ""_"" ""_"" ""_"" ""_"" ""_"" ""_"" ""_""
timetable_atts = ('first_first', 'first_second', 'first_third', 'first_forth', 'second_first', 'second_second', 'second_third', 'second_forth', 'third_first', 'third_second', 'third_third', 'third_forth', 'forth_first', 'forth_second', 'forth_third', 'forth_forth', 'fifth_first', 'fifth_second', 'fifth_third', 'fifth_forth')  
day_converter = {
    "first_first" : "Dimanche",
    "first_second" : "Dimanche",
    "first_third" : "Dimanche",
    "first_forth" : "Dimanche",

    "second_first" : "Lundi",
    "second_second" : "Lundi",
    "second_third" : "Lundi",
    "second_forth" : "Lundi",

    "third_first" : "Mardi",
    "third_second" : "Mardi",
    "third_third" : "Mardi",
    "third_forth" : "Mardi",

    "forth_first" : "Mercredi",
    "forth_second" : "Mercredi",
    "forth_third" : "Mercredi",
    "forth_forth" : "Mercredi",

    "fifth_first" : "Jeudi",
    "fifth_second" : "Jeudi",
    "fifth_third" : "Jeudi",
    "fifth_forth" : "Jeudi",
}
hour_converter = {
    "first_first" : "08h30 - 10h00",
    "first_second" : "10h15 - 11h45",
    "first_third" : "13h30 - 15h00",
    "first_forth" : "15h00 - 16h30",

    "second_first" : "08h30 - 10h00",
    "second_second" : "10h15 - 11h45",
    "second_third" : "13h30 - 15h00",
    "second_forth" : "15h00 - 16h30",

    "third_first" : "08h30 - 10h00",
    "third_second" : "10h15 - 11h45",
    "third_third" : "13h30 - 15h00",
    "third_forth" : "15h00 - 16h30",

    "forth_first" : "08h30 - 10h00",
    "forth_second" : "10h15 - 11h45",
    "forth_third" : "13h30 - 15h00",
    "forth_forth" : "15h00 - 16h30",

    "fifth_first" : "08h30 - 10h00",
    "fifth_second" : "10h15 - 11h45",
    "fifth_third" : "13h30 - 15h00",
    "fifth_forth" : "15h00 - 16h30",
}





# def findWholeWord(w):

#         return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

#         p = sub.Popen(('sudo', 'tcpdump', '-l', '-s 0', '-vvv', '-n', '((udp port 67) and (udp[8:1] = 0x1))'), stdout=sub.PIPE)
#         for row in iter(p.stdout.readline, b''):
#             if findWholeWord('requested-ip')(row):
#                 print(row.split(' ')[-1])
#                 print('mac_______address')
#             elif findWholeWord('client-id')(row):
#                 print(row.split(' ')[-1])



# if the user doesn's have this permission then
    #  this function will prevent him to access this page
def give_permission(request, user_permission):

    permissions = request.user.staff.permissions.all()
    
    if(not request.user.is_superuser):
        is_staf = False
        for perm in permissions:
            if (perm.name == user_permission):
                is_staf = True
    else:
        is_staf = True

    return is_staf





@login_required(login_url='login')
def panel(reqeust):

    users = Staff.objects.filter(accepted=False)
    
    context = {
        "plain_user": users,
    }

    return render(reqeust, 'dashboard/admin_panel.html',context)


# get all teachers and modules and classrooms ========================================================================
@login_required(login_url='login')
def all_ens(request):
    notif_user = Staff.objects.filter(accepted=False)
    is_staf = give_permission(request, "peut_lister_toutes_enseignants")
    if not is_staf:
     
        return redirect("admin_panel")

    teacher = Enseignant.objects.filter(active=False)
    context = {
        'title': 'les enseignants',
        'teachers' : teacher,
        'plain_user': notif_user
    }

    return render(request, 'dashboard/all_teachers.html', context)

@login_required(login_url='login')
def all_modules(request):
    notif_user = Staff.objects.filter(accepted=False)
    is_staf = give_permission(request, "peut_lister_toutes_modules")
    if not is_staf:
        return redirect("admin_panel")

    module = Module.objects.filter(active=False)
    context = {
        'title': 'les modules',
        'modules' : module, 
        'plain_user': notif_user
    }

    return render(request, 'dashboard/all_modules.html', context)

@login_required(login_url='login')
def all_classrooms(request):
    notif_user = Staff.objects.filter(accepted=False)
    is_staf = give_permission(request, "peut_lister_toutes_salles")
    if not is_staf:
        return redirect("admin_panel")


    model = Salle.objects.filter(active=False)
    template_name = 'dashboard/all_classrooms.html'
    context = {
        'title': 'all classrooms',
        'salles': model,
        'plain_user': notif_user
    }

    return render(request, template_name, context)

@login_required(login_url='login')
def all_timetables(request):
    notif_user = Staff.objects.filter(accepted=False)
    is_staf = give_permission(request, "peut_lister_toutes_emploitems")
    if not is_staf:
        return redirect("admin_panel")


    model = EmploiTemps.objects.all()
    context = {
        'title': 'all timetibles',
        'emploitemps': model,
        'plain_user': notif_user
    }

    return render(request, 'dashboard/all_emploitems.html', context)



@login_required(login_url='login')
def all_material(request):
    notif_user = Staff.objects.filter(accepted=False)
    is_staf = give_permission(request, "peut_lister_toutes_materials")
    if not is_staf:
        return redirect("admin_panel")

    material = Material.objects.all()

    context = {
        'title': 'all material', 
        'material': material,
        'plain_user': notif_user
    }

    return render(request, "dashboard/all_material.html", context)

@login_required(login_url='login')
def all_orders(request):
    notif_user = Staff.objects.filter(accepted=False)
    is_staf = give_permission(request, "peut_lister_toutes_ordres")
    if not is_staf:
        return redirect("admin_panel")




    if request.user.is_staff:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(staff=request.user.staff)


    context = {
        'title': 'all orders', 
        'orders': orders,
        'plain_user': notif_user
    }

    return render(request, "dashboard/all_orders.html", context)

def all_staff(request):
    notif_user = Staff.objects.filter(accepted=False)
    is_staf = give_permission(request, "peut_lister_toutes_staff")
    if not is_staf:
        return redirect("admin_panel")

    staff = Staff.objects.filter(active=True)

    context = {
        'title': 'all staff', 
        'staff': staff,
        'plain_user': notif_user
    }

    return render(request, "dashboard/all_staff.html", context)




#_____________________CREATE VIEWS ______________________________________________________________________________
@login_required(login_url='login')
def new_teacher(request):
    notif_user = Staff.objects.filter(accepted=False)
    is_staf = give_permission(request, "peut_créer_du_enseignant")
    if not is_staf:
        return redirect("admin_panel")


    if request.method == 'POST':
        form = EnseignantModelForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.departement = form.cleaned_data['departement2']
            new_form.save()

            return redirect("all_teachers")
    else:
            
        form = EnseignantModelForm()
    context = {
        'title': 'new teacher',
        'form': form,
        'plain_user': notif_user
    }
    return render(request, 'dashboard/new_teacher.html', context)

@login_required(login_url='login')
def new_module(request):
    notif_user = Staff.objects.filter(accepted=False)
    is_staf = give_permission(request, "peut_créer_du_module")
    if not is_staf:
        return redirect("admin_panel")


    if request.method == 'POST':
        form = ModuleModelForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.operateur = request.user
            new_form.save()
            return redirect("all_modules")
    else:
        form = ModuleModelForm()
    context = {
        'title': 'new Module',
        'form': form,
        'plain_user': notif_user
    }
    return render(request, 'dashboard/new_module.html', context)

@login_required(login_url='login')
def new_classroom(request):
    notif_user = Staff.objects.filter(accepted=False)
    is_staf = give_permission(request, "peut_créer_du_salle")
    if not is_staf:

        return redirect("admin_panel")
        # return messages.error(request, "you can't access to this page ")
        

    if request.method == 'POST':
        form = SalleModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("all_classrooms")
    else:
        form = SalleModelForm()

    context = {
        'title': 'new classroom',
        'form': form,
        'plain_user': notif_user
    }
    return render(request, 'dashboard/new_classroom.html', context)




#_____________________DETAIL VIEWS ______________________________________________________________________________
@login_required(login_url='login')
def timetable_detail(request, id):
    notif_user = Staff.objects.filter(accepted=False)
    emploiTemp = EmploiTemps.objects.get(id=id)
    context = {
        'title': 'timetable-detail',
        'emploitemps': emploiTemp,
        'plain_user': notif_user
    }
    return render(request, 'dashboard/detail_timetable.html', context)


@login_required(login_url='login')
def hourlyLoad_teacher_detail(request, slug):
    chargehoraire = {}
    enseignant = get_object_or_404(Enseignant, slug=slug)
    periods = Periode.objects.filter(enseignant=enseignant)
    timetable = EmploiTemps.objects.all()


    print("length of attrs", len(timetable_atts))

    for tt in timetable:
        for atr in dir(tt):
            
            if atr in timetable_atts:

                per = getattr(tt, '{}'.format(atr))

                for p in per.all():
                    if p.enseignant.nom == enseignant.nom:
                        if  p.groupe != None:
                            chargehoraire['{}'.format(atr)] = {
                                "module": p.module.designation,
                                "groupe_type": p.groupe_type,
                                "groupe": p.groupe
                            }
                        else: 
                            chargehoraire['{}'.format(atr)] = {
                                "module": p.module.designation,
                                "groupe_type": p.groupe_type,
                                "groupe": ""
                            }


    notif_user = Staff.objects.filter(accepted=False)
    context = {
        'title': 'charge horaire pour enseignent',
        'chargehoraire': chargehoraire,
        'enseignant' : enseignant,
        'plain_user': notif_user
    }

    return render(request, "dashboard/detail_hourlyload_teacher.html", context)

@login_required(login_url='login')
def teacher_detail(request, tel):
    notif_user = Staff.objects.filter(accepted=False)
    teacher = get_object_or_404(Enseignant, tel=tel)

    context = {
        'title': ' enseignent',
        'teacher': teacher,
        'plain_user': notif_user
    }

    return render(request, "dashboard/detail_teacher.html", context)






@login_required(login_url='login')
def new_timetable(request):
    notif_user = Staff.objects.filter(accepted=False)
    is_staf = give_permission(request, "peut_créer_du_empoitemps")
    if not is_staf:
        return redirect("admin_panel")
        


    niveau = Niveau.objects.all()
    teachers = Enseignant.objects.all().values("nom").distinct().filter(active=False)
    name_of_modules = Module.objects.all().filter(active=False)
    classrooms = Salle.objects.all().values("design").distinct()

    context = {
        'title': 'creating timetables',
        'teachers': teachers,
        'modules': name_of_modules,
        'classrooms': classrooms,
        'niveau': niveau,
        'plain_user': notif_user
    }
    return render(request, 'dashboard/new_timetable.html', context)


@login_required(login_url='login')
def new_staff(request):
    notif_user = Staff.objects.filter(accepted=False)
    is_staf = give_permission(request, "peut_créer_du_staff")
    if not is_staf:
        return redirect("admin_panel")

    print("is this user staff !!! ", request.user.is_staff)

    if (request.method == 'POST'):
        userform = UserForm(request.POST)
        staffForm = StaffForm(request.POST)

        if userform.is_valid() and staffForm.is_valid():
            user = userform.save(commit=False)
            user.is_staff = True
            user.set_password(userform.cleaned_data["password1"])
            user.save()

            permissions = staffForm.cleaned_data["permissions"]
            u = User.objects.get(id=user.id)
            staff = Staff(user=u)
            staff.save()
            for perms in permissions:
                permission = StaffPermission.objects.get(id=perms.id)
                staff.permissions.add(permission)
            return redirect("all_staff")            
    else:
        userform = UserForm()
        staffForm = StaffForm()

    context = {
        'title': 'new staff',
        'userform': userform,
        'staff': staffForm,
        'plain_user': notif_user
    }
    
    return render(request, "dashboard/new_staff.html", context)


@login_required(login_url='login')
def new_material(request):
    notif_user = Staff.objects.filter(accepted=False)
    is_staf = give_permission(request, "peut_créer_du_material")
    if not is_staf:
        return redirect("admin_panel")


    if request.method == 'POST':
        form = MaterialModelForm(request.POST)
        if form.is_valid():

            form.save()
            return redirect("all-material")
    else:
        form = MaterialModelForm()
    context = {
        'title': 'new material',
        'form': form,
        'plain_user': notif_user
    }
    return render(request, 'dashboard/new_material.html', context)



# to save data in the database via the ajax object ---------------$$
import json
@login_required(login_url='login')
def save_data(request):

    ajax_data = {} 
    print("from the server side")
    # print(request.POST)

    if request.method == 'POST':
        loaded_data = json.loads(request.body)
        json_dict = loaded_data['our_data']
        level = Niveau.objects.get(Nv=loaded_data['level'])
        semestre = loaded_data['semestre']
        timetables = EmploiTemps(level=level, semestree=semestre)
        timetables.save()
        # print(json_dict['1']['type'])
        
        if('1' in json_dict and json_dict['1']['type'] == "TD-TP"):
            i = 0
            while i < len(json_dict['1'])-1:
                teacher = Enseignant.objects.filter(nom=json_dict['1']["{}".format(i)]['enseignant'])[0]
                modules = Module.objects.filter(designation=json_dict['1']["{}".format(i)]['module'])[0]
                classroom = Salle.objects.filter(design=json_dict['1']["{}".format(i)]['salle'])[0]
                group = json_dict['1']["{}".format(i)]['groupe']
                period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe=group, groupe_type=json_dict['1']["{}".format(i)]['type_of_group'])
                timetables.first_first.add(period)
                i = i+1
        elif '1' in json_dict and json_dict['1']['type'] == "Cours":
            teacher = Enseignant.objects.filter(nom=json_dict['1']['enseignant'])[0]
            modules = Module.objects.filter(designation=json_dict['1']['module'])[0]
            classroom = Salle.objects.filter(design=json_dict['1']['salle'])[0]
            period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe_type=json_dict['1']['type'])
            timetables.first_first.add(period)
                                    
        if('2' in json_dict and json_dict['2']['type'] == "TD-TP"):
            i = 0
            while i < len(json_dict['2'])-1:
                teacher = Enseignant.objects.filter(nom=json_dict['2']["{}".format(i)]['enseignant'])[0]
                modules = Module.objects.filter(designation=json_dict['2']["{}".format(i)]['module'])[0]
                classroom = Salle.objects.filter(design=json_dict['2']["{}".format(i)]['salle'])[0]
                group = json_dict['2']["{}".format(i)]['groupe']
                period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe=group, groupe_type=json_dict['2']["{}".format(i)]['type_of_group'])
                timetables.first_second.add(period)
                i = i+1
        elif '2' in json_dict and json_dict['2']['type'] == "Cours":
            teacher = Enseignant.objects.filter(nom=json_dict['2']['enseignant'])[0]
            modules = Module.objects.filter(designation=json_dict['2']['module'])[0]
            classroom = Salle.objects.filter(design=json_dict['2']['salle'])[0]
            period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe_type=json_dict['2']['type'])
            timetables.first_second.add(period)
        
        if('3' in json_dict and  json_dict['3']['type'] == "TD-TP"):
            i = 0
            while i < len(json_dict['3'])-1:
                teacher = Enseignant.objects.filter(nom=json_dict['3']["{}".format(i)]['enseignant'])[0]
                modules = Module.objects.filter(designation=json_dict['3']["{}".format(i)]['module'])[0]
                classroom = Salle.objects.filter(design=json_dict['3']["{}".format(i)]['salle'])[0]
                group = json_dict['3']["{}".format(i)]['groupe']
                period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe=group, groupe_type=json_dict['3']["{}".format(i)]['type_of_group'])            
                timetables.first_third.add(period)
                i = i+1
        elif '3' in json_dict and json_dict['3']['type'] == "Cours":
            teacher = Enseignant.objects.filter(nom=json_dict['3']['enseignant'])[0]
            modules = Module.objects.filter(designation=json_dict['3']['module'])[0]
            classroom = Salle.objects.filter(design=json_dict['3']['salle'])[0]
            period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe_type=json_dict['3']['type'])
            timetables.first_third.add(period)

        if('4' in json_dict and  json_dict['4']['type'] == "TD-TP"):
            i = 0
            while i < len(json_dict['4'])-1:
                teacher = Enseignant.objects.filter(nom=json_dict['4']["{}".format(i)]['enseignant'])[0]
                modules = Module.objects.filter(designation=json_dict['4']["{}".format(i)]['module'])[0]
                classroom = Salle.objects.filter(design=json_dict['4']["{}".format(i)]['salle'])[0]
                group = json_dict['4']["{}".format(i)]['groupe']
                period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe=group, groupe_type=json_dict['4']["{}".format(i)]['type_of_group'])            
                timetables.first_forth.add(period)
                i = i+1
        elif '4' in json_dict and json_dict['4']['type'] == "Cours":
            teacher = Enseignant.objects.filter(nom=json_dict['4']['enseignant'])[0]
            modules = Module.objects.filter(designation=json_dict['4']['module'])[0]
            classroom = Salle.objects.filter(design=json_dict['4']['salle'])[0]
            period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe_type=json_dict['4']['type'])
            timetables.first_forth.add(period)

        if('5' in json_dict and  json_dict['5']['type'] == "TD-TP"):
            i = 0
            while i < len(json_dict['5'])-1:
                teacher = Enseignant.objects.filter(nom=json_dict['5']["{}".format(i)]['enseignant'])[0]
                modules = Module.objects.filter(designation=json_dict['5']["{}".format(i)]['module'])[0]
                classroom = Salle.objects.filter(design=json_dict['5']["{}".format(i)]['salle'])[0]
                group = json_dict['5']["{}".format(i)]['groupe']
                period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe=group, groupe_type=json_dict['5']["{}".format(i)]['type_of_group'])            
                timetables.second_first.add(period)
                i = i+1
        elif '5' in json_dict and json_dict['5']['type'] == "Cours":
            teacher = Enseignant.objects.filter(nom=json_dict['5']['enseignant'])[0]
            modules = Module.objects.filter(designation=json_dict['5']['module'])[0]
            classroom = Salle.objects.filter(design=json_dict['5']['salle'])[0]
            period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe_type=json_dict['5']['type'])
            timetables.second_first.add(period)

        if('6' in json_dict and  json_dict['6']['type'] == "TD-TP"):
            i = 0
            while i < len(json_dict['6'])-1:
                teacher = Enseignant.objects.filter(nom=json_dict['6']["{}".format(i)]['enseignant'])[0]
                modules = Module.objects.filter(designation=json_dict['6']["{}".format(i)]['module'])[0]
                classroom = Salle.objects.filter(design=json_dict['6']["{}".format(i)]['salle'])[0]
                group = json_dict['6']["{}".format(i)]['groupe']
                period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe=group, groupe_type=json_dict['6']["{}".format(i)]['type_of_group'])            
                timetables.second_second.add(period)
                i = i+1
        elif '6' in json_dict and json_dict['6']['type'] == "Cours":
            teacher = Enseignant.objects.filter(nom=json_dict['6']['enseignant'])[0]
            modules = Module.objects.filter(designation=json_dict['6']['module'])[0]
            classroom = Salle.objects.filter(design=json_dict['6']['salle'])[0]
            period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe_type=json_dict['6']['type'])
            timetables.second_second.add(period)
     
        if('7' in json_dict and json_dict['7']['type'] == "TD-TP"):
            i = 0
            while i < len(json_dict['7'])-1:
                teacher = Enseignant.objects.filter(nom=json_dict['7']["{}".format(i)]['enseignant'])[0]
                modules = Module.objects.filter(designation=json_dict['7']["{}".format(i)]['module'])[0]
                classroom = Salle.objects.filter(design=json_dict['7']["{}".format(i)]['salle'])[0]
                group = json_dict['7']["{}".format(i)]['groupe']
                period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe=group, groupe_type=json_dict['7']["{}".format(i)]['type_of_group'])            
                timetables.second_third.add(period)
                i = i+1
        elif '7' in json_dict and json_dict['7']['type'] == "Cours":
            teacher = Enseignant.objects.filter(nom=json_dict['7']['enseignant'])[0]
            modules = Module.objects.filter(designation=json_dict['7']['module'])[0]
            classroom = Salle.objects.filter(design=json_dict['7']['salle'])[0]
            period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe_type=json_dict['7']['type'])
            timetables.second_third.add(period)

        if('8' in json_dict and  json_dict['8']['type'] == "TD-TP"):
            i = 0
            while i < len(json_dict['8'])-1:
                teacher = Enseignant.objects.filter(nom=json_dict['8']["{}".format(i)]['enseignant'])[0]
                modules = Module.objects.filter(designation=json_dict['8']["{}".format(i)]['module'])[0]
                classroom = Salle.objects.filter(design=json_dict['8']["{}".format(i)]['salle'])[0]
                group = json_dict['8']["{}".format(i)]['groupe']
                period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe=group, groupe_type=json_dict['8']["{}".format(i)]['type_of_group'])            
                timetables.second_forth.add(period)
                i = i+1
        elif '8' in json_dict and json_dict['8']['type'] == "Cours":
            teacher = Enseignant.objects.filter(nom=json_dict['8']['enseignant'])[0]
            modules = Module.objects.filter(designation=json_dict['8']['module'])[0]
            classroom = Salle.objects.filter(design=json_dict['8']['salle'])[0]
            period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe_type=json_dict['8']['type'])
            timetables.second_forth.add(period)

        if('9' in json_dict and  json_dict['9']['type'] == "TD-TP"):
            i = 0
            while i < len(json_dict['9'])-1:
                teacher = Enseignant.objects.filter(nom=json_dict['9']["{}".format(i)]['enseignant'])[0]
                modules = Module.objects.filter(designation=json_dict['9']["{}".format(i)]['module'])[0]
                classroom = Salle.objects.filter(design=json_dict['9']["{}".format(i)]['salle'])[0]
                group = json_dict['9']["{}".format(i)]['groupe']
                period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe=group, groupe_type=json_dict['9']["{}".format(i)]['type_of_group'])            
                timetables.third_first.add(period)
                i = i+1
        elif '9' in json_dict and json_dict['9']['type'] == "Cours":
            teacher = Enseignant.objects.filter(nom=json_dict['9']['enseignant'])[0]
            modules = Module.objects.filter(designation=json_dict['9']['module'])[0]
            classroom = Salle.objects.filter(design=json_dict['9']['salle'])[0]
            period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe_type=json_dict['9']['type'])
            timetables.third_first.add(period)

        if('10' in json_dict and  json_dict['10']['type'] == "TD-TP"):
            i = 0
            while i < len(json_dict['10'])-1:
                teacher = Enseignant.objects.filter(nom=json_dict['10']["{}".format(i)]['enseignant'])[0]
                modules = Module.objects.filter(designation=json_dict['10']["{}".format(i)]['module'])[0]
                classroom = Salle.objects.filter(design=json_dict['10']["{}".format(i)]['salle'])[0]
                group = json_dict['10']["{}".format(i)]['groupe']
                period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe=group, groupe_type=json_dict['10']["{}".format(i)]['type_of_group'])            
                timetables.third_second.add(period)
                i = i+1
        elif '10' in json_dict and json_dict['10']['type'] == "Cours":
            teacher = Enseignant.objects.filter(nom=json_dict['10']['enseignant'])[0]
            modules = Module.objects.filter(designation=json_dict['10']['module'])[0]
            classroom = Salle.objects.filter(design=json_dict['10']['salle'])[0]
            period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe_type=json_dict['10']['type'])
            timetables.third_second.add(period)

        if('11' in json_dict and  json_dict['11']['type'] == "TD-TP"):
            i = 0
            while i < len(json_dict['11'])-1:
                teacher = Enseignant.objects.filter(nom=json_dict['11']["{}".format(i)]['enseignant'])[0]
                modules = Module.objects.filter(designation=json_dict['11']["{}".format(i)]['module'])[0]
                classroom = Salle.objects.filter(design=json_dict['11']["{}".format(i)]['salle'])[0]
                group = json_dict['11']["{}".format(i)]['groupe']
                period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe=group, groupe_type=json_dict['11']["{}".format(i)]['type_of_group'])            
                timetables.third_third.add(period)
                i = i+1
        elif '11' in json_dict and json_dict['11']['type'] == "Cours":
            teacher = Enseignant.objects.filter(nom=json_dict['11']['enseignant'])[0]
            modules = Module.objects.filter(designation=json_dict['11']['module'])[0]
            classroom = Salle.objects.filter(design=json_dict['11']['salle'])[0]
            period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe_type=json_dict['11']['type'])
            timetables.third_third.add(period)

        if('12' in json_dict and json_dict['12']['type'] == "TD-TP"):
            i = 0
            while i < len(json_dict['12'])-1:
                teacher = Enseignant.objects.filter(nom=json_dict['12']["{}".format(i)]['enseignant'])[0]
                modules = Module.objects.filter(designation=json_dict['12']["{}".format(i)]['module'])[0]
                classroom = Salle.objects.filter(design=json_dict['12']["{}".format(i)]['salle'])[0]
                group = json_dict['12']["{}".format(i)]['groupe']
                period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe=group, groupe_type=json_dict['12']["{}".format(i)]['type_of_group'])            
                timetables.third_forth.add(period)
                i = i+1
        elif '12' in json_dict and json_dict['12']['type'] == "Cours":
            teacher = Enseignant.objects.filter(nom=json_dict['12']['enseignant'])[0]
            modules = Module.objects.filter(designation=json_dict['12']['module'])[0]
            classroom = Salle.objects.filter(design=json_dict['12']['salle'])[0]
            period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe_type=json_dict['12']['type'])
            timetables.third_forth.add(period)


        if('13' in json_dict and json_dict['13']['type'] == "TD-TP"):
            i = 0
            while i < len(json_dict['13'])-1:
                teacher = Enseignant.objects.filter(nom=json_dict['13']["{}".format(i)]['enseignant'])[0]
                modules = Module.objects.filter(designation=json_dict['13']["{}".format(i)]['module'])[0]
                classroom = Salle.objects.filter(design=json_dict['13']["{}".format(i)]['salle'])[0]
                group = json_dict['13']["{}".format(i)]['groupe']
                period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe=group, groupe_type=json_dict['13']["{}".format(i)]['type_of_group'])            
                timetables.forth_first.add(period)
                i = i+1
        elif '13' in json_dict and json_dict['13']['type'] == "Cours":
            teacher = Enseignant.objects.filter(nom=json_dict['13']['enseignant'])[0]
            modules = Module.objects.filter(designation=json_dict['13']['module'])[0]
            classroom = Salle.objects.filter(design=json_dict['13']['salle'])[0]
            period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe_type=json_dict['13']['type'])
            timetables.forth_first.add(period)

        
        if('14' in json_dict and json_dict['14']['type'] == "TD-TP"):
            i = 0
            while i < len(json_dict['14'])-1:
                teacher = Enseignant.objects.filter(nom=json_dict['14']["{}".format(i)]['enseignant'])[0]
                modules = Module.objects.filter(designation=json_dict['14']["{}".format(i)]['module'])[0]
                classroom = Salle.objects.filter(design=json_dict['14']["{}".format(i)]['salle'])[0]
                group = json_dict['14']["{}".format(i)]['groupe']
                period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe=group, groupe_type=json_dict['14']["{}".format(i)]['type_of_group'])            
                timetables.forth_second.add(period)
                i = i+1
        elif '14' in json_dict and json_dict['14']['type'] == "Cours":
            teacher = Enseignant.objects.filter(nom=json_dict['14']['enseignant'])[0]
            modules = Module.objects.filter(designation=json_dict['14']['module'])[0]
            classroom = Salle.objects.filter(design=json_dict['14']['salle'])[0]
            period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe_type=json_dict['14']['type'])
            timetables.forth_second.add(period)

        if('15' in json_dict and json_dict['15']['type'] == "TD-TP"):
            i = 0
            while i < len(json_dict['15'])-1:
                teacher = Enseignant.objects.filter(nom=json_dict['15']["{}".format(i)]['enseignant'])[0]
                modules = Module.objects.filter(designation=json_dict['15']["{}".format(i)]['module'])[0]
                classroom = Salle.objects.filter(design=json_dict['15']["{}".format(i)]['salle'])[0]
                group = json_dict['15']["{}".format(i)]['groupe']
                period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe=group, groupe_type=json_dict['15']["{}".format(i)]['type_of_group'])            
                timetables.forth_third.add(period)
                i = i+1
        elif '15' in json_dict and json_dict['15']['type'] == "Cours":
            teacher = Enseignant.objects.filter(nom=json_dict['15']['enseignant'])[0]
            modules = Module.objects.filter(designation=json_dict['15']['module'])[0]
            classroom = Salle.objects.filter(design=json_dict['15']['salle'])[0]
            period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe_type=json_dict['15']['type'])
            timetables.forth_third.add(period)

        if('16' in json_dict and json_dict['16']['type'] == "TD-TP"):
            i = 0
            while i < len(json_dict['16'])-1:
                teacher = Enseignant.objects.filter(nom=json_dict['16']["{}".format(i)]['enseignant'])[0]
                modules = Module.objects.filter(designation=json_dict['16']["{}".format(i)]['module'])[0]
                classroom = Salle.objects.filter(design=json_dict['16']["{}".format(i)]['salle'])[0]
                group = json_dict['16']["{}".format(i)]['groupe']
                period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe=group, groupe_type=json_dict['16']["{}".format(i)]['type_of_group'])            
                timetables.forth_forth.add(period)
                i = i+1
        elif '16' in json_dict and json_dict['16']['type'] == "Cours":
            teacher = Enseignant.objects.filter(nom=json_dict['16']['enseignant'])[0]
            modules = Module.objects.filter(designation=json_dict['16']['module'])[0]
            classroom = Salle.objects.filter(design=json_dict['16']['salle'])[0]
            period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe_type=json_dict['16']['type'])
            timetables.forth_forth.add(period)

        if('17' in json_dict and json_dict['17']['type'] == "TD-TP"):
            i = 0
            while i < len(json_dict['17'])-1:
                teacher = Enseignant.objects.filter(nom=json_dict['17']["{}".format(i)]['enseignant'])[0]
                modules = Module.objects.filter(designation=json_dict['17']["{}".format(i)]['module'])[0]
                classroom = Salle.objects.filter(design=json_dict['17']["{}".format(i)]['salle'])[0]
                group = json_dict['17']["{}".format(i)]['groupe']
                period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe=group, groupe_type=json_dict['17']["{}".format(i)]['type_of_group'])            
                timetables.fifth_first.add(period)
                i = i+1
        elif '17' in json_dict and json_dict['17']['type'] == "Cours":
            teacher = Enseignant.objects.filter(nom=json_dict['17']['enseignant'])[0]
            modules = Module.objects.filter(designation=json_dict['17']['module'])[0]
            classroom = Salle.objects.filter(design=json_dict['17']['salle'])[0]
            period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe_type=json_dict['17']['type'])
            timetables.fifth_first.add(period)
        
        if('18' in json_dict and json_dict['18']['type'] == "TD-TP"):
            i = 0
            while i < len(json_dict['18'])-1:
                teacher = Enseignant.objects.filter(nom=json_dict['18']["{}".format(i)]['enseignant'])[0]
                modules = Module.objects.filter(designation=json_dict['18']["{}".format(i)]['module'])[0]
                classroom = Salle.objects.filter(design=json_dict['18']["{}".format(i)]['salle'])[0]
                group = json_dict['18']["{}".format(i)]['groupe']
                period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe=group, groupe_type=json_dict['18']["{}".format(i)]['type_of_group'])            
                timetables.fifth_second.add(period)
                i = i+1
        elif '18' in json_dict and json_dict['18']['type'] == "Cours":
            teacher = Enseignant.objects.filter(nom=json_dict['18']['enseignant'])[0]
            modules = Module.objects.filter(designation=json_dict['18']['module'])[0]
            classroom = Salle.objects.filter(design=json_dict['18']['salle'])[0]
            period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe_type=json_dict['18']['type'])
            timetables.fifth_second.add(period)
              

        if('19' in json_dict and json_dict['19']['type'] == "TD-TP"):
            i = 0
            while i < len(json_dict['19'])-1:
                teacher = Enseignant.objects.filter(nom=json_dict['19']["{}".format(i)]['enseignant'])[0]
                modules = Module.objects.filter(designation=json_dict['19']["{}".format(i)]['module'])[0]
                classroom = Salle.objects.filter(design=json_dict['19']["{}".format(i)]['salle'])[0]
                group = json_dict['19']["{}".format(i)]['groupe']
                period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe=group, groupe_type=json_dict['19']["{}".format(i)]['type_of_group'])            
                timetables.fifth_third.add(period)
                i = i+1
        elif '19' in json_dict and json_dict['19']['type'] == "Cours":
            teacher = Enseignant.objects.filter(nom=json_dict['19']['enseignant'])[0]
            modules = Module.objects.filter(designation=json_dict['19']['module'])[0]
            classroom = Salle.objects.filter(design=json_dict['19']['salle'])[0]
            period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe_type=json_dict['19']['type'])
            timetables.fifth_third.add(period)


        if('20' in json_dict and json_dict['20']['type'] == "TD-TP"):
            i = 0
            while i < len(json_dict['20'])-1:
                teacher = Enseignant.objects.filter(nom=json_dict['20']["{}".format(i)]['enseignant'])[0]
                modules = Module.objects.filter(designation=json_dict['20']["{}".format(i)]['module'])[0]
                classroom = Salle.objects.filter(design=json_dict['20']["{}".format(i)]['salle'])[0]
                group = json_dict['20']["{}".format(i)]['groupe']
                period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe=group, groupe_type=json_dict['20']["{}".format(i)]['type_of_group'])            
                timetables.fifth_forth.add(period)
                i = i+1
        elif '20' in json_dict and json_dict['20']['type'] == "Cours":
            teacher = Enseignant.objects.filter(nom=json_dict['20']['enseignant'])[0]
            modules = Module.objects.filter(designation=json_dict['20']['module'])[0]
            classroom = Salle.objects.filter(design=json_dict['20']['salle'])[0]
            period = Periode.objects.create(enseignant=teacher, module=modules, salle=classroom, groupe_type=json_dict['20']['type'])
            timetables.fifth_forth.add(period)

        # timetables.save()
     
        ajax_data['successMsg'] = "success message"
    else:
        ajax_data['errorMsg'] = ' there is an error somewhere'

    return HttpResponse(json.dumps(ajax_data))


@login_required(login_url='login')
def create_order_staff(request):
    returned_data = {}

    if request.method == 'POST':
       
        data_client = json.loads(request.body)
        
        material = Material.objects.get(id=data_client['id_of_material'])
        material.is_available = False
        material.save()

        u = User.objects.get(id=request.user.id)

        staff = Staff.objects.get(user=u)

        order = Order.objects.create(staff=staff, item=material, returned=False)

        returned_data["success_message"] = "data was received successfuly"

    else:
        returned_data["error_message"] = "data didn't receive , something went wrong"
   
    return HttpResponse(json.dumps(returned_data))

@login_required(login_url='login')
def return_material(request):
    returned_data = {}

    if request.method == 'POST':
       
        data_client = json.loads(request.body)
        
        material = Material.objects.get(id=data_client['id_of_material'])
        material.is_available = True
        material.save()

        order = Order.objects.get(item=material, returned=False)
        order.returned = True
        order.save()

        returned_data["success_message"] = "data was received successfuly"
        returned_data["is returned"] = order.returned

    else:
        returned_data["error_message"] = "data didn't receive , something went wrong"
   
    return HttpResponse(json.dumps(returned_data))




# update all teachers and modules and classrooms____________________________________________________________________________
@login_required(login_url='login')
def update_teacher(request, slug): 
    notif_user = Staff.objects.filter(accepted=False)
    is_staf = give_permission(request, "peut_modifier_enseignant")
    if not is_staf:
        return redirect("admin_panel")

    model = get_object_or_404(Enseignant, slug=slug)
    if request.method == 'POST':
        form = EnseignantModelForm(request.POST, instance=model)
        if form.is_valid():
            form.save()
            return redirect("all_teachers")
    else: 
       form = EnseignantModelForm(instance=model)         
    context = {
        'title': 'update teacher',
        'form': form,
        'plain_user': notif_user
    } 
    return render(request, 'dashboard/update_teacher.html', context)   

@login_required(login_url='login')
def update_module(request, slug): 
    notif_user = Staff.objects.filter(accepted=False)
    is_staf = give_permission(request, "peut_modifier_module")
    if not is_staf:
        return redirect("admin_panel")


    model = get_object_or_404(Module, slug=slug)
    if request.method == 'POST':
        form = UpdateModuleModelForm(request.POST, instance=model)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.operateur = request.user
            new_form.save()
            return redirect("all_modules")
    else: 
       form = UpdateModuleModelForm(instance=model)         
    context = {
        'title': 'update module',
        'form': form,
        'plain_user': notif_user
    } 
    return render(request, 'dashboard/update_module.html', context)   

@login_required(login_url='login')
def update_salle(request, id): 
    notif_user = Staff.objects.filter(accepted=False)
    is_staf = give_permission(request, "peut_modifier_salle")
    if not is_staf:
        return redirect("admin_panel")


    model = get_object_or_404(Salle, id=id)
    if request.method == 'POST':
        form = UpdateSalleModelForm(request.POST, instance=model)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.opr = request.user
            new_form.save()
            return redirect("all_classrooms")
    else: 
       form = UpdateSalleModelForm(instance=model)         
    context = {
        'title': 'update classroom',
        'form': form,
        'plain_user': notif_user
    } 
    return render(request, 'dashboard/update_classroom.html', context)   


@login_required(login_url='login')
def update_staff(request, id): 
    notif_user = Staff.objects.filter(accepted=False)
    is_staf = give_permission(request, "peut_modifier_staff")
    if not is_staf:
        return redirect("admin_panel")

    staff = get_object_or_404(Staff, id=id)

    if request.method == 'POST':
        userForm = UpdateUserForm(request.POST, instance=staff.user)
        staffForm = StaffForm(request.POST, instance=staff)

        if userForm.is_valid() and staffForm.is_valid():

            userForm.save()
            staf = staffForm.save(commit=False)
            u = User.objects.get(id=staff.user.id)
            staf.user = u

            permissions = staffForm.cleaned_data["permissions"]
            for perms in permissions:
                permission = StaffPermission.objects.get(id=perms.id)
                staff.permissions.add(permission)

            staf.save()

            return redirect("all_staff")
    else:
        userForm = UpdateUserForm(instance=staff.user)
        staffForm = StaffForm(instance=staff)

    context = {
        'userForm': userForm,
        'staff': staffForm,
        'plain_user': notif_user
    }

    return render(request, 'dashboard/update_staff.html', context)

@login_required(login_url='login')
def update_timetable(request, id):
    notif_user = Staff.objects.filter(accepted=False)
    is_staf = give_permission(request, "peut_modifier_emploitemps")
    if not is_staf:
        return redirect("admin_panel")
    
    timetables = EmploiTemps.objects.get(id=id)

    context = {
        'emploitemps': timetables,
        'plain_user': notif_user
    }

    return render(request, 'dashboard/update_timetable.html', context)



    



# delete all teachers and modules and classrooms----------------------------------------------------------
@login_required(login_url='login')
def delete_teacher(request, slug):
    notif_user = Staff.objects.filter(accepted=False)
    is_staf = give_permission(request, "peut_supprimer_enseignant")
    if not is_staf:
        return redirect("admin_panel")


    model = get_object_or_404(Enseignant, slug=slug)
    try:
        if request.method == 'POST':
            model.active = True
            model.save()
            return redirect('all_teachers')
            messages.success(request, 'you have successfully delete it')
    except Exception as e:
        messages.error(request, 'the teacher could not be deleted: Error {}'.format(e))    
    
    context = {

        'enseignant': model,
        'plain_user': notif_user
    }
    return render(request, 'dashboard/delete_teacher.html', context)


@login_required(login_url='login')
def delete_module(request, slug):
    notif_user = Staff.objects.filter(accepted=False)
    is_staf = give_permission(request, "peut_supprimer_module")
    if not is_staf:
        return redirect("admin_panel")

    model = get_object_or_404(Module, slug=slug)
    try:

        if request.method == 'POST':
            model.active = True
            model.save()
            return redirect('all_modules')
            messages.success(request, 'you have successfully delete it')
    except Exception as e:
        messages.error(request, 'the module could not be deleted: Error {}'.format(e))          
    context = {
        'module': model,
        'plain_user': notif_user
    }
    return render(request, 'dashboard/delete_module.html', context)


@login_required(login_url='login')
def delete_classroom(request, id):
    notif_user = Staff.objects.filter(accepted=False)
    is_staf = give_permission(request, "peut_supprimer_salle")
    if not is_staf:
        return redirect("admin_panel")

    model = get_object_or_404(Salle, id=id)
    try:
        if request.method == 'POST':
            model.active = True
            model.save()
            return redirect('all_classrooms')
            messages.success(request, 'you have successfully delete it')
    except Exception as e:
        messages.error(request, 'the classroom could not be deleted: Error {}'.format(e))          
    context = {
        'salle': model,
        'plain_user': notif_user
    }
    return render(request, 'dashboard/delete_classroom.html', context)


@login_required(login_url='login')
def delete_timetable(request, id):
    notif_user = Staff.objects.filter(accepted=False)
    is_staf = give_permission(request, "peut_supprimer_emploitemps")
    if not is_staf:
        return redirect("admin_panel")





    timetable = get_object_or_404(EmploiTemps, id=id)

    context={
        'title': 'delete timetable',
        'timetable': timetable,
        'plain_user': notif_user
    }

    if request.method == "POST":
        timetable.delete()
        return redirect('all_emploitemps')
    else:
        messages.error(request, "something is wrong")        

    return render(request, 'dashboard/delete_timetable.html', context)

@login_required(login_url='login')
def delete_staff(request, id):
    notif_user = Staff.objects.filter(accepted=False)
    is_staf = give_permission(request, "peut_supprimer_staff")
    if not is_staf:
        return redirect("admin_panel")

    staff = get_object_or_404(Staff, id=id)
    try:
        if request.method == 'POST':
            staff.active = False
            staff.save()
            return redirect('all_staff')
            messages.success(request, 'you have successfully delete it')
    except Exception as e:
        messages.error(request, 'the classroom could not be deleted: Error {}'.format(e))          
    context = {
        'staff': staff,
        'plain_user': notif_user
    }
    return render(request, 'dashboard/delete_staff.html', context)



@login_required(login_url='login')
def confirm_anony_user(request):

    returned_data = {}
    fetch_data = json.loads(request.body)
    if request.method == "POST":

        anonymous_user = fetch_data

        staff = Staff.objects.get(id=anonymous_user['account_id'])
        if(anonymous_user['operation'] == "confirm"):
            
            staff.accepted = True
            staff.save()
            print("after confirming staff", staff, staff.accepted)
            timetable_permission = StaffPermission.objects.get(name="peut_lister_toutes_emploitems")
            reservation_permission = StaffPermission.objects.get(name="peut_lister_toutes_materials")
            ordre_permission = StaffPermission.objects.get(name="peut_lister_toutes_ordres")
            
            staff.permissions.add(timetable_permission, reservation_permission)
            
        elif anonymous_user['operation'] == "delete":
            try:
                user = User.objects.get(staff=staff)
                user.delete()
                messages.success(request, "The user is deleted")            

            except User.DoesNotExist:
                messages.error(request, "User doesnot exist")    
                

            except Exception as e: 
                returned_data["error"] = e.message
    
        returned_data["success"] = "data received successfuty"
    else:

        returned_data["error"] = "something went wrong"


    return HttpResponse(json.dumps(returned_data))




# document part  ééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééé

# timetable with classroom -----------------------------------------
@login_required(login_url='login')
def salle_document(request):
    notif_user = Staff.objects.filter(accepted=False)

    is_staf = give_permission(request, "peut_afficher_emploi_salle")
    if not is_staf:
        return redirect("admin_panel")


    context = {
        "niveau": Niveau.objects.all(),
        'plain_user': notif_user
    }

    return render(request, "dashboard/document_classroom.html", context)
@login_required(login_url='login')
def load_classR_doc_data(request):

    loaded_data = json.loads(request.body)

    timetable_name = '{}-{}'.format(loaded_data['level'], loaded_data ['semester'])
    print("table name ", timetable_name)

    classroom_type_document = {}
    row_number = 1

    try:
        timetable_obj = EmploiTemps.objects.get(slug=timetable_name)

    except EmploiTemps.DoesNotExist:
        return HttpResponse(json.dumps("no result"))
        

    for tt_attr in dir(timetable_obj):

        if tt_attr in timetable_atts:

            perd = getattr(timetable_obj, "{}".format(tt_attr))

            for p in perd.all():
                if loaded_data['cr_type'] == "tout":
                    if p.groupe_type == "TD" or p.groupe_type == "TP":
                        classroom_type_document["{}".format(row_number)] = {
                            "day" : day_converter[tt_attr],
                            "hour" : hour_converter[tt_attr],
                            "group" : p.groupe,
                            "type": p.groupe_type,
                            "classroom" : p.salle.design
                        }
                elif p.groupe_type == loaded_data['cr_type']:
                    classroom_type_document["{}".format(row_number)] = {
                        "day" : day_converter[tt_attr],
                        "hour" : hour_converter[tt_attr],
                        "group" : p.groupe,
                        "type": p.groupe_type,
                        "classroom" : p.salle.design
                    }
                row_number +=1

    return HttpResponse(json.dumps(classroom_type_document))


# weekly teaching followup -----------------------------------------
@login_required(login_url='login')
def Weekly_teaching_followup_document(request):
    notif_user = Staff.objects.filter(accepted=False)

    is_staf = give_permission(request, "peut_afficher_fiche_haib_sui_e")
    if not is_staf:
        return redirect("admin_panel")

    context = {
        "niveau": Niveau.objects.all(),
        'plain_user': notif_user
    }

    return render(request, "dashboard/document_teaching_followup.html", context)
@login_required(login_url='login')
def load_teaching_followup(request):

    loaded_data = json.loads(request.body)

    timetable_name = '{}-{}'.format(loaded_data['level'], loaded_data ['semester'])
    print("table name followup", timetable_name)

    teaching_followup_document = {}
    row_number = 1

    try:
        timetable_obj = EmploiTemps.objects.get(slug=timetable_name)
    except EmploiTemps.DoesNotExist:
        return HttpResponse(json.dumps("no result"))
        

    for tt_attr in dir(timetable_obj):

        if tt_attr in timetable_atts:

            perd = getattr(timetable_obj, "{}".format(tt_attr))

            for p in perd.all():
                if p.groupe_type == "Cours":
                    teaching_followup_document["{}".format(row_number)] = {
                        "day" : day_converter[tt_attr],
                        "hour" : hour_converter[tt_attr],
                        "group" : "",
                        "module" : p.module.designation,
                        "nature": "C",
                        "teacher" : p.enseignant.nom,
                        "classroom" : p.salle.design
                    }
                else :
                    teaching_followup_document["{}".format(row_number)] = {
                        "day" : day_converter[tt_attr],
                        "hour" : hour_converter[tt_attr],
                        "group" : p.groupe,
                        "module" : p.module.designation,
                        "nature": p.groupe_type,
                        "teacher" : p.enseignant.nom,
                        "classroom" : p.salle.design
                    }

                row_number +=1

    return HttpResponse(json.dumps(teaching_followup_document))


# teacher hourly loader -----------------------------------------
@login_required(login_url='login')
def teacher_hourly_loader(request):
    notif_user = Staff.objects.filter(accepted=False)

    is_staf = give_permission(request, "peut_afficher_charge_horaire_e")
    if not is_staf:
        return redirect("admin_panel")

    context = {
        "enseignant" : Enseignant.objects.all(),
        "niveau": Niveau.objects.all(),
        'plain_user': notif_user,
    }
    return render(request, "dashboard/document_teacher_hourlyL.html", context)
@login_required(login_url='login')
def load_teacher_hourlyL(request):

    loaded_data = json.loads(request.body)

    # timetable_name = '{}-{}'.format(loaded_data['level'], loaded_data ['semester'])

    teaching_followup_document = {}
    row_number = 1

    # try:
    #     timetable_obj = EmploiTemps.objects.get(slug=timetable_name)
    # except EmploiTemps.DoesNotExist:
    #     return HttpResponse(json.dumps("no result"))
        
    timetables = EmploiTemps.objects.all()
    for timetable_obj in timetables:
        for tt_attr in dir(timetable_obj):

            if tt_attr in timetable_atts:

                perd = getattr(timetable_obj, "{}".format(tt_attr))

                for p in perd.all():
                    if p.enseignant.get_departement_display() == loaded_data['department']:
                        if p.groupe_type == "Cours":
                            teaching_followup_document["{}".format(row_number)] = {
                                "teacher" : "{} {}".format(p.enseignant.nom, p.enseignant.prenom),
                                "module" : p.module.designation,
                                "nature": "C",
                                "group" : "",                        
                            }
                        else :
                            teaching_followup_document["{}".format(row_number)] = {
                                "teacher" : "{} {}".format(p.enseignant.nom, p.enseignant.prenom),
                                "module" : p.module.designation,
                                "nature": p.groupe_type,
                                "group" : p.groupe,                        
                            }

                        row_number +=1

    if teaching_followup_document == {}:
        return HttpResponse(json.dumps("no result"))


    # counting how much hour for each teacher teach
    teacher_counter = {}
    for i in range(1, len(teaching_followup_document)-1):
        if teaching_followup_document['{}'.format(i)]['teacher'] not in teacher_counter:
            teacher_counter[teaching_followup_document['{}'.format(i)]['teacher']] = {
                "module" : teaching_followup_document['{}'.format(i)]['module'],
                "nature" : teaching_followup_document['{}'.format(i)]['nature'],
                "group" : [teaching_followup_document['{}'.format(i)]['group']],
                "count" : 1
            }
            for j in range(i+1, len(teaching_followup_document)):
                if teaching_followup_document['{}'.format(i)]['teacher'] == teaching_followup_document['{}'.format(j)]['teacher']:
                    teacher_counter[teaching_followup_document['{}'.format(i)]['teacher']]['count'] +=1
                    if(teaching_followup_document['{}'.format(j)]['group'] not in teacher_counter[teaching_followup_document['{}'.format(i)]['teacher']]['group']):
                        teacher_counter[teaching_followup_document['{}'.format(i)]['teacher']]['group'].append(teaching_followup_document['{}'.format(j)]['group'])



    return HttpResponse(json.dumps(teacher_counter))


# teacher with department----------------------------------------
@login_required(login_url='login')
def teacher_dep(request):
    notif_user = Staff.objects.filter(accepted=False)

    is_staf = give_permission(request, "peut_afficher_ens_département")
    if not is_staf:
        return redirect("admin_panel")
    print("dep", Enseignant.DEPARTMENT)
    context = {
        "enseignant" : Enseignant.DEPARTMENT,
        "niveau": Niveau.objects.all(),
        'plain_user': notif_user
    }
    return render(request, "dashboard/document_teacher_department.html", context)
@login_required(login_url='login')
def load_teacher_dep(request):

   
    
    loaded_data = json.loads(request.body)
    print("dep", loaded_data['department'])



    
    teacher_department_document = {}
    row_number = 1

    for enseignant in Enseignant.objects.all():
        if enseignant.get_departement_display() == loaded_data['department']:
            teacher_department_document["{}".format(row_number)] = {
                "teacher" : "{} {}".format(enseignant.nom, enseignant.prenom),
                "email" : enseignant.email,                 
            }
        row_number +=1
        

    print("teacher department", teacher_department_document)

    if(teacher_department_document == {}):
        return HttpResponse(json.dumps("no result"))
    

    return HttpResponse(json.dumps(teacher_department_document))

# timetable of teacher ----------------------------------------
@login_required(login_url='login')
def teacher_timetable(request):
    notif_user = Staff.objects.filter(accepted=False)

    is_staf = give_permission(request, "peut_afficher_emploi_ens")
    if not is_staf:
        return redirect("admin_panel")


    context = {
        "enseignant": Enseignant.objects.all(),
        'plain_user': notif_user
    }
    return render(request, "dashboard/document_teacher_timetable.html", context)




# PDF part  ééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééééé

# generate the timetable template to PDF:----------------------------
@login_required(login_url='login')
def generatePDF(request, id):
    print("url path :")

    emploi_data = get_object_or_404(EmploiTemps, id=id)
    context = {
        'title': 'pdf',
        'emploitemps': emploi_data,
        'current_time': datetime.datetime.now()
    }
    pdf = render_to_pdf("dashboard/PDF_timetable.html", context)
    return HttpResponse(pdf, content_type="application/pdf")


# generate timetable of teacher's template to PDF--------------------------------------------
@login_required(login_url='login')
def generate_ttt_PDF(request, slug):


    chargehoraire = {}
    enseignant = get_object_or_404(Enseignant, slug=slug)
    periods = Periode.objects.filter(enseignant=enseignant)
    timetable = EmploiTemps.objects.all()


    print("length of attrs", len(timetable_atts))

    for tt in timetable:
        for atr in dir(tt):
            
            if atr in timetable_atts:

                per = getattr(tt, '{}'.format(atr))

                for p in per.all():
                    if p.enseignant.nom == enseignant.nom:
                        if  p.groupe != None:
                            chargehoraire['{}'.format(atr)] = {
                                "module": p.module.designation,
                                "groupe_type": p.groupe_type,
                                "groupe": p.groupe
                            }
                        else: 
                            chargehoraire['{}'.format(atr)] = {
                                "module": p.module.designation,
                                "groupe_type": p.groupe_type,
                                "groupe": ""
                            }


    notif_user = Staff.objects.filter(accepted=False)
    print("charge horaire ", chargehoraire)
    context = {
        'title': 'charge horaire pour enseignent',
        'chargehoraire': chargehoraire,
        'enseignant' : enseignant,
        'plain_user': notif_user,
        'current_time': datetime.datetime.now()
    }


    pdf = render_to_pdf("dashboard/PDF_teacher_timetable.html", context)
    return HttpResponse(pdf, content_type="application/pdf")


# generate timetable of teacher template to PDF----------------------------------
@login_required(login_url='login')
def generate_teacher_hourlyL_PDF(request, department):


   
    department = department
    
    teaching_followup_document = {}
    row_number = 1

    timetables = EmploiTemps.objects.all()
    # try:
    #     timetable_obj = EmploiTemps.objects.get(slug=timetable_name)
    # except EmploiTemps.DoesNotExist:
    #     return HttpResponse(json.dumps("no result"))
        
    for timetable_obj in timetables:
        
        for tt_attr in dir(timetable_obj):

            if tt_attr in timetable_atts:

                perd = getattr(timetable_obj, "{}".format(tt_attr))

                for p in perd.all():
                    if p.enseignant.get_departement_display() == department:
                        if p.groupe_type == "Cours":
                            teaching_followup_document["{}".format(row_number)] = {
                                "teacher" : "{} {}".format(p.enseignant.nom, p.enseignant.prenom),
                                "module" : p.module.designation,
                                "nature": "C",
                                "group" : "",                        
                            }
                        else :
                            teaching_followup_document["{}".format(row_number)] = {
                                "teacher" : "{} {}".format(p.enseignant.nom, p.enseignant.prenom),
                                "module" : p.module.designation,
                                "nature": p.groupe_type,
                                "group" : p.groupe,                        
                            }

                        row_number +=1

        
    
    if teaching_followup_document == {}:
        return HttpResponse(json.dumps("no result"))


    # counting how much hour for each teacher teach
    teacher_counter = {}
    c = 1
    for i in range(1, len(teaching_followup_document)-1):
        if teaching_followup_document['{}'.format(i)]['teacher'] not in teacher_counter:
            teacher_counter[teaching_followup_document['{}'.format(i)]['teacher']] = {
                "teacher" : teaching_followup_document['{}'.format(i)]['teacher'],
                "module" : teaching_followup_document['{}'.format(i)]['module'],
                "nature" : teaching_followup_document['{}'.format(i)]['nature'],
                "group" : [teaching_followup_document['{}'.format(i)]['group']],
                "count" : 1
            }
            for j in range(i+1, len(teaching_followup_document)):
                if teaching_followup_document['{}'.format(i)]['teacher'] == teaching_followup_document['{}'.format(j)]['teacher']:
                    teacher_counter[teaching_followup_document['{}'.format(i)]['teacher']]['count'] +=1
                    if(teaching_followup_document['{}'.format(j)]['group'] not in teacher_counter[teaching_followup_document['{}'.format(i)]['teacher']]['group']):
                        teacher_counter[teaching_followup_document['{}'.format(i)]['teacher']]['group'].append(teaching_followup_document['{}'.format(j)]['group'])

    
    print("tece", teacher_counter)
    context = {
        "teacher_counter" : teacher_counter,
        'current_time':  datetime.datetime.now()
    }

    pdf = render_to_pdf("dashboard/PDF_teacher_hourlyL.html", context)
    return HttpResponse(pdf, content_type="application/pdf")


# generate timetable of classroom template to PDF----------------------------------
@login_required(login_url='login')
def generate_clarssR_timetable_PDF(request, level, semester, cr_type):

    

    timetable_name = '{}-{}'.format(level, semester)
    print("table name ", timetable_name)

    classroom_type_document = {}
    row_number = 1

    try:
        timetable_obj = EmploiTemps.objects.get(slug=timetable_name)

    except EmploiTemps.DoesNotExist:
        return HttpResponse(json.dumps("no result"))
        

    for tt_attr in dir(timetable_obj):

        if tt_attr in timetable_atts:

            perd = getattr(timetable_obj, "{}".format(tt_attr))

            for p in perd.all():
                if cr_type == "tout":
                    if p.groupe_type == "TD" or p.groupe_type == "TP":
                        classroom_type_document["{}".format(row_number)] = {
                            "day" : day_converter[tt_attr],
                            "hour" : hour_converter[tt_attr],
                            "group" : p.groupe,
                            "type": p.groupe_type,
                            "classroom" : p.salle.design
                        }
                elif p.groupe_type == cr_type:
                    classroom_type_document["{}".format(row_number)] = {
                        "day" : day_converter[tt_attr],
                        "hour" : hour_converter[tt_attr],
                        "group" : p.groupe,
                        "type": p.groupe_type,
                        "classroom" : p.salle.design
                    }
                row_number +=1


    context = {
        "timetable_classroom" : classroom_type_document,
        'current_time':  datetime.datetime.now()
    }

    pdf = render_to_pdf("dashboard/PDF_timetable_classroom.html", context)
    return HttpResponse(pdf, content_type="application/pdf")


# generate weakly teaching followup template to PDF----------------------------------
@login_required(login_url='login')
def generate_Weekly_teaching_followup_PDF(request, level, semester):

    timetable_name = '{}-{}'.format(level, semester)
    print("table name followup", timetable_name)

    teaching_followup_document = {}
    row_number = 1

    try:
        timetable_obj = EmploiTemps.objects.get(slug=timetable_name)
    except EmploiTemps.DoesNotExist:
        return HttpResponse(json.dumps("no result"))
        

    for tt_attr in dir(timetable_obj):

        if tt_attr in timetable_atts:

            perd = getattr(timetable_obj, "{}".format(tt_attr))

            for p in perd.all():
                if p.groupe_type == "Cours":
                    teaching_followup_document["{}".format(row_number)] = {
                        "day" : day_converter[tt_attr],
                        "hour" : hour_converter[tt_attr],
                        "group" : "",
                        "module" : p.module.designation,
                        "nature": "C",
                        "teacher" : p.enseignant.nom,
                        "classroom" : p.salle.design
                    }
                else :
                    teaching_followup_document["{}".format(row_number)] = {
                        "day" : day_converter[tt_attr],
                        "hour" : hour_converter[tt_attr],
                        "group" : p.groupe,
                        "module" : p.module.designation,
                        "nature": p.groupe_type,
                        "teacher" : p.enseignant.nom,
                        "classroom" : p.salle.design
                    }

                row_number +=1

    context = {
        "weakly_teaching_followup" : teaching_followup_document,
        'current_time':  datetime.datetime.now()
    }

    pdf = render_to_pdf("dashboard/PDF_weakly_followup.html", context)
    return HttpResponse(pdf, content_type="application/pdf")




















