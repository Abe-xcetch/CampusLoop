"use client";

import React, { useState } from "react";
import { Button } from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import ErrorMessage from "@/components/ui/ErrorMessage";

export default function ForgotPasswordForm() {
  const [email, setEmail] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!email.endsWith("@strathmore.edu")) {
      setError("Please use your @strathmore.edu email address.");
      return;
    }

    setIsLoading(true);

    try {
      // Placeholder for Firebase password reset
      // TODO: Integrate Firebase client SDK
      console.log("Password reset request:", { email });
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setSuccess(true);
    } catch (err) {
      setError("Failed to send reset email. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  if (success) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50 px-4">
        <div className="w-full max-w-md">
          <div className="glass-panel rounded-2xl p-8 shadow-premium text-center">
            <div className="h-16 w-16 rounded-full bg-blue-100 flex items-center justify-center mx-auto mb-4">
              <svg className="h-8 w-8 text-campusloop-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <h1 className="font-display font-bold text-2xl text-slate-900 mb-2">
              Check Your Email
            </h1>
            <p className="text-slate-600 mb-6">
              We've sent a password reset link to <strong>{email}</strong>. The link will expire in 24 hours.
            </p>
            <Button variant="outline" onClick={() => window.location.href = "/auth/login"}>
              Back to Login
            </Button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 px-4">
      <div className="w-full max-w-md">
        <div className="glass-panel rounded-2xl p-8 shadow-premium">
          <div className="text-center mb-8">
            <div className="h-12 w-12 rounded-xl bg-campusloop-primary flex items-center justify-center font-display font-bold text-white text-xl mx-auto mb-4">
              CL
            </div>
            <h1 className="font-display font-bold text-2xl text-slate-900">
              Reset Password
            </h1>
            <p className="mt-2 text-sm text-slate-600">
              Enter your @strathmore.edu email to receive a reset link
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {error && <ErrorMessage>{error}</ErrorMessage>}
            
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-slate-700 mb-1">
                Email
              </label>
              <Input
                id="email"
                type="email"
                placeholder="your.email@strathmore.edu"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={isLoading}
              />
            </div>

            <Button type="submit" className="w-full" isLoading={isLoading}>
              Send Reset Link
            </Button>
          </form>

          <div className="mt-6 text-center">
            <a href="/auth/login" className="text-sm text-strathmore-blue hover:underline font-medium">
              Back to Sign In
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
