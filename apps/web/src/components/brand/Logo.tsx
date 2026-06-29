import React from "react";
import Link from "next/link";
import { Infinity } from "lucide-react";

export default function Logo({ light = false }: { light?: boolean }) {
  return (
    <Link href="/" className="inline-flex items-center gap-2 transition hover:opacity-90">
      <div className={`flex items-center justify-center rounded-full p-1.5 ${light ? 'bg-white text-campusloop-primary' : 'bg-campusloop-primary text-white'}`}>
        <Infinity size={24} strokeWidth={2.5} />
      </div>
      <span className={`text-2xl font-display font-bold tracking-tight ${light ? 'text-white' : 'text-slate-900'}`}>
        Campus<span className={light ? "text-campusloop-secondary" : "text-campusloop-primary"}>Loop</span>
      </span>
    </Link>
  );
}
