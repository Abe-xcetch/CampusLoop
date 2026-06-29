import React from "react";
import Link from "next/link";

export default function VerifyEmailPage() {
  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900">Verify your email</h1>
        <p className="mt-2 text-sm text-slate-600">A verification link has been sent to your Strathmore email. Please check your inbox and follow the link to complete registration.</p>
      </div>
      <div className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm text-center">
        <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-3xl bg-campusloop-secondary/10 text-campusloop-secondary">
          <span className="text-2xl">✓</span>
        </div>
        <p className="text-sm leading-7 text-slate-600">If you don’t see the email within a few minutes, check your spam folder or request another verification email from the login page.</p>
        <div className="mt-8">
          <Link href="/auth/login" className="inline-flex rounded-full bg-campusloop-primary px-6 py-3 text-sm font-semibold text-white shadow-sm hover:bg-campusloop-secondary">
            Return to login
          </Link>
        </div>
      </div>
    </div>
  );
}
