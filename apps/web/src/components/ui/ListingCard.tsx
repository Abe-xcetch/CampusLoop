import React from "react";
import Badge from "./Badge";

export default function ListingCard({ title, price, status, badge }: { title: string; price: string; status?: string; badge?: string; }) {
  return (
    <div className="rounded-3xl border border-slate-100 bg-white p-5 shadow-sm hover:-translate-y-1 transition-transform">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h3 className="text-lg font-semibold text-slate-900">{title}</h3>
          <p className="mt-1 text-sm text-slate-500">{status || "Available"}</p>
        </div>
        {badge ? <Badge>{badge}</Badge> : null}
      </div>
      <div className="mt-6 flex items-center justify-between">
        <p className="text-2xl font-bold text-slate-900">{price}</p>
        <button className="rounded-full bg-campusloop-primary px-4 py-2 text-sm font-semibold text-white transition hover:bg-campusloop-secondary">View</button>
      </div>
    </div>
  );
}
