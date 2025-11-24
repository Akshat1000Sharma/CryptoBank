import Link from "next/link";

const links = [
  { href: "/", label: "Home" },
  { href: "/dashboard", label: "Dashboard" },
  { href: "/balance", label: "Balance" },
  { href: "/total-supply", label: "Total Supply" },
  { href: "/transfer", label: "Transfer" },
];

export default function Navbar() {
  return (
    <nav className="sticky top-0 z-50 border-b border-white/10 bg-[#0c0620]/70 text-white backdrop-blur-xl">
      <div className="container mx-auto flex flex-wrap items-center justify-between gap-4 py-4">
        <Link href="/" className="text-2xl font-semibold tracking-tight text-white drop-shadow-lg">
          Crypto Bank
        </Link>
        <div className="flex flex-wrap items-center gap-2">
          {links.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="rounded-full bg-white/10 px-4 py-1.5 text-sm font-medium text-white/80 transition hover:bg-white/20 hover:text-white"
            >
              {item.label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
}