from django.shortcuts import redirect

from src.base.selectors import get_user_by_pk, get_or_create_follower


def add_user_to_subscriptions(request, pk):
    subscriber = request.user
    user = get_user_by_pk(pk)
    get_or_create_follower(user, subscriber)
    return redirect(user)


def remove_user_from_subscriptions(request, pk):
    subscriber = request.user
    user = get_user_by_pk(pk)
    get_or_create_follower(user, subscriber).delete()
    return redirect(user)


def is_followed(request, user):
    """Проверяет подписан ли текущий пользователь на данного."""
    return user.followers.filter(subscriber=request.user).exists()
