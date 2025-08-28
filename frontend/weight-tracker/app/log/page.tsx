"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function LogPage() {
  const [weight, setWeight] = useState("");
  const router = useRouter();
  const userId = 1; // TEMPORARY

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await fetch("http://localhost:5000/weights", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, weight: parseFloat(weight) }),
    });
    setWeight("");
    router.push("/"); // Return to the main screen after logging!
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="p-4 rounded-xl shadow space-y-4 max-w-md"
    >
      <h2 className="text-lg font-semibold">Log Today's Weight</h2>
      <input
        type="number"
        value={weight}
        onChange={(e) => setWeight(e.target.value)}
        placeholder="Enter weight"
        className="border rounded p-2 w-full"
        required
      />
      <button
        type="submit"
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Save
      </button>
    </form>
  );
}