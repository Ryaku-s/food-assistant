from typing import Any, Dict
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect

from src.base.services import build_context_data
from src.accounts.models import User
from src.accounts.repositories import FollowerRepository, UserRepository
from src.catalog.repositories import RecipeRepository


def add_user_to_subscriptions(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    subscriber = request.user
    user = UserRepository.get_object_or_404(pk=pk)
    FollowerRepository.get_or_create(user=user, subscriber=subscriber)
    return redirect(user)


def remove_user_from_subscriptions(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    subscriber = request.user
    user = UserRepository.get_object_or_404(pk=pk)
    follower = FollowerRepository.get_object_or_none(user=user, subscriber=subscriber)
    if follower:
        follower.delete()
    return redirect(user)


def get_profile_detail_context_data(base_context: Dict[str, Any], request: HttpRequest, owner: User) -> Dict[str, Any]:
    return build_context_data(
        base_context,
        is_followed=_is_followed(request.user, owner),
        recipes=RecipeRepository.filter(
            2,
            author__id=owner.id
        )
    )


def _is_followed(user: User, owner: User) -> bool:
    if user.is_active:
        return owner.followers.filter(subscriber=user).exists()
    return False
