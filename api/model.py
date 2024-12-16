from pydantic import BaseModel

class CountryFlightData(BaseModel):
    country: str
    flights: str
