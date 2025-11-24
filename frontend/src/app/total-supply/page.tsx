'use client';

import { useState, useEffect } from "react";
import { Button } from "../../components/Button";
import { getTotalSupply } from "../../lib/api";

export default function TotalSupply() {
  const [totalSupply, setTotalSupply] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchTotalSupply = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await getTotalSupply();
      setTotalSupply(response.total_supply);
    } catch (err) {
      setError("Failed to fetch total supply. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTotalSupply();
  }, []);

  return (
    <div className="max-w-md mx-auto glass-panel bg-white/5 p-8 rounded-3xl text-white shadow-2xl">
      <h1 className="text-2xl font-bold mb-6 text-center">Total Token Supply</h1>
      <Button onClick={fetchTotalSupply} disabled={loading} className="w-full">
        {loading ? "Fetching..." : "Refresh Total Supply"}
      </Button>
      {totalSupply !== null && (
        <div className="mt-4 p-4 rounded-2xl bg-slate-900/60 border border-white/10">
          <p className="text-lg font-semibold">
            Total Supply: <span className="text-indigo-200">{totalSupply}</span> tokens
          </p>
        </div>
      )}
      {error && (
        <div className="mt-4 p-4 bg-red-500/20 text-red-100 border border-red-500/40 rounded-2xl">
          {error}
        </div>
      )}
    </div>
  );
}