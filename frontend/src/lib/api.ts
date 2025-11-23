const api_url = 'http://localhost:8000';

export async function getBalance(address: string, tokenAddress?: string) {
  const url = tokenAddress 
    ? `${api_url}/api/balance/${address}?token_address=${tokenAddress}`
    : `${api_url}/api/balance/${address}`;
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error("Failed to fetch balance");
  }
  return response.json();
}

export async function getTotalSupply() {
  const response = await fetch(`${api_url}/api/total-supply`);
  if (!response.ok) {
    throw new Error("Failed to fetch total supply");
  }
  return response.json();
}

export async function transferTokens(to: string, amount: number) {
  const response = await fetch(`${api_url}/api/transfer`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ to, amount }),
  });
  if (!response.ok) {
    throw new Error("Failed to process transfer");
  }
  return response.json();
}

export async function swapTokens(tokenIn: string, tokenOut: string, amountIn: number) {
  const response = await fetch(`${api_url}/api/swap`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ token_in: tokenIn, token_out: tokenOut, amount_in: amountIn }),
  });
  if (!response.ok) {
    throw new Error("Failed to process swap");
  }
  return response.json();
}

export async function getSwapQuote(tokenIn: string, tokenOut: string, amountIn: number) {
  const response = await fetch(
    `${api_url}/api/swap/quote?token_in=${tokenIn}&token_out=${tokenOut}&amount_in=${amountIn}`
  );
  if (!response.ok) {
    throw new Error("Failed to get swap quote");
  }
  return response.json();
}

export async function batchTransfer(transactions: Array<{ to: string; amount: number }>) {
  const response = await fetch(`${api_url}/api/batch-transfer`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ transactions }),
  });
  if (!response.ok) {
    throw new Error("Failed to process batch transfer");
  }
  return response.json();
}

export async function verifyTransaction(txHash: string, verifierAddress: string) {
  const response = await fetch(`${api_url}/api/verify/${txHash}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ verifier_address: verifierAddress }),
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Failed to verify transaction" }));
    throw new Error(error.detail || "Failed to verify transaction");
  }
  return response.json();
}

export async function getTransactionStatus(txHash: string) {
  const response = await fetch(`${api_url}/api/verify/${txHash}`);
  if (!response.ok) {
    throw new Error("Failed to get transaction status");
  }
  return response.json();
}

export async function addVerifier(address: string) {
  const response = await fetch(`${api_url}/api/consensus/add-verifier?address=${address}`, {
    method: "POST",
  });
  if (!response.ok) {
    throw new Error("Failed to add verifier");
  }
  return response.json();
}

export async function getVerifiers() {
  const response = await fetch(`${api_url}/api/consensus/verifiers`);
  if (!response.ok) {
    throw new Error("Failed to get verifiers");
  }
  return response.json();
}