from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path('', views.panel, name='admin_panel'),
    path('all-teachers/', views.all_ens, name='all_teachers'),
    path('all-modules/', views.all_modules, name='all_modules'),
    path('all-classrooms/', views.all_classrooms, name='all_classrooms'),
    path('all-timetables', views.all_timetables, name='all_emploitemps'),
    path('all-TT-conditions', views.all_TT_canvas, name='all_TT_conditions'),
    url(r'^(?P<id>\d+)/pdf$', views.generatePDF, name="pdf_emploi"),
    path('new-teacher/', views.new_teacher, name='new-teacher'),
    path('new-module/', views.new_module, name='new-module'),
    path('new-classroom/', views.new_classroom, name='new-classroom'),
    path('new-timetable/', views.new_timetable, name='new-timetable'),
    path('new-canvas', views.createTimetableCanvas, name='new-canvas'),
    path('new-timetable/saveData/', views.save_data, name='save-data'),
    path('timetable-detail/<int:id>', views.timetable_detail, name='timetable-detail'),
    path('canvas-detail/<int:id>', views.canvas_detail, name='canvas_detail'),
    url(r'^update-teacher/(?P<slug>.*)/$', views.update_teacher, name='update-teacher'),
    url(r'^delete-teacher/(?P<slug>.*)/$', views.delete_teacher, name='delete-teacher'),
    url(r'^update-module/(?P<slug>.*)/$', views.update_module, name='update-module'),
    url(r'^delete-module/(?P<slug>.*)/$', views.delete_module, name='delete-module'),
    path('update-classroom/<int:id>', views.update_salle, name='update-classroom'),
    path('delete-classroom/<int:id>', views.delete_classroom, name='delete-classroom'),
    path('delete-timetable/<int:id>', views.delete_timetable, name='delete-timetable'),    
]
