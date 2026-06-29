import React from "react";

export default function EmptyState({ title, description, action }: { title?: string; description?: string; action?: React.ReactNode }) {
  return (
    <div className="text-center py-12">
      <div className="mx-auto w-full max-w-md">
        <div className="h-24 w-24 mx-auto rounded-full bg-campusloop-primary/5 flex items-center justify-center mb-6">
          <svg className="w-10 h-10 text-campusloop-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 7v10a2 2 0 002 2h14" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 7V4a4 4 0 118 0v3" />
          </svg>
        </div>
        <h3 className="text-lg font-semibold text-slate-900">{title || "Nothing here yet"}</h3>
        <p className="mt-2 text-sm text-slate-500">{description || "There are no items to show right now."}</p>
        {action ? <div className="mt-6">{action}</div> : null}
      </div>
    </div>
  );
}
