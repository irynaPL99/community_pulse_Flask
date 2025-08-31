from pydantic import BaseModel, Field, ConfigDict

# Используется для валидации данных при создании новой категории.
class CategoryCreate(BaseModel):
    """Schema for creating a new category."""
    name: str = Field(..., min_length=1, max_length=100, description="Name of the category")

# Отдельная схема для обновления, чтобы избежать дублирования логики (хотя можно объединить с CategoryCreate,
# если обновление и создание имеют одинаковые требования).
class CategoryUpdate(BaseModel):
    """Schema for updating an existing category."""
    name: str = Field(..., min_length=1, max_length=100, description="Updated name of the category")


# Используется для формирования ответа с данными категории,
# включая id и name, с поддержкой преобразования из SQLAlchemy-моделей.
class CategoryResponse(BaseModel):
    """Schema for responding with category details."""
    id: int
    name: str = Field(..., min_length=1, max_length=100, description="Name of the category")

    # позволяет преобразовывать SQLAlchemy-модели в Pydantic-модели:
    model_config = ConfigDict(
        from_attributes=True
    )

# новая схема для унифицированного ответа с сообщением и данными
class CategoryUpdateResponse(BaseModel):
    """Schema for the full response including message."""
    message: str = Field(..., description="Success message")
    data: CategoryResponse

class CategoryDeleteResponse(BaseModel):
    """Schema for the response after deleting a category."""
    message: str = Field(..., description="Success message")
    id: int = Field(..., description="ID of the deleted category")