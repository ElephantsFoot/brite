from pydantic import BaseModel


class MovieBase(BaseModel):
    title: str
    year: int | None = None


class MovieCreate(MovieBase):
    pass


class Movie(MovieBase):
    id: int
    description: str | None = None

    class ConfigDict:
        from_attributes = True
