const api_url = 'http://localhost:8000';

export async function getBalance(address: string) {
  const response = await fetch(`${api_url}/api/balance/${address}`);
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