import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, expect, it, vi } from "vitest";
import { LoginForm } from "@/components/LoginForm";

afterEach(() => {
  vi.unstubAllGlobals();
});

it("submits valid credentials and authenticates", async () => {
  const onAuthenticated = vi.fn();
  const fetchMock = vi.fn().mockResolvedValue({ ok: true });
  vi.stubGlobal("fetch", fetchMock);

  render(<LoginForm onAuthenticated={onAuthenticated} />);
  await userEvent.type(screen.getByLabelText("Username"), "user");
  await userEvent.type(screen.getByLabelText("Password"), "password");
  await userEvent.click(screen.getByRole("button", { name: "Sign in" }));

  expect(fetchMock).toHaveBeenCalledWith("/api/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: "user", password: "password" }),
  });
  expect(onAuthenticated).toHaveBeenCalledOnce();
});

it("shows an error when credentials are rejected", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false }));

  render(<LoginForm onAuthenticated={vi.fn()} />);
  await userEvent.type(screen.getByLabelText("Username"), "wrong");
  await userEvent.type(screen.getByLabelText("Password"), "wrong");
  await userEvent.click(screen.getByRole("button", { name: "Sign in" }));

  expect(screen.getByRole("alert")).toHaveTextContent(
    "Invalid username or password."
  );
});
