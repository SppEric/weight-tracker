"use client";
import { useEffect, useState } from "react";

export default function Home() {
  const [weights, setWeights] = useState<any[]>([]);
  const [insights, setInsights] = useState<any>({});

  // Define defaults
  // Default user_id for testing, TODO: implement authentication
  const user_id = 1; 
  // Default server URL for testing, TODO: use environment variable
  const server_url = "http://localhost:5000";

  async function fetchWeights() {
    try {
      const response = await fetch(`${server_url}/weights?user_id=${user_id}`);
      if (!response.ok) {
        throw new Error(`Error fetching weights: ${response.statusText}`);
      }
      const data = await response.json();
      setWeights(data);
    } catch (error) {
      console.error("Failed to fetch weights:", error);
    }
  }

  async function fetchInsights() {
    try {
      const response = await fetch(`${server_url}/insights?user_id=${user_id}`);
      if (!response.ok) {
        throw new Error(`Error fetching insights: ${response.statusText}`);
      }
      const data = await response.json();
      setInsights(data);
    } catch (error) {
      console.error("Failed to fetch insights:", error);
    }
  }
  
  useEffect(() => {
    // Fetch weights and insights on component mount only
    fetchWeights();
    fetchInsights();
  }, []);

  return (
    <div className="max-w-lg mx-auto mt-8 p-4">
      <h1 className="text-2xl font-bold mb-4">Weight Tracker</h1>

      <div className="mb-6">
        <h2 className="text-lg font-semibold mb-2">Insights</h2>
        {Object.keys(insights).length > 0 ? (
          <ul>
            {Object.entries(insights).map(([key, value]) => (
              <li key={key}>
                {key.replace(/_/g, " ")}: {String(value)}
              </li>
            ))}
          </ul>
        ) : (
          <span>No insights.</span>
        )}
      </div>

      <div>
        <h2 className="text-lg font-semibold mb-2">Recent Weights</h2>
        {weights.length > 0 ? (
          <ul>
            {weights.map((entry: any, idx: number) => (
              <li key={idx}>
                {entry.entry_date}: <b>{entry.weight} lbs</b>
              </li>
            ))}
          </ul>
        ) : (
          <span>No weights logged.</span>
        )}
      </div>
    </div>
  );
}
