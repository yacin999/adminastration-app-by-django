from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [

# LIST urls ===================================================================================
    path('', views.panel, name='admin_panel'),
    path('all-teachers/', views.all_ens, name='all_teachers'),
    path('all-modules/', views.all_modules, name='all_modules'),
    path('all-classrooms/', views.all_classrooms, name='all_classrooms'),
    path('all-timetables/', views.all_timetables, name='all_emploitemps'),
    path('all-material/', views.all_material, name='all_material'),
    path('all-orders/', views.all_orders, name='all_orders'),
    path('all-staff/', views.all_staff, name='all_staff'),


# CREATE urls ===================================================================================
    path('new-teacher/', views.new_teacher, name='new-teacher'),
    path('new-module/', views.new_module, name='new-module'),
    path('new-classroom/', views.new_classroom, name='new-classroom'),
    path('new-timetable/', views.new_timetable, name='new-timetable'),
    path('new-staff/', views.new_staff, name='new-staff'),
    path('new-material/', views.new_material, name='new_material'),
    path('new-timetable/saveData/', views.save_data, name='save-data'),
    path('new-order/', views.create_order_staff, name='create_order'),
    path('return-material/', views.return_material, name='return_material'),


# DETAIL urls ===================================================================================
    path('timetable-detail/<int:id>', views.timetable_detail, name='timetable-detail'),


# UPDATE urls ===================================================================================
    url(r'^update-teacher/(?P<slug>.*)/$', views.update_teacher, name='update-teacher'),
    url(r'^update-module/(?P<slug>.*)/$', views.update_module, name='update-module'),
    path('update-classroom/<int:id>', views.update_salle, name='update-classroom'),
    path('update-staff/<int:id>', views.update_staff, name='update-staff'),
    path('update-timetable/<int:id>', views.update_timetable, name='update-timetable'),


# DELETE urls ===================================================================================
    path('delete-classroom/<int:id>', views.delete_classroom, name='delete-classroom'),
    path('delete-timetable/<int:id>', views.delete_timetable, name='delete-timetable'), 
    url(r'^delete-teacher/(?P<slug>.*)/$', views.delete_teacher, name='delete-teacher'),
    url(r'^delete-module/(?P<slug>.*)/$', views.delete_module, name='delete-module'),
    path('delete-staff/<int:id>', views.delete_staff, name='delete-staff'),

# PDF urls ===================================================================================
    url(r'^(?P<id>\d+)/pdf$', views.generatePDF, name="pdf_emploi"),
    
]



