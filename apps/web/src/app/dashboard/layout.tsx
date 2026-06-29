"use client";
import React from "react";
import AppSidebar from "../../components/ui/AppSidebar";
import AppTopbar from "../../components/ui/AppTopbar";
import { useAuth } from "../../lib/auth";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const { signOut } = useAuth();

  return (
    <div className="min-h-screen bg-[#F8FAFC] py-10">
      <div className="mx-auto grid max-w-7xl gap-8 px-6 xl:grid-cols-[280px_1fr]">
        <AppSidebar />
        <div className="space-y-6">
          <AppTopbar onLogout={signOut} />
          {children}
        </div>
      </div>
    </div>
  );
}
