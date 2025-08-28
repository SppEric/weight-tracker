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
    // Fetch weights on component mount only
    fetchWeights();
    fetchInsights();
  }, []);

  return (
    <div>
      <h1>Welcome to Weight Tracker!</h1>

      <h2> Key Insights </h2>
      {insights && Object.keys(insights).length > 0 ? (
        <ul>
          {Object.entries(insights).map(([key, value]) => (
            <li key={key}>
              {key}: {String(value)}
            </li>
          ))}
        </ul>
      ) : (
        <p>No insights available.</p>
      )}

      <h2>Your Recent Weights:</h2>
      {weights.length === 0 ? (
        <p>No weights logged yet.</p>
      ) : (
        <ul>
          {weights.map((entry: any, index: number) => (
            <li key={index}>
              Date: {entry.entry_date}, Weight: {entry.weight} lbs
            </li>
          ))}
        </ul>
      )}
      </div>
  );
}
