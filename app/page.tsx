'use client';

import { useState } from "react";
import axios from "axios";

// Flights API response data model
interface FlightResult {
  country: string;
  flights: number;
}

export default function Home() {
  const [iataCode, setAirportCode] = useState<string>("");
  const [results, setResults] = useState<FlightResult[]>([]);
  const [error, setError] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  // Function to fetch flight data
  const fetchFlights = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validate airport IATA code. It should be 3 alpha-numeric characters
    if (iataCode.length !== 3 || !/^[A-Z]+$/.test(iataCode)) {
      setError("Please enter a valid 3-letter airport code");
      return;
    }

    // Reset previous state
    setLoading(true);
    setError("");
    setResults([]);

    // Call backend API endpoint to fetch data
    try {
      const response = await axios.get(
        `/api/arrivals/${iataCode}`
      );
      setResults(response.data);
    } catch (err: any) {
      setError(
        err.response?.data?.detail || "An error occurred fetching flight data"
      );
      console.error("Error details:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-8">
      {/* Container for the form and results */}
      <div className="max-w-3xl w-full p-6 absolute top-12 left-1/2 transform -translate-x-1/2 font-sans">

        {/* Title */}
        <h1 className="text-3xl font-bold mb-6 text-center">
          Flights by Country
        </h1>

        {/* Search Form */}
        <form onSubmit={fetchFlights} className="flex mb-6">
          <input
            type="text"
            value={iataCode}
            onChange={(e) => {
              const value = e.target.value.toUpperCase();
              setAirportCode(value);
              setError("");
            }}
            placeholder="Enter Airport Code (e.g., LAX)"
            maxLength={3}
            className="flex-grow p-3 text-lg border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <button
            type="submit"
            disabled={loading || iataCode.length !== 3}
            className="px-4 py-3 ml-2 bg-green-500 text-white rounded-r-md disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? "Searching..." : "Search"}
          </button>
        </form>

        {/* Error Message */}
        {error && <div className="text-red-500 mb-4 text-center">{error}</div>}

        {/* Loader */}
        {loading && (
          <div className="flex justify-center items-center h-24">
            <div className="border-4 border-t-4 border-gray-300 border-t-blue-500 w-12 h-12 rounded-full animate-spin"></div>
          </div>
        )}

        {/* Results Table */}
        {!loading && results.length > 0 && (
            <table className="min-w-full table-auto border-collapse mt-6 rounded-lg overflow-hidden">
              <thead>
              <tr className="bg-gray-100">
                <th className="px-4 py-2 text-left border-b border-r">Country</th>
                <th className="px-4 py-2 text-left border-b"># of Flights</th>
              </tr>
              </thead>
              <tbody>
              {results.map((row, index) => (
                  <tr key={index} className="bg-white">
                    <td className="px-4 py-2 border-b border-r">{row.country}</td>
                    <td className="px-4 py-2 border-b">{row.flights}</td>
                  </tr>
              ))}
              </tbody>
            </table>
        )}
      </div>
    </main>
  );
}
