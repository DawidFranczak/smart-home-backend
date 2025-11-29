from django.db.models import Q


def get_available_for_user_device(model, user):
    return model.objects.filter(
        Q(home__users=user),
        Q(room__user=user) | Q(room__visibility="PU"),
    )
