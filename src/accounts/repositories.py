from django.contrib.auth import get_user_model

from src.base.repositories import ModelRepository
from src.accounts.models import Follower


class UserRepository(ModelRepository):
    model = get_user_model()


class FollowerRepository(ModelRepository):
    model = Follower
