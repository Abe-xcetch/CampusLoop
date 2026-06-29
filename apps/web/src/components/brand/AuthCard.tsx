import React from "react";

export default function AuthCard({ children }: { children: React.ReactNode }) {
  return (
    <div className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100">
      {children}
    </div>
  );
}
