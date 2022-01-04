from django.db.models.query_utils import Q

from src.base.selectors import RecipeSelector, get_user_subscriptions


class HomepageService:

    __slots__ = 'request',

    def __init__(self, request) -> None:
        self.request = request

    @staticmethod
    def _build_context(user_recipes, recent_recipes, user_subscriptions):
        return {
            "user_recipes": user_recipes,
            "recent_recipes": recent_recipes,
            "user_subscriptions": user_subscriptions
        }

    def execute(self):
        user_recipes = RecipeSelector.get_user_recipes(user=self.request.user, limit=4)
        recent_recipes = RecipeSelector.get_recent_recipes(limit=2)
        user_subscriptions = get_user_subscriptions(user=self.request.user, limit=4)
        return self._build_context(user_recipes, recent_recipes, user_subscriptions)


def get_recipes_by_fitler(request):
    q = request.GET.get("q", "")
    queryset = RecipeSelector.get_published_recipes().filter(Q(title__icontains=q) | Q(description__icontains=q))
    return queryset
