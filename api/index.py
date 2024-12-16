from fastapi import FastAPI

### Create FastAPI instance with custom docs and openapi url
app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")

@app.get("/api/helloFastApi")
def hello_fast_api():
    return {"message": "Hello from FastAPI"}


@app.get("/api/arrivals/{iata_code}")
async def get_arrivals(iata_code: str):
    """
    Endpoint to get arrivals for a specific iata code.
    :param iata_code: IATA code of the target Airport
    :return: List of countries with number of arrivals today for the target Airport
    """

    # Convert the dictionary to a list of CountryFlightData
    result = [
        {"country": "Thailand", "flights": "4" },
        {"country": "Cambodia", "flights": "2" },
        {"country": "Brunei", "flights": "1" },
    ]

    return result
