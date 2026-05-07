from __future__ import annotations

from pydantic import BaseModel, Field


class BudgetRange(BaseModel):
    """
    Represents an approximate numeric budget range.
    Interpreted consistently across the app (e.g., cost-for-two).
    """

    min: float | None = Field(default=None, ge=0)
    max: float | None = Field(default=None, ge=0)


class UserPreferences(BaseModel):
    location: str = Field(min_length=1, description="City/locality")
    budget: BudgetRange | None = None
    cuisines: list[str] = Field(default_factory=list)
    minimum_rating: float | None = Field(default=None, ge=0, le=5)
    additional_preferences: str | None = None

