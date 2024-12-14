from django.core.exceptions import PermissionDenied

class HavePermissionsMixin:
    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user and not request.user.is_moderator:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)