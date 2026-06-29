"use client";
import React, { useState } from "react";
import Link from "next/link";
import Input from "../../../components/ui/Input";
import { Button } from "../../../components/ui/Button";
import ErrorMessage from "../../../components/ui/ErrorMessage";
import { getFirebaseAuth } from "../../../lib/firebase";
import { signInWithEmailAndPassword } from "firebase/auth";
import { apiClient } from "../../../services/apiClient";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!email || !password) return setError("Please provide email and password.");
    setLoading(true);
    try {
      const auth = getFirebaseAuth();
      const cred = await signInWithEmailAndPassword(auth, email, password);
      const token = await cred.user.getIdToken();
      await apiClient.post('/auth/login/', { id_token: token }, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      localStorage.setItem('firebase_id_token', token);
      localStorage.setItem('campusloop_authed', '1');
      window.location.href = '/dashboard';
    } catch (err: any) {
      const msg = err?.message || 'Login failed. Please try again.';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900">Welcome back</h1>
        <p className="mt-2 text-sm text-slate-600">Sign in to access the CampusLoop dashboard.</p>
      </div>

      <form onSubmit={submit} className="space-y-5">
        {error ? <ErrorMessage>{error}</ErrorMessage> : null}

        <Input label="University Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@strathmore.edu" />
        <Input label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" />

        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <Link href="/auth/forgot-password" className="text-sm text-campusloop-primary hover:underline">
            Forgot password?
          </Link>
          <Button type="submit" isLoading={loading} className="w-full sm:w-auto">
            Sign in
          </Button>
        </div>
      </form>

      <div className="mt-8 text-center text-sm text-slate-600">
        Don’t have an account?{' '}
        <Link href="/auth/signup" className="font-semibold text-campusloop-primary hover:text-campusloop-secondary">
          Create one
        </Link>
      </div>
    </div>
  );
}
