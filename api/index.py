from fastapi import FastAPI, HTTPException
from typing import List
import requests
import os

from api.model import CountryFlightData

### Create FastAPI instance with custom docs and openapi url
app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

FLIGHT_API_URL = "https://api.flightapi.io/compschedule"
API_KEY = os.getenv("FLIGHT_API_KEY")

@app.get("/api/arrivals/{iata_code}", response_model=List[CountryFlightData])
async def get_arrivals(iata_code: str):
    """
    Endpoint to get arrivals for a specific iata code.
    :param iata_code: IATA code of the target Airport
    :return: List of countries with number of arrivals today for the target Airport
    """

    # Validate IATA code. It should be 3 alpha-numeric characters
    if len(iata_code) != 3 or not iata_code.isalpha():
        raise HTTPException(status_code=400, detail="Invalid IATA code")

    # print(f"query for IATA code: {iata_code}")

    try:
        # Construct the full API request URL. day=1(today)
        url = f"{FLIGHT_API_URL}/{API_KEY}?mode=arrivals&day=1&iata={iata_code}"

        response = requests.get(url)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to retrieve data from external API")

        flight_data = response.json()

        # print("Response: ", flight_data)

        # Process the flight data to aggregate flights per country
        country_flight_map = {}
        # The API endpoints send the list of pages.
        for page in flight_data:
            # List of arrivals
            arrivals = (
                page.get("airport")
                .get("pluginData")
                .get("schedule")
                .get("arrivals")
                .get("data")
            )

            # Country of origin for the arrivals
            for arrival in arrivals:
                country = (
                    arrival.get("flight")
                    .get("airport")
                    .get("origin")
                    .get("position")
                    .get("country")
                    .get("name")
                )

                if country:
                    country_flight_map[country] = country_flight_map.get(country, 0) + 1

        # print(f"Found {len(country_flight_map)} flights for {iata_code}")
        result = [
            CountryFlightData(country=country, flights=count)
            for country, count in sorted(country_flight_map.items())
        ]

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")