from fastapi import FastAPI
from typing import List

from api.model import CountryFlightData

### Create FastAPI instance with custom docs and openapi url
app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

@app.get("/api/arrivals/{iata_code}", response_model=List[CountryFlightData])
async def get_arrivals(iata_code: str):
    """
    Endpoint to get arrivals for a specific iata code.
    :param iata_code: IATA code of the target Airport
    :return: List of countries with number of arrivals today for the target Airport
    """

    result = [
        CountryFlightData(country="Thailand", flights="4"),
        CountryFlightData(country="Cambodia", flights="2"),
        CountryFlightData(country="Brunei", flights="1"),
    ]

    return result
