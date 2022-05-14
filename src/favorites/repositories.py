from src.base.repositories import ModelRepository
from src.favorites.models import Favorites


class FavoritesRepository(ModelRepository):
    model = Favorites
