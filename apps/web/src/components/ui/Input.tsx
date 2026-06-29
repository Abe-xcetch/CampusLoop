"use client";
import React from "react";

type InputProps = React.InputHTMLAttributes<HTMLInputElement> & {
  label?: string;
  error?: string | null;
};

export default function Input({ label, error, className = "", ...rest }: InputProps) {
  return (
    <label className="block">
      {label ? <div className="text-sm font-medium text-slate-700 mb-1">{label}</div> : null}
      <input className={`w-full rounded-lg border border-slate-200 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-campusloop-primary/30 ${className}`} {...rest} />
      {error ? <p className="mt-1 text-xs text-red-600">{error}</p> : null}
    </label>
  );
}
