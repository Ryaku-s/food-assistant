from django.utils import timezone


def get_avatar_upload_path(instance, file) -> str:
    return f"img/avatars/{instance.id}/{timezone.now().day}{timezone.now().month}{timezone.now().year}/{file}"


def get_recipe_image_upload_path(instance, file) -> str:
    return f"img/recipes/{instance.author.id}/{timezone.now().day}{timezone.now().month}{timezone.now().year}/{file}"


def get_direction_image_upload_path(instance, file) -> str:
    return f"img/directions/{instance.recipe.author.id}/\
        {timezone.now().day}{timezone.now().month}{timezone.now().year}/{file}"
