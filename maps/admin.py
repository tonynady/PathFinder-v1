from django.contrib import admin
from django.contrib.sessions.models import Session
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth import get_user_model

# from django.contrib.auth.admin import UserAdmin
from .models import Robot, Project, ProjectData, MyUser
# UserModel = get_user_model()


# class CustomUserCreationForm(UserCreationForm):

#     class Meta(UserCreationForm.Meta):
#         model = MyUser
#         fields = UserCreationForm.Meta.fields + ('phone', 'image',)

# class CustomUserChangeForm(UserChangeForm):

#     class Meta(UserChangeForm.Meta):
#         model = MyUser

class UserAdmin(BaseUserAdmin):
    # form = CustomUserChangeForm
    # add_form = CustomUserCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "phone", "image")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    BaseUserAdmin.search_fields += ("phone",)


# Register your models here.
admin.site.register(MyUser, UserAdmin)
admin.site.register(Session)
admin.site.register(Robot)
admin.site.register(Project)
admin.site.register(ProjectData)

