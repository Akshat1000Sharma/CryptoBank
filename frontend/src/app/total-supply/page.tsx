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
    <div className="max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-6">Total Token Supply</h1>
      <Button onClick={fetchTotalSupply} disabled={loading} className="w-full">
        {loading ? "Fetching..." : "Refresh Total Supply"}
      </Button>
      {totalSupply !== null && (
        <div className="mt-4 p-4 bg-foreground/10 rounded">
          <p>Total Supply: {totalSupply} tokens</p>
        </div>
      )}
      {error && (
        <div className="mt-4 p-4 bg-red-100 text-red-700 rounded">
          {error}
        </div>
      )}
    </div>
  );
}