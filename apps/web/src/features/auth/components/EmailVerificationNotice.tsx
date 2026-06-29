"use client";

import React from "react";
import { Button } from "@/components/ui/Button";

export default function EmailVerificationNotice() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 px-4">
      <div className="w-full max-w-md">
        <div className="glass-panel rounded-2xl p-8 shadow-premium text-center">
          <div className="h-16 w-16 rounded-full bg-yellow-100 flex items-center justify-center mx-auto mb-4">
            <svg className="h-8 w-8 text-campusloop-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <h1 className="font-display font-bold text-2xl text-slate-900 mb-2">
            Email Verification Required
          </h1>
          <p className="text-slate-600 mb-6">
            Please verify your @strathmore.edu email address to access CampusLoop. Check your inbox for the verification link.
          </p>
          
          <div className="space-y-3">
            <Button className="w-full" onClick={() => window.location.reload()}>
              I've Verified My Email
            </Button>
            <Button variant="outline" className="w-full" onClick={() => window.location.href = "/auth/login"}>
              Back to Login
            </Button>
          </div>

          <p className="mt-6 text-xs text-slate-500">
            Didn't receive the email? Check your spam folder or request a new verification link.
          </p>
        </div>
      </div>
    </div>
  );
}
