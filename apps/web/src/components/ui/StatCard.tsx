import React from "react";

export default function StatCard({ title, value, subtitle, className = "" }: { title: string; value: string; subtitle: string; className?: string; }) {
  return (
    <div className={`rounded-3xl border border-slate-100 bg-white p-6 shadow-sm ${className}`}>
      <p className="text-sm font-medium text-slate-500">{title}</p>
      <p className="mt-4 text-3xl font-bold text-slate-900">{value}</p>
      <p className="mt-2 text-sm text-slate-500">{subtitle}</p>
    </div>
  );
}
