from django.contrib.auth.mixins import AccessMixin


class AuthorRequiredMixin(AccessMixin):
    """Проверяет автор ли пользователь"""
    def dispatch(self, request, *args, **kwargs):
        if request.user == self.get_object().author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()
