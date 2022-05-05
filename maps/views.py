from rest_framework import generics, mixins, authentication, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import authenticate, login, logout, get_user_model
UserModel = get_user_model()

from .models import Project, ProjectData, Robot, CameraFrame
# from .permissions import IsProjectDoneOrWorking
from .serializers import (
    ProjectSerializer,
    CreateUpdateProjectSerializer,
    ProjectDataSerializer, 
    RobotSerializer, 
    UserSerializer,
    UserLoginSerializer,
    #CameraFrameSerializer,
)

from django.shortcuts import render
def lobby(request):
    return render(request, 'maps/lobby.html')


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

class UserAccountView(generics.RetrieveAPIView):
    '''
    Get the logged in user's account details.
    '''
    serializer_class = UserSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        instance = UserModel.objects.get(pk=request.user.pk)
        print(f"THe instance is {instance}")
        serializer = UserSerializer(instance)
        return Response(serializer.data)

class UserDetailAPIView(generics.RetrieveAPIView):
    '''
    Get the details of any user. Only superusers can access this view.
    '''
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    ]

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        if self.request.user.is_superuser:
            return qs

            
class UserListAPIView(generics.ListAPIView):
    '''
    Get a list of all the users on the system.
    Only superusers can view this list.
    '''
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    ]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return self.list(request, *args, **kwargs)
        return Response(
            {"detail":"You are not allowed to view these data"},
            status=status.HTTP_403_FORBIDDEN
        )

class UpdateUserAPIView(generics.UpdateAPIView):
    '''
    Update the logged in user's object.
    The superusers only can update any user.
    '''
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    lookup_field = "pk"
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        if self.request.user.is_superuser:
            return qs
        return qs.filter(pk = self.request.user.pk)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

class DeleteUserAPIView(generics.DestroyAPIView):
    '''
    Delete the logged in user's object.
    The superusers only can delete any user.
    '''
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    lookup_field = "pk"
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        if self.request.user.is_superuser:
            return qs
        return qs.filter(pk = self.request.user.pk)

class LoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                data = UserLoginSerializer(user).data
                return Response(data)
            return Response(
                {'detail':'Your account has been disabled'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response({'detail':'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response(data={'detail':'Logged out'}, status=status.HTTP_204_NO_CONTENT)


class CreateProjectAPIView(generics.CreateAPIView):
    '''
    Create a Project for the logged in user.
    '''
    serializer_class = CreateUpdateProjectSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        robot = Robot.objects.get(robot_id = instance.robot.robot_id)
        robot.is_assigned= True
        robot.save()


class ProjectListAPIView(generics.ListAPIView):
    '''
    Get a list of all the projects of a certain user.
    If the user is a superuser it return all the projects on the system.
    '''
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        if self.request.user.is_superuser:
            return qs
        return qs.filter(user = self.request.user)

class ProjectListByRobotMixinView(mixins.ListModelMixin, generics.GenericAPIView):
    '''
    Get all the projects performed by a certain robot. Only superusers can view them.
    '''
    serializer_class = ProjectSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    ]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.queryset = Project.objects.filter(robot_id=kwargs.get("robot_id"))
            return self.list(request, *args, **kwargs)
        return Response(
            {"detail":"You are not allowed to view these data"},
            status=status.HTTP_403_FORBIDDEN
        )

class ProjectDetailAPIView(generics.RetrieveAPIView):
    '''
    Get the details of a certain project of a certain user.
    The superusers only can view any project.
    '''
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'project_id'
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        if self.request.user.is_superuser:
            return qs
        return qs.filter(user = self.request.user)

class UpdateProjectAPIView(generics.UpdateAPIView):
    '''
    Update a project related to a certain user.
    The superusers only can update any project.
    '''
    queryset = Project.objects.all()
    serializer_class = CreateUpdateProjectSerializer
    lookup_field = "project_id"
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated] #IsProjectDoneOrWorking

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        if self.request.user.is_superuser:
            return qs
        return qs.filter(user = self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_done or instance.is_working:
            return Response(
            data={"detail": "You can't update a finished or working project"}, 
            status=status.HTTP_403_FORBIDDEN
        )
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

class DeleteProjectAPIView(generics.DestroyAPIView):
    '''
    Delete a project related to a certain user.
    The superusers can delete any project.
    '''
    queryset = Project.objects.all()
    lookup_field = "project_id"
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        if self.request.user.is_superuser:
            return qs
        return qs.filter(user = self.request.user)

    def perform_destroy(self, instance):
        robot = Robot.objects.get(robot_id = instance.robot.robot_id)
        robot.is_assigned = False
        robot.save()
        instance.delete()


class CreateRobotAPIView(generics.CreateAPIView):
    '''
    Create a New Robot. Only admins can create robots.
    '''
    serializer_class = RobotSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    ]

class RobotListAPIView(generics.ListAPIView):
    '''
    Get a list of all the robots on the system.
    Any authenticated user can view them.
    '''
    queryset = Robot.objects.all()
    serializer_class = RobotSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class RobotDetailAPIView(generics.RetrieveAPIView):
    '''
    Get the details of a certain robot.
    Any authenticated user can view these data.
    '''
    queryset = Robot.objects.all()
    serializer_class = RobotSerializer
    lookup_field = 'robot_id' #pk and then must modify the url param.
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class UpdateRobotAPIView(generics.UpdateAPIView):
    '''
    Update a certain robot. Only admins can update robots.
    '''
    queryset = Robot.objects.all()
    serializer_class = RobotSerializer
    lookup_field = "robot_id"
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    ]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

class DeleteRobotAPIView(generics.DestroyAPIView):
    '''
    Delete a Robot. Only admins can delete robots.
    '''
    queryset = Robot.objects.all()
    lookup_field = "robot_id"
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    ]


class ProjectDataListMixinView(mixins.ListModelMixin, generics.GenericAPIView):
    '''
    Get the all the data collected during a certain project.
    The project must belong to the logged in user. 
    Only the superusers are allowed to view any data.
    '''
    serializer_class = ProjectDataSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        proj = Project.objects.get(project_id=kwargs.get("project_id"))
        if proj in Project.objects.filter(user=request.user) or request.user.is_superuser:
            self.queryset = ProjectData.objects.filter(project_id=kwargs.get("project_id"))
            return self.list(request, *args, **kwargs)
        return Response(
            data={"detail": "You are not allowed to view these data"}, 
            status=status.HTTP_403_FORBIDDEN
        )

class ProjectDataWithinRange(generics.CreateAPIView):
    '''
    Get the all the Data collected during a certain project within certain time range.
    The project must belong to the logged in user. 
    Only the superusers are allowed to view any data.
    '''
    serializer_class = ProjectDataSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        proj = Project.objects.get(project_id=kwargs.get("project_id"))
        if proj in Project.objects.filter(user=request.user) or request.user.is_superuser:
            queryset = ProjectData.objects.filter(
                project_id=kwargs.get("project_id"),
                time_collected__range=(data["inst1"], data["inst2"])
            )
            data = ProjectDataSerializer(queryset, many=True).data
            return Response(data)
        return Response(
            data={"detail": "You are not allowed to view these data"}, 
            status=status.HTTP_403_FORBIDDEN
        )

class ProjectPoisonousData(generics.ListCreateAPIView):
    serializer_class = ProjectDataSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        '''
        Get the all the Data collected during a certain project with certain poisonous gas readings.
        A logged in user can access only the data of his own projects. 
        Only superusers can view any data.
        '''
        data = request.data
        proj = Project.objects.get(project_id=kwargs.get("project_id"))
        if proj in Project.objects.filter(user=request.user) or request.user.is_superuser:
            queryset = ProjectData.objects.filter(
                project_id=kwargs.get("project_id"), 
                gas_type__in=data["gas_type"]
            )
            data = ProjectDataSerializer(queryset, many=True).data
            return Response(data)
        return Response(
            data={"detail": "You are not allowed to view these data"}, 
            status=status.HTTP_403_FORBIDDEN
        )

    def get(self, request, *args, **kwargs):
        '''
        Get the all the Data collected during a certain project with poisonous readings.
        A logged in user can access only the data of his own projects. 
        Only superusers can view any data.
        '''
        data = request.data
        proj = Project.objects.get(project_id=kwargs.get("project_id"))
        if proj in Project.objects.filter(user=request.user) or request.user.is_superuser:
            self.queryset = ProjectData.objects.filter(
                project_id=kwargs.get("project_id"), 
                gas_reading__isnull=False
            )
            data = ProjectDataSerializer(self.queryset, many=True).data
            return Response(data)
        return Response(
            data={"detail": "You are not allowed to view these data"}, 
            status=status.HTTP_403_FORBIDDEN
        )




# class ProjectFramesMixinView(mixins.ListModelMixin, generics.GenericAPIView):
#     '''
#     Get the all the frames collected during a certain project.
#     A logged in user can access only the frames of his own projects. 
#     Only superusers can view any frames.
#     '''
#     serializer_class = CameraFrameSerializer
#     authentication_classes = [authentication.SessionAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         proj = Project.objects.get(project_id=kwargs.get("project_id"))
#         if proj in Project.objects.filter(user=request.user) or request.user.is_superuser:
#             self.queryset = CameraFrame.objects.filter(project_id=kwargs.get("project_id"))
#             return self.list(request, *args, **kwargs)
#         return Response(
#             data={"detail": "You are not allowed to view these data"}, 
#             status=status.HTTP_403_FORBIDDEN
#         )
