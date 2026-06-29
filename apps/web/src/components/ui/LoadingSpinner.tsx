import React from "react";

export default function LoadingSpinner({ size = 6 }: { size?: number }) {
  const s = `${size}rem`;
  return (
    <div className="flex items-center justify-center">
      <svg className="animate-spin text-campusloop-primary" style={{ width: s, height: s }} viewBox="0 0 24 24">
        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
      </svg>
    </div>
  );
}
