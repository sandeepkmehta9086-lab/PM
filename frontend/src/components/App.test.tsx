import { render, screen } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";
import { App } from "@/components/App";
import { initialData } from "@/lib/kanban";

afterEach(() => {
  vi.unstubAllGlobals();
});

it("loads the authenticated user's board from the backend", async () => {
  const board = {
    ...initialData,
    columns: [
      { ...initialData.columns[0], title: "Saved backlog" },
      ...initialData.columns.slice(1),
    ],
  };
  const fetchMock = vi
    .fn()
    .mockResolvedValueOnce({
      json: async () => ({ authenticated: true }),
    })
    .mockResolvedValueOnce({
      ok: true,
      json: async () => board,
    });
  vi.stubGlobal("fetch", fetchMock);

  render(<App />);

  expect(await screen.findByDisplayValue("Saved backlog")).toBeInTheDocument();
  expect(fetchMock).toHaveBeenNthCalledWith(1, "/api/session");
  expect(fetchMock).toHaveBeenNthCalledWith(2, "/api/board");
});
