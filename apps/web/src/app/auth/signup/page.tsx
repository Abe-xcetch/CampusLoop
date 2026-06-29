"use client";
import React, { useState } from "react";
import Link from "next/link";
import Input from "../../../components/ui/Input";
import { Button } from "../../../components/ui/Button";
import ErrorMessage from "../../../components/ui/ErrorMessage";
import { getFirebaseAuth } from "../../../lib/firebase";
import { createUserWithEmailAndPassword, sendEmailVerification } from "firebase/auth";

export default function SignupPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!email || !password) return setError("Please provide an email and password.");
    if (password !== confirm) return setError("Passwords do not match.");
    if (!email.endsWith('@strathmore.edu')) return setError('Please use your @strathmore.edu email');
    setLoading(true);
    try {
      const auth = getFirebaseAuth();
      const cred = await createUserWithEmailAndPassword(auth, email, password);
      await sendEmailVerification(cred.user);
      window.location.href = '/auth/verify-email';
    } catch (err: any) {
      setError(err?.message || "Registration failed. Try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900">Create your account</h1>
        <p className="mt-2 text-sm text-slate-600">Only Strathmore University emails are allowed for registration.</p>
      </div>
      <form onSubmit={submit} className="space-y-5">
        {error ? <ErrorMessage>{error}</ErrorMessage> : null}

        <Input label="University Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@strathmore.edu" />
        <Input label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Create a password" />
        <Input label="Confirm Password" type="password" value={confirm} onChange={(e) => setConfirm(e.target.value)} placeholder="Repeat password" />

        <div className="flex justify-between items-center gap-4 sm:flex-row sm:items-center">
          <Link href="/auth/login" className="text-sm text-campusloop-primary hover:underline">
            Already have an account?
          </Link>
          <Button type="submit" isLoading={loading} className="w-full sm:w-auto">
            Create account
          </Button>
        </div>
      </form>
    </div>
  );
}
