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
    <div className="max-w-2xl mx-auto glass-panel bg-white/5 p-8 text-white rounded-3xl shadow-2xl">
      <h1 className="text-3xl font-bold mb-3 text-center drop-shadow-lg">Check Token Balances</h1>
      <p className="text-center text-white/70 mb-6">
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
        <div className="mb-4 p-4 bg-red-500/20 text-red-100 rounded-xl border border-red-500/40">
          {error}
        </div>
      )}

      <div className="space-y-4">
        {balances.map((tokenBalance, index) => (
          <div
            key={index}
            className="p-4 rounded-2xl bg-white/5 border border-white/10 shadow-lg"
          >
            <div className="flex justify-between items-start mb-2">
              <div>
                <h3 className="font-semibold text-lg">{tokenBalance.name}</h3>
                <p className="text-sm text-white/60 font-mono">
                  {tokenBalance.address.slice(0, 6)}...{tokenBalance.address.slice(-4)}
                </p>
              </div>
              {tokenBalance.balance !== null && (
                <div className="text-right">
                  <p className="text-2xl font-bold text-emerald-300 drop-shadow">
                    {tokenBalance.balance.toFixed(4)}
                  </p>
                  <p className="text-sm text-white/70">{tokenBalance.symbol}</p>
                </div>
              )}
            </div>
            
            {tokenBalance.error && (
              <div className="mt-2 p-2 bg-yellow-400/15 text-yellow-100 border border-yellow-300/30 rounded text-sm">
                ⚠️ {tokenBalance.error}
              </div>
            )}
            
            {loading && tokenBalance.balance === null && !tokenBalance.error && (
              <div className="mt-2 text-sm text-white/60">
                Loading...
              </div>
            )}
            
            {!loading && tokenBalance.balance === null && !tokenBalance.error && (
              <div className="mt-2 text-sm text-white/60">
                Enter an address and click "Check All Balances"
              </div>
            )}
          </div>
        ))}
      </div>

      {balances.some(b => b.balance !== null) && (
        <div className="mt-6 p-4 bg-blue-500/20 border border-blue-300/30 rounded-xl">
          <p className="text-sm text-blue-50">
            💡 Tip: You can use these balances to verify your swaps in the Dashboard!
          </p>
        </div>
      )}
    </div>
  );
}