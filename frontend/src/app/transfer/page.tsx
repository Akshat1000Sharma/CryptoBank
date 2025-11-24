'use client';

import { useState } from "react";
import { AddressInput } from "../../components/AddressInput";
import { AmountInput } from "../../components/AmountInput";
import { Button } from "../../components/Button";
import { transferTokens } from "../../lib/api";

export default function Transfer() {
  const [toAddress, setToAddress] = useState("");
  const [amount, setAmount] = useState("");
  const [txHash, setTxHash] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleTransfer = async () => {
    if (!toAddress || !amount) {
      setError("Please enter both recipient address and amount");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const response = await transferTokens(toAddress, parseFloat(amount));
      setTxHash(response.tx_hash);
      setToAddress("");
      setAmount("");
    } catch (err) {
      setError("Failed to process transfer. Please check inputs and try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto glass-panel bg-white/5 p-8 rounded-3xl text-white shadow-2xl">
      <h1 className="text-2xl font-bold mb-6 text-center">Transfer Tokens</h1>
      <AddressInput
        value={toAddress}
        onChange={(e) => setToAddress(e.target.value)}
        placeholder="Recipient address (0x...)"
      />
      <AmountInput
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        placeholder="Amount (tokens)"
        className="mt-4"
      />
      <Button onClick={handleTransfer} disabled={loading} className="mt-4 w-full">
        {loading ? "Transferring..." : "Transfer Tokens"}
      </Button>
      {txHash && (
        <div className="mt-4 p-4 bg-emerald-500/20 border border-emerald-400/30 rounded-2xl">
          <p className="text-sm">Transaction successful! Tx Hash: {txHash}</p>
        </div>
      )}
      {error && (
        <div className="mt-4 p-4 bg-red-500/20 border border-red-400/30 rounded-2xl">
          {error}
        </div>
      )}
    </div>
  );
}