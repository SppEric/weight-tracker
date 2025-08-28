"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function LogPage() {
  const [weight, setWeight] = useState("");
  const router = useRouter();
  const userId = 1; // TEMPORARY

  const handleSubmit = async () => {
    if (!weight) return;
    await fetch("http://localhost:5000/weights", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, weight: parseFloat(weight) }),
    });
    setWeight("");
    router.push("/"); // Return to the main screen after logging!
  };

  return (
    <div className="p-4 mx-auto rounded-xl shadow space-y-4 max-w-md">
      <h2 className="text-lg font-semibold">Log Today's Weight</h2>
      <div className="flex space-x-2"></div>
      <input
        type="number"
        value={weight}
        onChange={(e) => setWeight(e.target.value)}
        placeholder="Enter weight"
        className="border rounded p-2 w-full"
        onKeyDown={(e) => {
          if (e.key === "Enter") handleSubmit();
        }}
        required
      />
      <button
        onClick={handleSubmit}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Submit
      </button>
    </div>
  );
}