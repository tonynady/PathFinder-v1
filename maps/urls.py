from django.urls import path

from .views import(
    ProjectDataListMixinView, ProjectListByRobotMixinView, 
    RobotListAPIView, ProjectListAPIView, RobotDetailAPIView, 
    ProjectDetailAPIView, ProjectDataPoisonous, ProjectDataWithinRange, 
    RegisterAPIView, LoginView, LogoutView, 
    ProjectCreateAPIView, ProjectDeleteAPIView, RobotCreateAPIView, RobotDeleteAPIView,
    ProjectUpdateAPIView, RobotUpdateAPIView, UserUpdateAPIView, UserDeleteAPIView,
    UserListAPIView, UserAccountView, UserDetailAPIView, #ProjectFramesMixinView,
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('users/', UserListAPIView.as_view()),
    path('user/account/', UserAccountView.as_view()),
    path('user/<int:pk>/', UserDetailAPIView.as_view()),
    path('update/user/<int:pk>/', UserUpdateAPIView.as_view()),
    path('delete/user/<int:pk>/', UserDeleteAPIView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),

    path('create/project/', ProjectCreateAPIView.as_view()),
    path('projects/', ProjectListAPIView.as_view()),
    path('projects/robot/<int:robot_id>/', ProjectListByRobotMixinView.as_view()),
    path('project/<int:project_id>/', ProjectDetailAPIView.as_view()),
    path('update/project/<int:project_id>/', ProjectUpdateAPIView.as_view()),
    path('delete/project/<int:project_id>/', ProjectDeleteAPIView.as_view()),

    path('create/robot/', RobotCreateAPIView.as_view()),
    path('robots/', RobotListAPIView.as_view()),
    path('robot/<int:robot_id>/', RobotDetailAPIView.as_view()), #pk and then must modify the view lookup.
    path('update/robot/<int:robot_id>/', RobotUpdateAPIView.as_view()),
    path('delete/robot/<int:robot_id>/', RobotDeleteAPIView.as_view()),

    path('project/<int:project_id>/data/', ProjectDataListMixinView.as_view()),
    path('project/<int:project_id>/data/range/', ProjectDataWithinRange.as_view()),
    path('project/<int:project_id>/data/poisonous/', ProjectDataPoisonous.as_view()), #Get & Post



    # path('frames/project/<int:project_id>/', ProjectFramesMixinView.as_view()),
]