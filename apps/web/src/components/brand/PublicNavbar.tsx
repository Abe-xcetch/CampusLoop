import Link from "next/link";
import Logo from "./Logo";

export default function PublicNavbar() {
  return (
    <div className="bg-white/80 backdrop-blur-xl sticky top-0 z-50 border-b border-slate-200/70 shadow-sm">
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        <Logo />

        <div className="hidden md:flex items-center gap-6 text-sm font-medium text-slate-600">
          <Link href="/" className="hover:text-campusloop-primary transition">Home</Link>
          <Link href="/browse" className="hover:text-campusloop-primary transition">Browse</Link>
          <Link href="/categories" className="hover:text-campusloop-primary transition">Categories</Link>
          <Link href="/how-it-works" className="hover:text-campusloop-primary transition">How It Works</Link>
          <Link href="/about" className="hover:text-campusloop-primary transition">About Us</Link>
        </div>

        <div className="flex items-center gap-3">
          <Link href="/auth/login" className="inline-flex items-center rounded-full border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-700 shadow-sm transition hover:bg-slate-50">
            Log in
          </Link>
          <Link href="/auth/signup" className="inline-flex items-center rounded-full bg-campusloop-primary px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-campusloop-secondary">
            Sign up
          </Link>
        </div>
      </div>
    </div>
  );
}
