from django.contrib.auth.mixins import AccessMixin
from django.db.models.query_utils import Q

from src.base.selectors import get_categories


class AuthorRequiredMixin(AccessMixin):
    """Проверяет автор ли пользователь"""
    def dispatch(self, request, *args, **kwargs):
        if request.user == self.get_object().author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()


class RecipeFilterMixin:
    """Фильтрует и сортирует рецепты согласно запросу пользователя"""
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        q = request.GET.get("q", "")
        order_by = request.GET.get("order-by", "-pub_date")
        category_id = request.GET.get("category", "")
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        if category_id:
            queryset.filter(category_id=category_id)
        queryset = queryset.order_by(order_by)
        self.object_list = queryset
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        context["order_by"] = self.request.GET.get("order-by", "-pub_date")
        context["categories"] = get_categories()
        if self.request.GET.get("category"):
            context["category_id"] = int(self.request.GET.get("category"))
        return context
