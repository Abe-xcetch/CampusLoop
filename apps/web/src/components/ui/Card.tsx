import React from "react";

type CardProps = React.HTMLAttributes<HTMLDivElement> & {
  title?: string;
  subtitle?: string;
};

export default function Card({ title, subtitle, children, className = "", ...rest }: CardProps) {
  return (
    <div className={`bg-white rounded-2xl p-6 border border-slate-100 shadow-sm ${className}`} {...rest}>
      {title ? <h3 className="font-semibold text-lg text-slate-900">{title}</h3> : null}
      {subtitle ? <p className="text-sm text-slate-500 mt-1">{subtitle}</p> : null}
      <div className="mt-4">{children}</div>
    </div>
  );
}
