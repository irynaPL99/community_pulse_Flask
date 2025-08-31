from pydantic import BaseModel, Field, ConfigDict

class QuestionCreate(BaseModel):
    question: str = Field(..., min_length=10, max_length=100)
    category_id: int = Field(..., description="ID of the category")


class QuestionResponse(BaseModel):
    id: int
    question: str = Field(..., min_length=10, max_length=100)
    category_id: int = Field(..., description="ID of the category")

    # позволяет преобразовывать SQLAlchemy-модели в Pydantic-модели:
    model_config = ConfigDict(
        from_attributes=True
    )