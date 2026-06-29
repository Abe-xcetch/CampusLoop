import React from "react";
import Logo from "./Logo";

export default function BrandHeader() {
  return (
    <header className="w-full py-4 bg-transparent">
      <div className="max-w-6xl mx-auto px-6 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <Logo />
          <div>
            <div className="font-bold text-lg text-slate-900">CampusLoop</div>
            <div className="text-xs text-slate-500">One Campus. Endless Opportunities.</div>
          </div>
        </div>
        <nav className="hidden md:flex items-center space-x-4 text-sm">
          <a href="#features" className="text-1E293B hover:underline">Features</a>
          <a href="/auth/signup" className="px-3 py-2 rounded-md brand-primary">Get Started</a>
        </nav>
      </div>
    </header>
  );
}
