import { Button } from "./Button";

export default function AppTopbar({ onLogout }: { onLogout: () => void }) {
  return (
    <div className="flex flex-col gap-4 rounded-3xl border border-slate-100 bg-white p-6 shadow-sm md:flex-row md:items-center md:justify-between">
      <div>
        <p className="text-sm uppercase tracking-[0.24em] text-slate-400">CampusLoop dashboard</p>
        <h2 className="mt-2 text-2xl font-semibold text-slate-900">Welcome back</h2>
      </div>
      <div className="flex items-center gap-3">
        <Button variant="outline" size="sm" onClick={onLogout}>Log out</Button>
      </div>
    </div>
  );
}
