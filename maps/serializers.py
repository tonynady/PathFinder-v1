from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth import get_user_model

from .models import Project, ProjectData, Robot, CameraFrame

UserModel = get_user_model()

class RobotPublicSerializer(serializers.Serializer):
    robot_id = serializers.IntegerField(read_only=True)
    robot_name = serializers.CharField(read_only=True)
    ip_address = serializers.CharField(read_only=True)

class UserPublicSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)

class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            validators=[UniqueValidator(queryset=UserModel.objects.all())]
            )
    username = serializers.CharField(
            validators=[UniqueValidator(queryset=UserModel.objects.all())]
            )
    password = serializers.CharField(write_only=True)
    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'], 
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        return user
    class Meta:
        model = UserModel
        fields = [
            'id', 
            'first_name', 
            'last_name', 
            'username', 
            'email', 
            'password',
        ]


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            validators=[UniqueValidator(queryset=UserModel.objects.all())]
            )
    username = serializers.CharField(
            validators=[UniqueValidator(queryset=UserModel.objects.all())]
            )
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField(validators=[UniqueValidator(queryset=UserModel.objects.all())], allow_null=True, required=False)
        
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        # if password is not None:
        #     instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = UserModel
        fields = [
            'id', 
            'first_name', 
            'last_name', 
            'username', 
            'email', 
            'password',
            'phone',
            'image',
        ]

class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(read_only=True)
    class Meta:
        model = UserModel
        fields = [
            'id',
            'username',
            'password',
            'email',
        ]

class ProjectSerializer(serializers.ModelSerializer):
    # user = serializers.CharField(read_only=True)
    user = UserPublicSerializer(read_only=True)
    robot = RobotPublicSerializer(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Project
        fields = [
            'project_id',
            'user',
            'robot',
            'project_name',
            'is_done',
            'is_working',
            'control_type',
            'created',
            'last_updated',
            'project_address',
            'map',
        ]

class CreateUpdateProjectSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Project
        fields = [
            'project_id',
            'user',
            'robot',
            'project_name',
            'control_type',
            'project_address',
            'created',
        ]

class ProjectDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectData
        fields = '__all__'
        # fields = [
        #     'project_data_id',
        #     'project',
        #     'x_position',
        #     'y_position',
        #     'angle',
        #     'speed',
        #     'temperature',
        #     'humidity',
        #     'gas_type',
        #     'gas_reading',
        #     'control_type',
        #     'time_collected',
        # ]

class RobotCreateUpdateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    is_assigned = serializers.BooleanField(read_only=True)
    at_maintainance = serializers.BooleanField(read_only=True)
    class Meta:
        model = Robot
        fields = [
            'robot_id',
            'user',
            'robot_name',
            'is_assigned',
            'at_maintainance',
            'robot_image',
            'ip_address',
        ]
class RobotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Robot
        fields = '__all__'


class CameraFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraFrame
        fields = [
            'camera_frame_id',
            'project',
            'frame',
        ]