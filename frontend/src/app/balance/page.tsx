'use client';

import { useState } from "react";
import { AddressInput } from "../../components/AddressInput";
import { Button } from "../../components/Button";
import { getBalance } from "../../lib/api";

// Token addresses - these match your deployed contracts
const TOKENS = [
  {
    name: "MyToken (MTK)",
    address: "0x5FbDB2315678afecb367f032d93F642f64180aa3",
    symbol: "MTK"
  },
  {
    name: "MyToken2 (MTK2)",
    address: "0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0",
    symbol: "MTK2"
  }
];

interface TokenBalance {
  name: string;
  symbol: string;
  address: string;
  balance: number | null;
  error?: string;
}

export default function Balance() {
  const [address, setAddress] = useState("");
  const [balances, setBalances] = useState<TokenBalance[]>(
    TOKENS.map(token => ({ ...token, balance: null }))
  );
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleCheckBalance = async () => {
    if (!address) {
      setError("Please enter a valid address");
      return;
    }
    
    setLoading(true);
    setError(null);
    
    // Reset balances
    setBalances(TOKENS.map(token => ({ ...token, balance: null, error: undefined })));
    
    // Fetch balance for each token
    const balancePromises = TOKENS.map(async (token) => {
      try {
        const response = await getBalance(address, token.address);
        return {
          ...token,
          balance: response.balance,
          error: undefined
        };
      } catch (err: any) {
        return {
          ...token,
          balance: null,
          error: err.message || "Failed to fetch balance"
        };
      }
    });
    
    try {
      const results = await Promise.all(balancePromises);
      setBalances(results);
    } catch (err) {
      setError("Failed to fetch balances. Please check the address and try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-center">Check Token Balances</h1>
      <p className="text-center text-gray-600 dark:text-gray-400 mb-6">
        View balances for all tokens in your wallet
      </p>
      
      <div className="mb-6">
        <AddressInput
          value={address}
          onChange={(e) => setAddress(e.target.value)}
          placeholder="Enter wallet address (0x...)"
        />
        <Button onClick={handleCheckBalance} disabled={loading} className="mt-4 w-full">
          {loading ? "Checking Balances..." : "Check All Balances"}
        </Button>
      </div>

      {error && (
        <div className="mb-4 p-4 bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300 rounded">
          {error}
        </div>
      )}

      <div className="space-y-4">
        {balances.map((tokenBalance, index) => (
          <div
            key={index}
            className="p-4 bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700"
          >
            <div className="flex justify-between items-start mb-2">
              <div>
                <h3 className="font-semibold text-lg">{tokenBalance.name}</h3>
                <p className="text-sm text-gray-500 dark:text-gray-400 font-mono">
                  {tokenBalance.address.slice(0, 6)}...{tokenBalance.address.slice(-4)}
                </p>
              </div>
              {tokenBalance.balance !== null && (
                <div className="text-right">
                  <p className="text-2xl font-bold text-green-600 dark:text-green-400">
                    {tokenBalance.balance.toFixed(4)}
                  </p>
                  <p className="text-sm text-gray-500 dark:text-gray-400">{tokenBalance.symbol}</p>
                </div>
              )}
            </div>
            
            {tokenBalance.error && (
              <div className="mt-2 p-2 bg-yellow-100 dark:bg-yellow-900 text-yellow-700 dark:text-yellow-300 rounded text-sm">
                ⚠️ {tokenBalance.error}
              </div>
            )}
            
            {loading && tokenBalance.balance === null && !tokenBalance.error && (
              <div className="mt-2 text-sm text-gray-500 dark:text-gray-400">
                Loading...
              </div>
            )}
            
            {!loading && tokenBalance.balance === null && !tokenBalance.error && (
              <div className="mt-2 text-sm text-gray-500 dark:text-gray-400">
                Enter an address and click "Check All Balances"
              </div>
            )}
          </div>
        ))}
      </div>

      {balances.some(b => b.balance !== null) && (
        <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900 rounded-lg">
          <p className="text-sm text-blue-800 dark:text-blue-200">
            💡 Tip: You can use these balances to verify your swaps in the Dashboard!
          </p>
        </div>
      )}
    </div>
  );
}