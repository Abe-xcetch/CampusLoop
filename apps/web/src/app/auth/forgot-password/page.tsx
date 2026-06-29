"use client";
import React, { useState } from "react";
import Link from "next/link";
import Input from "../../../components/ui/Input";
import { Button } from "../../../components/ui/Button";
import ErrorMessage from "../../../components/ui/ErrorMessage";
import { getFirebaseAuth } from "../../../lib/firebase";
import { sendPasswordResetEmail } from "firebase/auth";
import { apiClient } from "../../../services/apiClient";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!email) return setError("Please enter your university email.");
    setLoading(true);
    try {
      const auth = getFirebaseAuth();
      await sendPasswordResetEmail(auth, email);
      try {
        await apiClient.post('/auth/password-reset/', { email });
      } catch (e) {
        // ignore backend errors
      }
      setMessage("If that email exists, we've sent password reset instructions.");
    } catch (err: any) {
      setError(err?.message || "Unable to send reset email.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900">Reset your password</h1>
        <p className="mt-2 text-sm text-slate-600">Enter your Strathmore email and we’ll send instructions to reset your password.</p>
      </div>

      <form onSubmit={submit} className="space-y-5">
        {error ? <ErrorMessage>{error}</ErrorMessage> : null}
        {message ? <div className="rounded-2xl border border-emerald-100 bg-emerald-50 px-4 py-3 text-sm text-emerald-700">{message}</div> : null}

        <Input label="University Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@strathmore.edu" />

        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <Link href="/auth/login" className="text-sm text-campusloop-primary hover:underline">
            Back to login
          </Link>
          <Button type="submit" isLoading={loading} className="w-full sm:w-auto">
            Send reset link
          </Button>
        </div>
      </form>
    </div>
  );
}
