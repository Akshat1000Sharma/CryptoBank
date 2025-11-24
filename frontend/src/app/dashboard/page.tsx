"use client";

import { useState, useEffect } from "react";
import { Button } from "../../components/Button";
import { AddressInput } from "../../components/AddressInput";
import { AmountInput } from "../../components/AmountInput";
import {
  swapTokens,
  getSwapQuote,
  batchTransfer,
  verifyTransaction,
  getTransactionStatus,
  addVerifier,
  getVerifiers,
} from "../../lib/api";

export default function Dashboard() {
  // Swap state
  const [swapTokenIn, setSwapTokenIn] = useState("");
  const [swapTokenOut, setSwapTokenOut] = useState("");
  const [swapAmount, setSwapAmount] = useState("");
  const [swapQuote, setSwapQuote] = useState<number | null>(null);
  const [swapResult, setSwapResult] = useState<string>("");

  // Batch transfer state
  const [batchTxs, setBatchTxs] = useState<Array<{ to: string; amount: string }>>([
    { to: "", amount: "" },
  ]);
  const [batchResult, setBatchResult] = useState<any>(null);

  // Verification state
  const [txHash, setTxHash] = useState("");
  const [verifierAddress, setVerifierAddress] = useState("");
  const [verificationResult, setVerificationResult] = useState<any>(null);
  const [txStatus, setTxStatus] = useState<any>(null);

  // Verifiers state
  const [newVerifier, setNewVerifier] = useState("");
  const [verifiers, setVerifiers] = useState<string[]>([]);

  const handleGetQuote = async () => {
    if (!swapTokenIn || !swapTokenOut || !swapAmount) {
      alert("Please fill all swap fields");
      return;
    }
    try {
      const result = await getSwapQuote(swapTokenIn, swapTokenOut, parseFloat(swapAmount));
      setSwapQuote(result.amount_out);
    } catch (error: any) {
      alert(`Error: ${error.message}`);
    }
  };

  const handleSwap = async () => {
    if (!swapTokenIn || !swapTokenOut || !swapAmount) {
      alert("Please fill all swap fields");
      return;
    }
    try {
      const result = await swapTokens(swapTokenIn, swapTokenOut, parseFloat(swapAmount));
      setSwapResult(`Swap successful! TX: ${result.tx_hash}, Amount out: ${result.amount_out}`);
      setSwapQuote(null);
    } catch (error: any) {
      alert(`Error: ${error.message}`);
    }
  };

  const addBatchTx = () => {
    setBatchTxs([...batchTxs, { to: "", amount: "" }]);
  };

  const removeBatchTx = (index: number) => {
    setBatchTxs(batchTxs.filter((_, i) => i !== index));
  };

  const updateBatchTx = (index: number, field: "to" | "amount", value: string) => {
    const updated = [...batchTxs];
    updated[index][field] = value;
    setBatchTxs(updated);
  };

  const handleBatchTransfer = async () => {
    const validTxs = batchTxs.filter((tx) => tx.to && tx.amount);
    if (validTxs.length === 0) {
      alert("Please add at least one valid transaction");
      return;
    }
    try {
      const transactions = validTxs.map((tx) => ({
        to: tx.to,
        amount: parseFloat(tx.amount),
      }));
      const result = await batchTransfer(transactions);
      setBatchResult(result);
    } catch (error: any) {
      alert(`Error: ${error.message}`);
    }
  };

  const handleVerify = async () => {
    if (!txHash || !verifierAddress) {
      alert("Please provide transaction hash and verifier address");
      return;
    }
    try {
      const result = await verifyTransaction(txHash, verifierAddress);
      setVerificationResult(result);
      if (result.consensus_reached) {
        alert("Consensus reached! Transaction verified.");
      }
    } catch (error: any) {
      alert(`Error: ${error.message}`);
    }
  };

  const handleGetStatus = async () => {
    if (!txHash) {
      alert("Please provide transaction hash");
      return;
    }
    try {
      const result = await getTransactionStatus(txHash);
      setTxStatus(result);
    } catch (error: any) {
      alert(`Error: ${error.message}`);
    }
  };

  const handleAddVerifier = async () => {
    if (!newVerifier) {
      alert("Please provide verifier address");
      return;
    }
    try {
      await addVerifier(newVerifier);
      alert("Verifier added successfully");
      setNewVerifier("");
      loadVerifiers();
    } catch (error: any) {
      alert(`Error: ${error.message}`);
    }
  };

  const loadVerifiers = async () => {
    try {
      const result = await getVerifiers();
      setVerifiers(result.verifiers || []);
    } catch (error: any) {
      console.error("Error loading verifiers:", error);
    }
  };

  // Load verifiers on mount
  useEffect(() => {
    loadVerifiers();
  }, []);

  return (
    <div className="max-w-6xl mx-auto space-y-8 text-white">
      <h1 className="text-4xl font-bold text-center drop-shadow-lg">DeFi Dashboard</h1>

      {/* Token Swap Section */}
      <section className="glass-panel bg-white/5 p-6 rounded-3xl space-y-4">
        <h2 className="text-2xl font-semibold mb-2">🔄 Token Swap (DeFi)</h2>
        <p className="text-white/70">
          Convert between different tokens using our liquidity pool
        </p>
        <div className="space-y-4">
          <div>
            <label className="block mb-2">Token In Address</label>
            <AddressInput
              value={swapTokenIn}
              onChange={(e) => setSwapTokenIn(e.target.value)}
              placeholder="0x..."
            />
          </div>
          <div>
            <label className="block mb-2">Token Out Address</label>
            <AddressInput
              value={swapTokenOut}
              onChange={(e) => setSwapTokenOut(e.target.value)}
              placeholder="0x..."
            />
          </div>
          <div>
            <label className="block mb-2">Amount In</label>
            <AmountInput
              value={swapAmount}
              onChange={(e) => setSwapAmount(e.target.value)}
              placeholder="0.0"
            />
          </div>
          <div className="flex flex-wrap gap-4">
            <Button onClick={handleGetQuote} className="flex-1 min-w-[140px]">
              Get Quote
            </Button>
            <Button onClick={handleSwap} className="flex-1 min-w-[140px]">
              Execute Swap
            </Button>
          </div>
          {swapQuote !== null && (
            <div className="p-4 rounded-xl bg-indigo-600/20 border border-white/10">
              <p className="font-semibold text-sm tracking-wide">
                Estimated Amount Out: {swapQuote.toFixed(6)}
              </p>
            </div>
          )}
          {swapResult && (
            <div className="p-4 rounded-xl bg-emerald-500/20 border border-emerald-300/30">
              <p className="text-sm">{swapResult}</p>
            </div>
          )}
        </div>
      </section>

      {/* Batch Transfer Section */}
      <section className="glass-panel bg-white/5 p-6 rounded-3xl space-y-4">
        <h2 className="text-2xl font-semibold mb-2">⚡ Parallel Batch Transfer</h2>
        <p className="text-white/70">
          Execute multiple transactions in parallel using our super node
        </p>
        <div className="space-y-4">
          {batchTxs.map((tx, index) => (
            <div key={index} className="flex flex-col gap-4 md:flex-row md:items-end">
              <div className="flex-1">
                <label className="block mb-2">To Address</label>
                <AddressInput
                  value={tx.to}
                  onChange={(e) => updateBatchTx(index, "to", e.target.value)}
                  placeholder="0x..."
                />
              </div>
              <div className="flex-1">
                <label className="block mb-2">Amount</label>
                <AmountInput
                  value={tx.amount}
                  onChange={(e) => updateBatchTx(index, "amount", e.target.value)}
                  placeholder="0.0"
                />
              </div>
              {batchTxs.length > 1 && (
                <button
                  onClick={() => removeBatchTx(index)}
                  className="px-4 py-2 bg-red-500/70 text-white rounded hover:bg-red-500 transition"
                >
                  Remove
                </button>
              )}
            </div>
          ))}
          <div className="flex flex-wrap gap-4">
            <Button onClick={addBatchTx} className="flex-1 min-w-[160px]">
              Add Transaction
            </Button>
            <Button onClick={handleBatchTransfer} className="flex-1 min-w-[160px]">
              Execute Batch
            </Button>
          </div>
          {batchResult && (
            <div className="p-4 rounded-2xl bg-emerald-500/15 border border-emerald-300/20">
              <p className="font-semibold text-lg mb-2">Batch Transfer Result</p>
              <p className="text-sm text-white/80">Status: {batchResult.status}</p>
              <p className="text-sm text-white/80">Verified: {batchResult.verified ? "Yes" : "No"}</p>
              <p className="text-sm text-white/80">Count: {batchResult.count}</p>
              <div className="mt-3">
                <p className="font-semibold">Transaction Hashes:</p>
                <ul className="list-disc list-inside text-xs text-white/80 space-y-1">
                  {batchResult.tx_hashes.map((hash: string, i: number) => (
                    <li key={i} className="break-all">{hash}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
      </section>

      {/* Consensus & Verification Section */}
      <section className="glass-panel bg-white/5 p-6 rounded-3xl space-y-4">
        <h2 className="text-2xl font-semibold mb-2">🔐 Consensus & Verification</h2>
        <p className="text-white/70">
          Verify transactions using our consensus mechanism
        </p>
        <div className="space-y-4">
          <div>
            <label className="block mb-2">Transaction Hash</label>
            <input
              type="text"
              value={txHash}
              onChange={(e) => setTxHash(e.target.value)}
              placeholder="0x..."
              className="w-full p-2 border rounded dark:bg-gray-700"
            />
          </div>
          <div>
            <label className="block mb-2">Verifier Address</label>
            <AddressInput
              value={verifierAddress}
              onChange={(e) => setVerifierAddress(e.target.value)}
              placeholder="0x..."
            />
          </div>
          <div className="flex flex-wrap gap-4">
            <Button onClick={handleVerify} className="flex-1 min-w-[160px]">
              Verify Transaction
            </Button>
            <Button onClick={handleGetStatus} className="flex-1 min-w-[160px]">
              Get Status
            </Button>
          </div>
          {verificationResult && (
            <div className="p-4 rounded-2xl bg-blue-500/20 border border-blue-200/20">
              <p className="font-semibold">Verification Result:</p>
              <p>Consensus Reached: {verificationResult.consensus_reached ? "Yes" : "No"}</p>
              <p>Verification Count: {verificationResult.verification_count}/{verificationResult.threshold}</p>
              <p>Verifiers: {verificationResult.verifiers.join(", ")}</p>
            </div>
          )}
          {txStatus && (
            <div className="p-4 rounded-2xl bg-blue-500/20 border border-blue-200/20">
              <p className="font-semibold">Transaction Status:</p>
              <p>Consensus Reached: {txStatus.consensus_reached ? "Yes" : "No"}</p>
              <p>Executed: {txStatus.executed ? "Yes" : "No"}</p>
              <p>Verifiers: {txStatus.verifiers.join(", ") || "None"}</p>
            </div>
          )}
        </div>
      </section>

      {/* Verifier Management Section */}
      <section className="glass-panel bg-white/5 p-6 rounded-3xl space-y-4">
        <h2 className="text-2xl font-semibold mb-2">👥 Verifier Management</h2>
        <div className="space-y-4">
          <div className="flex flex-col gap-4 lg:flex-row">
            <AddressInput
              value={newVerifier}
              onChange={(e) => setNewVerifier(e.target.value)}
              placeholder="Add new verifier address"
            />
            <Button onClick={handleAddVerifier}>Add Verifier</Button>
            <Button onClick={loadVerifiers}>Refresh</Button>
          </div>
          <div>
            <p className="font-semibold mb-2">Registered Verifiers:</p>
            {verifiers.length === 0 ? (
              <p className="text-white/60">No verifiers registered</p>
            ) : (
              <ul className="list-disc list-inside text-white/80 space-y-1">
                {verifiers.map((addr, i) => (
                  <li key={i} className="break-all text-sm">{addr}</li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </section>
    </div>
  );
}

