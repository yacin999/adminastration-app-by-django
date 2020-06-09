from django.urls import path
from . import views



urlpatterns = [
    path('timetable-list/', views.timetable_serializer_list),
    path('module-list/', views.module_serializer_list),
    path('canvas-list/', views.CanvasList.as_view()),
    path('teacher-list/', views.teacher_serializer_list),
    path('classroom-list/', views.classroom_serializer_list),
    path('timetable-detail/<int:id>', views.timetable_serializer_detail),
    path('module-detail/<int:id>', views.module_serializer_detail),
    #path('canva-detail/<int:id>', views.canvas_serializer_detail),
]
