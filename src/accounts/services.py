from django.shortcuts import redirect

from src.accounts.repositories import FollowerRepository, UserRepository


def add_user_to_subscriptions(request, pk):
    subscriber = request.user
    user = UserRepository.get_object_or_404(pk=pk)
    FollowerRepository.get_or_create(user=user, subscriber=subscriber)
    return redirect(user)


def remove_user_from_subscriptions(request, pk):
    subscriber = request.user
    user = UserRepository.get_object_or_404(pk=pk)
    follower = FollowerRepository.get_object_or_none(user=user, subscriber=subscriber)
    if follower:
        follower.delete()
    return redirect(user)


def is_followed(request, user):
    """Проверяет подписан ли текущий пользователь на данного."""
    if request.user.is_active:
        return user.followers.filter(subscriber=request.user).exists()
    return False
