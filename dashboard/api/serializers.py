from rest_framework import serializers
from dashboard.models import EmploiTemps, Module, Periode, Enseignant, Salle
from django.contrib.auth.models import User




class UserSerializer(serializers.ModelSerializer):
    modules = serializers.StringRelatedField()
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'modules']


class PeriodeSerializer(serializers.ModelSerializer):
    class  Meta:
        model = Module
        fields = '__all__'




class EmpoiTempsSerializer(serializers.ModelSerializer):

    class Meta:
        model= EmploiTemps
        #fields = ['peride_one', 'first_first', 'first_second', 'first_third', 'first_forth', 'second_first', 'second_second', 'second_third', 'second_forth', 'third_first', 'third_second', 'third_third', 'third_forth', 'forth_first', 'forth_second', 'forth_third', 'forth_forth', 'fifth_first', 'fifth_second', 'fifth_third', 'fifth_forth']
        fields = '__all__'
        depth = 3



# class CanvasSerializer(serializers.ModelSerializer):
#     class  Meta:
#         model = CanvasTimeTable
#         fields = '__all__'
#         depth = 1


class ModuleSerializer(serializers.ModelSerializer):
    # canvas = CanvasSerializer(many=True)
    semestre = serializers.CharField(source="get_semestre_display")
    class  Meta:
        model = Module
        fields = ['code', 'slug', 'designation', 'unite', 'credit', 'coeff', 'active', 'semestre', 'cours', 'td', 'tp', 'niveau']
        depth = 2

    # def create(self, validated_data):
    #     canvas = validated_data.pop('canvas')
    #     module = Module.objects.create(**validated_data)
    #     for canva in canvas:
    #         CanvasTimeTable.objects.create(modules=module, **canva)
    #     return module
    


class TeacherSerializer(serializers.ModelSerializer):
    
    class  Meta:
        model = Enseignant
        fields = '__all__'



class ClassroomSerializer(serializers.ModelSerializer):
    bloc = serializers.CharField(source="get_bloc_display")
    type_of = serializers.CharField(source="get_type_of_display")

    
    class  Meta:
        model = Salle
        fields = ['bloc', 'design', 'type_of', 'active', 'is_available']



