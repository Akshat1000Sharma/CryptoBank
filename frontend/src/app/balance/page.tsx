'use client';

import { useState } from "react";
import { AddressInput } from "../../components/AddressInput";
import { Button } from "../../components/Button";
import { getBalance } from "../../lib/api";

export default function Balance() {
  const [address, setAddress] = useState("");
  const [balance, setBalance] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleCheckBalance = async () => {
    if (!address) {
      setError("Please enter a valid address");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const response = await getBalance(address);
      setBalance(response.balance);
    } catch (err) {
      setError("Failed to fetch balance. Please check the address and try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-6">Check Token Balance</h1>
      <AddressInput
        value={address}
        onChange={(e) => setAddress(e.target.value)}
        placeholder="Enter wallet address (0x...)"
      />
      <Button onClick={handleCheckBalance} disabled={loading} className="mt-4 w-full">
        {loading ? "Checking..." : "Check Balance"}
      </Button>
      {balance !== null && (
        <div className="mt-4 p-4 bg-foreground/10 rounded">
          <p>Balance: {balance} tokens</p>
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