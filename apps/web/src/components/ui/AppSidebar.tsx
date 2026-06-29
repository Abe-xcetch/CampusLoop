import Link from "next/link";
import Badge from "./Badge";

export default function AppSidebar() {
  return (
    <aside className="space-y-6 rounded-3xl border border-slate-100 bg-white p-6 shadow-sm">
      <div className="space-y-1">
        <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Workspace</p>
        <nav className="space-y-1">
          <Link href="/dashboard" className="block rounded-2xl px-4 py-3 text-sm font-medium text-slate-700 hover:bg-slate-50">Dashboard</Link>
          <Link href="/listings" className="block rounded-2xl px-4 py-3 text-sm font-medium text-slate-700 hover:bg-slate-50">Marketplace</Link>
          <Link href="/transactions" className="block rounded-2xl px-4 py-3 text-sm font-medium text-slate-700 hover:bg-slate-50">Transactions</Link>
          <Link href="/reports" className="block rounded-2xl px-4 py-3 text-sm font-medium text-slate-700 hover:bg-slate-50">Support</Link>
        </nav>
      </div>

      <div className="rounded-3xl bg-campusloop-primary/5 p-4">
        <div className="flex items-center justify-between gap-4">
          <div>
            <p className="text-sm font-semibold text-slate-900">Verified Student</p>
            <p className="text-xs text-slate-500">Strathmore University</p>
          </div>
          <Badge>Pro</Badge>
        </div>
      </div>
    </aside>
  );
}
