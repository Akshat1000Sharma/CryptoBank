import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="bg-foreground text-background p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link href="/" className="text-xl font-bold">
          Crypto Bank
        </Link>
        <div className="flex gap-4">
          <Link href="/balance" className="hover:underline">
            Balance
          </Link>
          <Link href="/total-supply" className="hover:underline">
            Total Supply
          </Link>
          <Link href="/transfer" className="hover:underline">
            Transfer
          </Link>
        </div>
      </div>
    </nav>
  );
}