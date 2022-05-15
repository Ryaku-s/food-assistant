from src.base.repositories import ModelRepository
from src.favorites.models import Favorites


class FavoritesRepository(ModelRepository):
    _model = Favorites
