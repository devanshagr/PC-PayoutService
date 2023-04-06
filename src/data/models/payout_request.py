from pydantic import BaseModel, Field, validator

class PayoutRequest(BaseModel):
    strike: float
    tMax: float
    year: int