from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson import ObjectId
from app.utils import PyObjectId

# Schemas de estadísticas

class BaseStatisticBase(BaseModel):
    description: Optional[str] = None
    date_generation: Optional[str] = None
    type_statistic: Optional[PyObjectId] = None
    value: Optional[float] = None

class BaseStatisticCreate(BaseStatisticBase):
    pass

class BaseStatisticUpdate(BaseStatisticBase):
    pass

class BaseStatisticResponse(BaseStatisticBase):
    id: Optional[str] = Field(None, alias="_id")

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, PyObjectId):
            return str(v)
        return v

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str, PyObjectId: str},
    }

class StatisticCompetenceBase(BaseModel):
    description: Optional[str] = None
    date_generation: Optional[str] = None
    type_statistic: Optional[PyObjectId] = None
    value: Optional[float] = None
    average_score: Optional[float] = None
    matches_completed: Optional[int] = None
    record_score: Optional[int] = None
    total_parties: Optional[int] = None
    competition_id: Optional[PyObjectId] = None

class StatisticCompetenceCreate(StatisticCompetenceBase):
    pass

class StatisticCompetenceUpdate(StatisticCompetenceBase):
    pass

class StatisticCompetenceResponse(StatisticCompetenceBase):
    id: Optional[str] = Field(None, alias="_id")

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, PyObjectId):
            return str(v)
        return v

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str, PyObjectId: str},
    }

class StatisticIndividualBase(BaseModel):
    description: Optional[str] = None
    date_generation: Optional[str] = None
    type_statistic: Optional[PyObjectId] = None
    value: Optional[float] = None
    fouls: Optional[int] = None
    games_played: Optional[int] = None
    points_scored: Optional[int] = None
    athlete_id: Optional[PyObjectId] = None

class StatisticIndividualCreate(StatisticIndividualBase):
    pass

class StatisticIndividualUpdate(StatisticIndividualBase):
    pass

class StatisticIndividualResponse(StatisticIndividualBase):
    id: Optional[str] = Field(None, alias="_id")

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, PyObjectId):
            return str(v)
        return v

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str, PyObjectId: str},
    }

class StatisticTeamBase(BaseModel):
    description: Optional[str] = None
    date_generation: Optional[str] = None
    type_statistic: Optional[PyObjectId] = None
    value: Optional[float] = None
    games_played: Optional[int] = None
    games_drawn: Optional[int] = None
    matches_lost: Optional[int] = None
    matches_won: Optional[int] = None
    points: Optional[int] = None
    team_id: Optional[PyObjectId] = None

class StatisticTeamCreate(StatisticTeamBase):
    pass

class StatisticTeamUpdate(StatisticTeamBase):
    pass

class StatisticTeamResponse(StatisticTeamBase):
    id: Optional[str] = Field(None, alias="_id")

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, PyObjectId):
            return str(v)
        return v

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str, PyObjectId: str},
    }

class StatisticSeasonBase(BaseModel):
    description: Optional[str] = None
    date_generation: Optional[str] = None
    type_statistic: Optional[PyObjectId] = None
    value: Optional[float] = None
    most_fouls: Optional[PyObjectId] = None
    most_red_cards: Optional[PyObjectId] = None
    most_yellow_cards: Optional[PyObjectId] = None
    top_assistant: Optional[PyObjectId] = None
    top_scorer: Optional[PyObjectId] = None
    season_id: Optional[PyObjectId] = None

class StatisticSeasonCreate(StatisticSeasonBase):
    pass

class StatisticSeasonUpdate(StatisticSeasonBase):
    pass

class StatisticSeasonResponse(StatisticSeasonBase):
    id: Optional[str] = Field(None, alias="_id")

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, PyObjectId):
            return str(v)
        return v

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str, PyObjectId: str},
    }
