import React from "react";
import Logo from "../../components/brand/Logo";

export const metadata = {
  title: "Auth | CampusLoop",
};

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-[#F8FAFC] py-16">
      <div className="mx-auto w-full max-w-md px-6">
        <div className="mb-10 rounded-[2rem] border border-slate-200/80 bg-white/90 p-8 shadow-[0_20px_80px_rgba(15,23,42,0.08)]">
          <div className="flex items-center gap-4">
            <Logo />
            <div>
              <p className="text-lg font-semibold text-slate-900">CampusLoop</p>
              <p className="text-sm text-slate-500">One Campus. Endless Opportunities.</p>
            </div>
          </div>
          <p className="mt-6 text-sm text-slate-600">Sign in or create your account using your @strathmore.edu email.</p>
        </div>

        <div className="rounded-[2rem] bg-white p-8 shadow-sm border border-slate-100">
          {children}
        </div>
      </div>
    </div>
  );
}
