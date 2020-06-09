from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from .serializers import EmpoiTempsSerializer, ModuleSerializer, CanvasSerializer, TeacherSerializer, ClassroomSerializer
from dashboard.models import EmploiTemps, Module, CanvasTimeTable, Enseignant, Salle
from rest_framework import status




@api_view(['GET',])
def timetable_serializer_list(request):
    timetables = EmploiTemps.objects.all()

    if request.method == 'GET':
        serializer = EmpoiTempsSerializer(timetables, many=True)   
        return Response(serializer.data)
    # return Response(status=status.)     
 

@api_view(['GET',])
def timetable_serializer_detail(request, id):
    
    try:
        timetable = EmploiTemps.objects.get(id=id)
    except timetable.DoesNotExist:
        Response(status=status.HTTP_404_NOT_FOUND)    

    if request.method == 'GET':
        serializer = EmpoiTempsSerializer(timetable)   
        return Response(serializer.data)



# Module serializers ::::::::::::::::::::
@api_view(['GET',])
def module_serializer_list(request):
    modules = Module.objects.all()

    if request.method == 'GET':
        serializer = ModuleSerializer(modules, many=True)   
        return Response(serializer.data)




@api_view(['GET',])
def module_serializer_detail(request, id):
    
    try:
        module = Module.objects.get(id=id)
    except module.DoesNotExist:
        Response(status=status.HTTP_404_NOT_FOUND)    

    if request.method == 'GET':
        serializer = ModuleSerializer(module)   
        return Response(serializer.data)





#Canvas of timetable serializer::::::::::
class CanvasList(mixins.ListModelMixin, generics.GenericAPIView):
    
    queryset = CanvasTimeTable.objects.all()
    serializer_class = CanvasSerializer

    def get(self, request, *args, **kwargs):
        return self.list(self, *args, **kwargs)

    

@api_view(['GET',])
def canvas_serializer_detail(request, id):
    
    try:
        canva = CanvasTimeTable.objects.get(id=id)
    except canva.DoesNotExist:
        Response(status=status.HTTP_404_NOT_FOUND)    

    if request.method == 'GET':
        serializer = EmpoiTempsSerializer(canva, many=True)   
        return Response(serializer.data)



# Teacher serializer ::::::::::::::::
@api_view(['GET',])
def teacher_serializer_list(request):
    teachers = Enseignant.objects.all()

    if request.method == 'GET':
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)



# classroom serializer ::::::::::::::::
@api_view(['GET',])
def classroom_serializer_list(request):
    classrooms = Salle.objects.all()

    if request.method == 'GET':
        serializer = ClassroomSerializer(classrooms, many=True)
        return Response(serializer.data)
