"use client";

import { FormEvent, useState } from "react";

type LoginFormProps = {
  onAuthenticated: () => void;
};

export const LoginForm = ({ onAuthenticated }: LoginFormProps) => {
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");
    setIsSubmitting(true);

    const formData = new FormData(event.currentTarget);
    const response = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: formData.get("username"),
        password: formData.get("password"),
      }),
    });

    setIsSubmitting(false);

    if (!response.ok) {
      setError("Invalid username or password.");
      return;
    }

    onAuthenticated();
  };

  return (
    <main className="flex min-h-screen items-center justify-center px-6 py-12">
      <section className="w-full max-w-md rounded-[32px] border border-[var(--stroke)] bg-white p-8 shadow-[var(--shadow)]">
        <p className="text-xs font-semibold uppercase tracking-[0.35em] text-[var(--gray-text)]">
          Kanban Studio
        </p>
        <h1 className="mt-3 font-display text-4xl font-semibold text-[var(--navy-dark)]">
          Sign in
        </h1>
        <p className="mt-3 text-sm leading-6 text-[var(--gray-text)]">
          Sign in to access your project board.
        </p>

        <form className="mt-8 space-y-5" onSubmit={handleSubmit}>
          <label className="block text-sm font-semibold text-[var(--navy-dark)]">
            Username
            <input
              className="mt-2 w-full rounded-xl border border-[var(--stroke)] px-4 py-3 outline-none focus:border-[var(--primary-blue)]"
              name="username"
              required
            />
          </label>
          <label className="block text-sm font-semibold text-[var(--navy-dark)]">
            Password
            <input
              className="mt-2 w-full rounded-xl border border-[var(--stroke)] px-4 py-3 outline-none focus:border-[var(--primary-blue)]"
              name="password"
              type="password"
              required
            />
          </label>
          {error ? (
            <p className="text-sm text-red-700" role="alert">
              {error}
            </p>
          ) : null}
          <button
            className="w-full rounded-xl bg-[var(--secondary-purple)] px-4 py-3 font-semibold text-white transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-60"
            disabled={isSubmitting}
            type="submit"
          >
            {isSubmitting ? "Signing in..." : "Sign in"}
          </button>
        </form>
      </section>
    </main>
  );
};
