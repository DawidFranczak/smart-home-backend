from django.db.models import Q, QuerySet

from device.models import Device


def get_available_for_user_device(model, user):
    return model.objects.filter(
        Q(home__users=user),
        Q(room__user=user) | Q(room__visibility="PU"),
    )


def get_all_available_for_user_device(user_id: int) -> QuerySet[Device]:
    return Device.objects.filter(
        Q(home__users=user_id),
        Q(room__user=user_id) | Q(room__visibility="PU"),
    )
