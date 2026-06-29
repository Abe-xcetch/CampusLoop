"use client";

import React, { useState } from "react";
import { Button } from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import ErrorMessage from "@/components/ui/ErrorMessage";

export default function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      // Placeholder for Firebase authentication
      // TODO: Integrate Firebase client SDK
      console.log("Login attempt:", { email });
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Redirect to dashboard on success
      // router.push("/dashboard");
    } catch (err) {
      setError("Invalid email or password. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 px-4">
      <div className="w-full max-w-md">
        <div className="glass-panel rounded-2xl p-8 shadow-premium">
          <div className="text-center mb-8">
            <div className="h-12 w-12 rounded-xl bg-campusloop-primary flex items-center justify-center font-display font-bold text-white text-xl mx-auto mb-4">
              CL
            </div>
            <h1 className="font-display font-bold text-2xl text-slate-900">
              Welcome Back
            </h1>
            <p className="mt-2 text-sm text-slate-600">
              Sign in to your CampusLoop account
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

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-slate-700 mb-1">
                Password
              </label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                disabled={isLoading}
              />
            </div>

            <div className="flex items-center justify-between">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  className="h-4 w-4 text-campusloop-primary focus:ring-campusloop-primary border-gray-300 rounded"
                />
                <span className="ml-2 text-sm text-slate-600">Remember me</span>
              </label>
              <a href="/auth/forgot-password" className="text-sm text-campusloop-primary hover:underline">
                Forgot password?
              </a>
            </div>

            <Button type="submit" className="w-full" isLoading={isLoading}>
              Sign In
            </Button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-sm text-slate-600">
              Don't have an account?{" "}
              <a href="/auth/register" className="text-campusloop-primary hover:underline font-medium">
                Sign up
              </a>
            </p>
          </div>
        </div>

        <p className="mt-6 text-center text-xs text-slate-500">
          By signing in, you agree to our Terms of Service and Privacy Policy
        </p>
      </div>
    </div>
  );
}
