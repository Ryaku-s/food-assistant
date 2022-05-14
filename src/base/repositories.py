from typing import Optional, Type

from django.db.models import Model, QuerySet
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()


class ModelRepository:
    model: Type[Model]

    @classmethod
    def all(cls, limit: Optional[int] = None) -> QuerySet:
        queryset = cls.model.objects.all()
        return queryset[:limit] if limit else queryset

    @classmethod
    def filter(cls, limit: Optional[int] = None, *args, **kwargs) -> QuerySet:
        queryset = cls.model.objects.filter(*args, **kwargs)
        return queryset[:limit] if limit else queryset

    @classmethod
    def get(cls, *args, **kwargs) -> Model:
        return cls.model.objects.get(*args, **kwargs)

    @classmethod
    def get_object_or_none(cls, *args, **kwargs) -> Optional[Model]:
        try:
            obj = cls.model.objects.get(*args, **kwargs)
        except cls.model.DoesNotExist:
            return None
        return obj

    @classmethod
    def get_object_or_404(cls, *args, **kwargs) -> Model:
        return get_object_or_404(cls.model, *args, **kwargs)

    @classmethod
    def get_or_create(cls, **kwargs) -> Model:
        return cls.model.objects.get_or_create(**kwargs)[0]

    @classmethod
    def none(cls):
        return cls.model.objects.none()
