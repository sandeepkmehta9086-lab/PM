"use client";

import { useEffect, useState } from "react";
import { KanbanBoard } from "@/components/KanbanBoard";
import { LoginForm } from "@/components/LoginForm";

export const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

  useEffect(() => {
    fetch("/api/session")
      .then((response) => response.json())
      .then((session) => setIsAuthenticated(session.authenticated));
  }, []);

  const logout = async () => {
    await fetch("/api/logout", { method: "POST" });
    setIsAuthenticated(false);
  };

  if (isAuthenticated === null) {
    return null;
  }

  if (!isAuthenticated) {
    return <LoginForm onAuthenticated={() => setIsAuthenticated(true)} />;
  }

  return <KanbanBoard onLogout={logout} />;
};
