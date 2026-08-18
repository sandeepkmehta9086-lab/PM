"use client";

import { useEffect, useState } from "react";
import { KanbanBoard } from "@/components/KanbanBoard";
import { LoginForm } from "@/components/LoginForm";
import type { BoardData } from "@/lib/kanban";

export const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const [board, setBoard] = useState<BoardData | null>(null);

  const loadBoard = async () => {
    const response = await fetch("/api/board");
    if (response.ok) {
      setBoard(await response.json());
      setIsAuthenticated(true);
    }
  };

  useEffect(() => {
    fetch("/api/session")
      .then((response) => response.json())
      .then((session) => {
        if (session.authenticated) {
          void loadBoard();
          return;
        }
        setIsAuthenticated(false);
      });
  }, []);

  const logout = async () => {
    await fetch("/api/logout", { method: "POST" });
    setBoard(null);
    setIsAuthenticated(false);
  };

  const saveBoard = (nextBoard: BoardData) => {
    setBoard(nextBoard);
    void fetch("/api/board", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(nextBoard),
    });
  };

  if (isAuthenticated === null) {
    return null;
  }

  if (!isAuthenticated) {
    return <LoginForm onAuthenticated={() => void loadBoard()} />;
  }

  if (!board) {
    return null;
  }

  return <KanbanBoard board={board} onBoardChange={saveBoard} onLogout={logout} />;
};
