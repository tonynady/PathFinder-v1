# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT /Users_Images/user_<id>/<filename>
    return 'Users_Images/user_{0}/{1}'.format(instance.id, filename)
class MyUser(AbstractUser):
    phone = models.CharField(max_length=12, unique=True, null=True, blank=True)
    image = models.ImageField(upload_to=user_directory_path, default="default_user.png", null=True, blank=True)


def robot_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT /Robots_Images/robot_<id>/<filename>
    return 'Robots_Images/robot_{0}/{1}'.format(instance.robot_id, filename)
class Robot(models.Model):
    robot_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    robot_name = models.CharField(max_length=20)
    is_assigned = models.BooleanField(default=False)
    at_maintainance = models.BooleanField(default=False)
    robot_image = models.ImageField(upload_to=robot_directory_path, default="default_robot.png", null=True, blank=True)
    ip_address = models.GenericIPAddressField(default="0.0.0.0")

    class Meta:
        managed = True
        db_table = 'Robot'
    
    def __str__(self):
        return f"{self.robot_name}"


def map_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT /maps/project_<id>_map/<filename>
    return 'maps/project_{0}_map/{1}'.format(instance.robot_id, filename)
class Project(models.Model):
    project_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    robot = models.ForeignKey(Robot, on_delete=models.SET_NULL, null=True)
    project_name = models.CharField(max_length=20)
    is_done = models.BooleanField(default=False)
    is_working = models.BooleanField(default=False)
    control_choices = (('Manual', 'Manual'), ('Automatic', 'Automatic'))
    control_type = models.CharField(max_length=15, choices=control_choices)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    map = models.ImageField(upload_to=map_directory_path, null=True, blank=True)
    project_address = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'Project'


class ProjectData(models.Model):
    project_data_id = models.BigAutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    x_position = models.DecimalField(max_digits=10, decimal_places=5)
    y_position = models.DecimalField(max_digits=10, decimal_places=5)
    angle = models.DecimalField(max_digits=10, decimal_places=5, )
    speed = models.DecimalField(max_digits=10, decimal_places=5)
    temperature = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    humidity = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    gas_type = models.CharField(max_length=100, blank=True, null=True)
    gas_reading = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    control_type = models.CharField(max_length=15)
    time_collected = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'Project_Data'


class CameraFrame(models.Model):
    camera_frame_id = models.BigAutoField(primary_key=True)
    project = models.ForeignKey(Project, models.DO_NOTHING)
    frame = models.BinaryField()

    class Meta:
        managed = True
        db_table = 'Camera_Frame'








# robot_status_choices = (('Available', 'Available'), ('Working', 'Working'), ('At Maintainance', 'At Maintainance'))
# robot_status = models.CharField(max_length=20, default="Available", choices=robot_status_choices)

# project_status_choices = (('Waiting', 'Waiting'), ('Working', 'Working'), ('Done', 'Done'))
# project_status = models.CharField(max_length=15, default="Waiting", choices=project_status_choices)

# class User(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     f_name = models.CharField(max_length=50)
#     l_name = models.CharField(max_length=50)
#     email = models.CharField(max_length=500, blank=True, null=True)
#     phone = models.CharField(max_length=15, blank=True, null=True)
#     username = models.CharField(max_length=50)
#     password = models.TextField()
#     user_image = models.BinaryField(blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'User'











# # This is an auto-generated Django model module.
# # You'll have to do the following manually to clean this up:
# #   * Rearrange models' order
# #   * Make sure each model has one field with primary_key=True
# #   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
# #   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# # Feel free to rename the models, but don't rename db_table values or field names.
# from django.conf import settings
# from django.contrib.auth.models import AbstractUser
# from django.db import models
# from django.contrib.auth.models import User

# # class MyUser(AbstractUser):
# #     phone = models.CharField(max_length=15, blank=True, null=True)
# #     user_image = models.BinaryField(blank=True, null=True)

# #     # class Meta(AbstractUser.Meta):
# #     #     swappable = "AUTH_USER_MODEL"
    
# #     # class Meta:
# #     #     managed = True
# #     #     db_table = 'auth_user'


# class User(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     f_name = models.CharField(max_length=50)
#     l_name = models.CharField(max_length=50)
#     email = models.CharField(max_length=500, blank=True, null=True)
#     phone = models.CharField(max_length=15, blank=True, null=True)
#     username = models.CharField(max_length=50)
#     password = models.TextField()
#     user_image = models.BinaryField(blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'User'

# class CameraFrame(models.Model):
#     project = models.ForeignKey('Project', models.DO_NOTHING, default=1)
#     camera_frame_id = models.BigAutoField(primary_key=True)
#     frame = models.BinaryField()

#     class Meta:
#         managed = True
#         db_table = 'Camera_Frame'


# class Project(models.Model):
#     user = models.ForeignKey('User', models.DO_NOTHING, default=1)
#     robot = models.ForeignKey('Robot', models.DO_NOTHING, default=1)
#     project_id = models.BigAutoField(primary_key=True)
#     project_name = models.CharField(max_length=100)
#     project_status = models.CharField(max_length=50)
#     control_type = models.CharField(max_length=50)
#     last_updated = models.DateTimeField(blank=True, null=True)
#     map = models.TextField(blank=True, null=True)  # This field type is a guess.

#     project_address = models.TextField(blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'Project'


# class ProjectData(models.Model):
#     project = models.ForeignKey(Project, models.DO_NOTHING, default=1)
#     project_data_id = models.BigAutoField(primary_key=True)
#     x_position = models.DecimalField(max_digits=10, decimal_places=5)
#     y_position = models.DecimalField(max_digits=10, decimal_places=5)
#     angle = models.DecimalField(max_digits=10, decimal_places=5)
#     speed = models.DecimalField(max_digits=10, decimal_places=5)
#     temperature = models.DecimalField(max_digits=10, decimal_places=5)
#     humidity = models.DecimalField(max_digits=10, decimal_places=5)
#     gas_type = models.CharField(max_length=100, blank=True, null=True)
#     gas_reading = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
#     control_type = models.CharField(max_length=50)
#     time_collected = models.DateTimeField()

#     class Meta:
#         managed = True
#         db_table = 'Project_Data'


# class Robot(models.Model):
#     robot_id = models.BigAutoField(primary_key=True)
#     robot_name = models.CharField(max_length=50)
#     robot_status = models.CharField(max_length=50)
#     robot_image = models.BinaryField(blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'Robot'



