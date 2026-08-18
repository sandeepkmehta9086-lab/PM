"use client";

import { FormEvent, useState } from "react";

export type ChatMessage = {
  role: "user" | "assistant";
  content: string;
  boardUpdated?: boolean;
};

type ChatSidebarProps = {
  messages: ChatMessage[];
  onSend: (message: string) => Promise<void>;
};

export const ChatSidebar = ({ messages, onSend }: ChatSidebarProps) => {
  const [message, setMessage] = useState("");
  const [isSending, setIsSending] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const trimmedMessage = message.trim();
    if (!trimmedMessage) {
      return;
    }

    setIsSending(true);
    await onSend(trimmedMessage);
    setMessage("");
    setIsSending(false);
  };

  return (
    <aside className="flex min-h-[420px] flex-col rounded-[28px] border border-[var(--stroke)] bg-white p-5 shadow-[var(--shadow)]">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.25em] text-[var(--gray-text)]">
          AI assistant
        </p>
        <h2 className="mt-2 font-display text-2xl font-semibold text-[var(--navy-dark)]">
          Plan with your board
        </h2>
      </div>

      <div className="mt-6 flex flex-1 flex-col gap-3 overflow-y-auto">
        {messages.length ? (
          messages.map((chatMessage, index) => (
            <div
              className={
                chatMessage.role === "user"
                  ? "self-end rounded-2xl bg-[var(--secondary-purple)] px-4 py-3 text-sm text-white"
                  : "self-start rounded-2xl bg-[var(--surface)] px-4 py-3 text-sm text-[var(--navy-dark)]"
              }
              key={`${chatMessage.role}-${index}`}
            >
              <p>{chatMessage.content}</p>
              {chatMessage.boardUpdated ? (
                <p className="mt-2 text-xs font-semibold text-[var(--primary-blue)]">
                  Board updated
                </p>
              ) : null}
            </div>
          ))
        ) : (
          <p className="text-sm leading-6 text-[var(--gray-text)]">
            Ask for a summary, or ask me to create, edit, or move cards.
          </p>
        )}
      </div>

      <form className="mt-6 space-y-3 border-t border-[var(--stroke)] pt-5" onSubmit={handleSubmit}>
        <label className="sr-only" htmlFor="chat-message">
          Message
        </label>
        <textarea
          className="min-h-24 w-full resize-none rounded-xl border border-[var(--stroke)] p-3 text-sm outline-none focus:border-[var(--primary-blue)]"
          id="chat-message"
          onChange={(event) => setMessage(event.target.value)}
          placeholder="Ask about your project..."
          value={message}
        />
        <button
          className="w-full rounded-xl bg-[var(--secondary-purple)] px-4 py-3 font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
          disabled={isSending}
          type="submit"
        >
          {isSending ? "Thinking..." : "Send"}
        </button>
      </form>
    </aside>
  );
};
