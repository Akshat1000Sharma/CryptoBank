import Link from "next/link";
import { Button } from "../components/Button";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-8rem)] gap-8">
      <h1 className="text-4xl font-bold">Welcome to Crypto Bank</h1>
      <p className="text-lg text-center max-w-md">
        Manage your tokens with ease. Check balances, view total supply, or transfer tokens securely.
      </p>
      <div className="flex flex-col sm:flex-row gap-4">
        <Link href="/balance">
          <Button>Check Balance</Button>
        </Link>
        <Link href="/total-supply">
          <Button>View Total Supply</Button>
        </Link>
        <Link href="/transfer">
          <Button>Transfer Tokens</Button>
        </Link>
      </div>
    </div>
  );
}