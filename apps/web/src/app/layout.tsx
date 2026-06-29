import type { Metadata } from "next";
import { Inter, Plus_Jakarta_Sans } from "next/font/google";
import "./globals.css";
import PublicNavbar from "../components/brand/PublicNavbar";
import Logo from "../components/brand/Logo";
import Link from "next/link";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const plusJakarta = Plus_Jakarta_Sans({ subsets: ["latin"], variable: "--font-plus-jakarta" });

export const metadata: Metadata = {
  title: "CampusLoop | One Campus. Endless Opportunities.",
  description: "CampusLoop - secure, verified student marketplace for your campus.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable} ${plusJakarta.variable}`}>
      <body className="antialiased min-h-screen bg-[#F8FAFC] text-slate-900 font-sans">
        <PublicNavbar />
        <main className="flex-grow">{children}</main>
        <footer className="bg-slate-900 text-white py-16">
          <div className="mx-auto max-w-6xl px-6">
            <div className="grid gap-12 md:grid-cols-4">
              <div className="md:col-span-1">
                <Logo light />
                <p className="mt-4 text-sm text-slate-400">One Campus. Endless Opportunities.</p>
              </div>
              <div>
                <h3 className="font-display font-semibold mb-4 text-white">Marketplace</h3>
                <ul className="space-y-2 text-sm text-slate-400">
                  <li><Link href="/browse" className="hover:text-campusloop-secondary transition">Browse All</Link></li>
                  <li><Link href="/categories" className="hover:text-campusloop-secondary transition">Categories</Link></li>
                  <li><Link href="/sell" className="hover:text-campusloop-secondary transition">Sell an Item</Link></li>
                </ul>
              </div>
              <div>
                <h3 className="font-display font-semibold mb-4 text-white">Company</h3>
                <ul className="space-y-2 text-sm text-slate-400">
                  <li><Link href="/about" className="hover:text-campusloop-secondary transition">About Us</Link></li>
                  <li><Link href="/how-it-works" className="hover:text-campusloop-secondary transition">How It Works</Link></li>
                  <li><Link href="/trust" className="hover:text-campusloop-secondary transition">Trust & Safety</Link></li>
                </ul>
              </div>
              <div>
                <h3 className="font-display font-semibold mb-4 text-white">Support</h3>
                <ul className="space-y-2 text-sm text-slate-400">
                  <li><Link href="/help" className="hover:text-campusloop-secondary transition">Help Center</Link></li>
                  <li><Link href="/contact" className="hover:text-campusloop-secondary transition">Contact Us</Link></li>
                </ul>
              </div>
            </div>
            <div className="mt-12 pt-8 border-t border-slate-800 text-center text-sm text-slate-500">
              © 2026 CampusLoop Strathmore. Created as a Final Year Project. All rights reserved.
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
