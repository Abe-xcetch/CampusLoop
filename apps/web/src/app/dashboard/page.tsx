import React from "react";
import StatCard from "../../components/ui/StatCard";
import ListingCard from "../../components/ui/ListingCard";
import Badge from "../../components/ui/Badge";

export default function DashboardHome() {
  return (
    <div className="space-y-8">
      <section className="grid gap-6 xl:grid-cols-3">
        <StatCard title="Active Listings" value="12" subtitle="Live on campus" />
        <StatCard title="Transactions" value="34" subtitle="Completed this term" />
        <StatCard title="Reputation" value="4.9/5" subtitle="Average seller score" />
      </section>

      <section className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm">
        <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-400">Recent activity</p>
            <h2 className="mt-3 text-2xl font-bold text-slate-900">Your campus marketplace</h2>
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <Badge>Verified</Badge>
            <Badge>Top seller</Badge>
          </div>
        </div>

        <div className="mt-8 grid gap-6 md:grid-cols-2">
          <ListingCard title="MacBook Air M1" price="KES 78,000" status="In stock" badge="Hot" />
          <ListingCard title="Textbook bundle" price="KES 4,500" status="Available" badge="New" />
        </div>
      </section>
    </div>
  );
}
