import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, it, vi } from "vitest";
import { ChatSidebar } from "@/components/ChatSidebar";

it("renders messages and submits a prompt", async () => {
  const onSend = vi.fn().mockResolvedValue(undefined);
  render(
    <ChatSidebar
      messages={[
        {
          role: "assistant",
          content: "I can help organize your board.",
          boardUpdated: true,
        },
      ]}
      onSend={onSend}
    />
  );

  expect(screen.getByText("I can help organize your board.")).toBeInTheDocument();
  expect(screen.getByText("Board updated")).toBeInTheDocument();

  await userEvent.type(screen.getByLabelText("Message"), "Move the card");
  await userEvent.click(screen.getByRole("button", { name: "Send" }));

  expect(onSend).toHaveBeenCalledWith("Move the card");
});
