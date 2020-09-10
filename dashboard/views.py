from django.shortcuts import get_object_or_404, redirect, render
from .models import Enseignant, Module, Salle, EmploiTemps, Periode, Niveau, CanvasTimeTable
from user.models import Staff, StaffPermission
from django.views.generic import CreateView
from .forms import EnseignantModelForm, ModuleModelForm, SalleModelForm
from user.forms import UserForm , StaffForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from univv.utils import render_to_pdf
import re
import random
from re import sub
import json




# def findWholeWord(w):

#         return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

#         p = sub.Popen(('sudo', 'tcpdump', '-l', '-s 0', '-vvv', '-n', '((udp port 67) and (udp[8:1] = 0x1))'), stdout=sub.PIPE)
#         for row in iter(p.stdout.readline, b''):
#             if findWholeWord('requested-ip')(row):
#                 print(row.split(' ')[-1])
#                 print('mac_______address')
#             elif findWholeWord('client-id')(row):
#                 print(row.split(' ')[-1])



@login_required(login_url='login')
def panel(reqeust):
    return render(reqeust, 'dashboard/admin_panel.html',{})


# get all teachers and modules and classrooms ========================================================================
@login_required(login_url='login')
def all_ens(request):
    teacher = Enseignant.objects.filter(active=False)
    context = {
        'title': 'les enseignants',
        'teachers' : teacher,
    }

    return render(request, 'dashboard/all_teachers.html', context)

@login_required(login_url='login')
def all_modules(request):
    module = Module.objects.filter(active=False)
    context = {
        'title': 'les modules',
        'modules' : module, 
    }

    return render(request, 'dashboard/all_modules.html', context)

@login_required(login_url='login')
def all_classrooms(request):
    model = Salle.objects.filter(active=False)
    template_name = 'dashboard/all_classrooms.html'
    context = {
        'title': 'all classrooms',
        'salles': model,
    }

    return render(request, template_name, context)

@login_required(login_url='login')
def all_timetables(request):
    model = EmploiTemps.objects.all()
    context = {
        'title': 'all timetibles',
        'emploitemps': model,
    }

    return render(request, 'dashboard/all_emploitems.html', context)

@login_required(login_url='login')
def all_TT_canvas(request):
    all_conditions = CanvasTimeTable.objects.all().order_by('slug')
    context = {
        'all_conditions': all_conditions,
    }


    return render(request, 'dashboard/all_TT_conditions.html', context)




#create all teachers and modules and classrooms and tabletimes ______________________________________________________________________________
@login_required(login_url='login')
def new_teacher(request):
    if request.method == 'POST':
        form = EnseignantModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("all_teachers")
    else:
        form = EnseignantModelForm()
    context = {
        'title': 'new teacher',
        'form': form,
    }
    return render(request, 'dashboard/new_teacher.html', context)

@login_required(login_url='login')
def new_module(request):
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
    }
    return render(request, 'dashboard/new_module.html', context)

@login_required(login_url='login')
def new_classroom(request):
    if request.method == 'POST':
        form = SalleModelForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.opr = request.user
            new_form.save()
            return redirect("all_classrooms")
    else:
        form = SalleModelForm()
    context = {
        'title': 'new classroom',
        'form': form,
    }
    return render(request, 'dashboard/new_classroom.html', context)


@login_required(login_url='login')
def timetable_detail(request, id):

    emploiTemp = EmploiTemps.objects.get(id=id)
    context = {
        'title': 'timetable-detail',
        'emploitemps': emploiTemp,
    }
    return render(request, 'dashboard/detail_timetable.html', context)



@login_required(login_url='login')
def canvas_detail(request, id):
    canva = CanvasTimeTable.objects.get(id=id)
    canvas = CanvasTimeTable.objects.all()

    context = {
        'title': 'canvas-detail',
        'canvas_detail': canva,
        'all_canvas': canvas
    } 

    return render(request, 'dashboard/canvas_datail.html', context)




@login_required(login_url='login')
def new_timetable(request):
    permissions = request.user.staff.permissions.all()
    # users = User.objects.all()
    # staffs = Staff.objects.all()
    
    # for staff in staffs:
    #     print("all users {}".format(staff.user.username), staff.permissions.all())
    # #print("our permissions", permissions)
    is_staf = False

    for permission in permissions:
        print("all users", permission.name)
        print("our permissions", permissions)
        if (permission.name == "can_create_timetable"):
            is_staf = True

    if not is_staf:
        return redirect("admin_panel")
        


    niveau = Niveau.objects.all()
    teachers = Enseignant.objects.all().values("nom").distinct().filter(active=False)
    name_of_modules = Module.objects.all().filter(active=False)
    classrooms = Salle.objects.all().values("design").distinct()
    canvas = CanvasTimeTable.objects.all()

    context = {
        'title': 'creating timetables',
        'teachers': teachers,
        'modules': name_of_modules,
        'classrooms': classrooms,
        'niveau': niveau,
        'canvas': canvas,
    }
    return render(request, 'dashboard/new_timetable.html', context)


@login_required(login_url='login')
def new_staff(request):
    if (request.method == 'POST'):
        userform = UserForm(request.POST)
        staffForm = StaffForm(request.POST)

        if userform.is_valid() and staffForm.is_valid():
            user = userform.save(commit=False)
            user.set_password(userform.cleaned_data["password1"])
            user.save()

            staff = staffForm.save(commit=False)
            permissions = staffForm.cleaned_data["permissions"]
            u = User.objects.get(id=user.id)
            staff = Staff(user=u)
            staff.save()
            for perms in permissions:
                permission = StaffPermission.objects.get(id=perms.id)
                staff.permissions.add(permission)
            return redirect("all_teachers")
        
        user = UserForm()
        staff = StaffForm()
            
    else:
        user = UserForm()
        staff = StaffForm()

    context = {
        'user': user,
        'staff': staff
    }
    
    return render(request, "dashboard/new_staff.html", context)






# to save data in the database via the ajax object ---------------$$
import json
def save_data(request):

    ajax_data = {} 
    print("from the server side")
    print(request.POST)

    if request.method == 'POST' and request.is_ajax():
        
        json_dict = json.loads(request.POST['our_data'])
        level = Niveau.objects.get(Nv=request.POST['level'])
        semestre = request.POST['semestre']
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



# generate the timetable template to PDF:
 
def generatePDF(request, id):
    emploi_data = get_object_or_404(EmploiTemps, id=id)
    context = {
        'title': 'pdf',
        'emploitemps': emploi_data,
    }
    pdf = render_to_pdf("dashboard/PDF_timetable.html", context)
    return HttpResponse(pdf, content_type="application/pdf")



def createTimetableCanvas(request):
    niveax = Niveau.objects.all()
    modules = Module.objects.all()

    context = {
        'niveax': niveax,
        'modules': modules
    }

    if request.method == 'POST':
        niveau_name = request.POST['niveau']
        semestre = request.POST['semestre']
        module_name = request.POST['module']
        cours = request.POST['cours']
        tp = request.POST['tp']
        td = request.POST['td']

        module_object = Module.objects.get(designation=module_name)
        niveau_object = Niveau.objects.get(Nv=niveau_name)

        canva = CanvasTimeTable(modules= module_object, semestre=semestre, cours=cours, niveau=niveau_object, tp=tp, td=td)
        canva.save()
        return redirect('all_TT_conditions')

    return render(request, 'dashboard/new_TTcanvas.html', context)

# update all teachers and modules and classrooms____________________________________________________________________________
@login_required(login_url='login')
def update_teacher(request, slug): 
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
    } 
    return render(request, 'dashboard/update_teacher.html', context)   

@login_required(login_url='login')
def update_module(request, slug): 
    model = get_object_or_404(Module, slug=slug)
    if request.method == 'POST':
        form = ModuleModelForm(request.POST, instance=model)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.operateur = request.user
            new_form.save()
            return redirect("all_modules")
    else: 
       form = ModuleModelForm(instance=model)         
    context = {
        'title': 'update module',
        'form': form,
    } 
    return render(request, 'dashboard/update_module.html', context)   

@login_required(login_url='login')
def update_salle(request, id): 
    model = get_object_or_404(Salle, id=id)
    if request.method == 'POST':
        form = SalleModelForm(request.POST, instance=model)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.opr = request.user
            new_form.save()
            return redirect("all_classrooms")
    else: 
       form = SalleModelForm(instance=model)         
    context = {
        'title': 'update classroom',
        'form': form,
    } 
    return render(request, 'dashboard/update_classroom.html', context)   


# delete all teachers and modules and classrooms----------------------------------------------------------
@login_required(login_url='login')
def delete_teacher(request, slug):
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
    }
    return render(request, 'dashboard/delete_teacher.html', context)


@login_required(login_url='login')
def delete_module(request, slug):

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
    }
    return render(request, 'dashboard/delete_module.html', context)


@login_required(login_url='login')
def delete_classroom(request, id):

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
    }
    return render(request, 'dashboard/delete_classroom.html', context)



def delete_timetable(request, id):
    timetable = get_object_or_404(EmploiTemps, id=id)

    context={
        'title': 'delete timetable',
        'timetable': timetable,
    }

    if request.method == "POST":
        timetable.delete()
        return redirect('all_emploitemps')
    else:
        messages.error(request, "something is wrong")        

    return render(request, 'dashboard/delete_timetable.html', context)
