from .models import Project

class IsProjectDoneOrWorking():
    """
    Permission fails if the project is done or still working.
    """
    def has_permission(self, request, view):
        project = Project.objects.get(project_id=view.kwargs['project_id'])
        if project.is_done or project.is_working:
            return False
        else: return True