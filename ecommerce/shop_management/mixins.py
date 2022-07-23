from django.core.exceptions import PermissionDenied


class IsSalesmanMixin:
    permission_denied_message = "شما اجازه دسترسی به این صفحه را ندارید."

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_salesman:
            return super(IsSalesmanMixin, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
