import { expect, test, type Page } from "@playwright/test";

const signIn = async (page: Page) => {
  await page.goto("/");
  await page.getByLabel("Username").fill("user");
  await page.getByLabel("Password").fill("password");
  await page.getByRole("button", { name: "Sign in" }).click();
  await expect(page.getByRole("heading", { name: "Kanban Studio" })).toBeVisible();
};

test("keeps the board hidden before sign in", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Sign in" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Kanban Studio" })).not.toBeVisible();
});

test("signs in with valid credentials", async ({ page }) => {
  await signIn(page);
  await expect(page.locator('[data-testid^="column-"]')).toHaveCount(5);
});

test("rejects invalid credentials", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel("Username").fill("user");
  await page.getByLabel("Password").fill("wrong");
  await page.getByRole("button", { name: "Sign in" }).click();
  await expect(page.getByText("Invalid username or password.")).toBeVisible();
});

test("logs out and returns to sign in", async ({ page }) => {
  await signIn(page);
  await page.getByRole("button", { name: "Log out" }).click();
  await expect(page.getByRole("heading", { name: "Sign in" })).toBeVisible();
});

test("shows an AI response and refreshes the board after an AI update", async ({
  page,
}) => {
  await signIn(page);
  const updatedBoard = await page.evaluate(async () => {
    const board = await fetch("/api/board").then((response) => response.json());
    board.columns[0].title = "AI planned";
    return board;
  });
  await page.route("**/api/ai/chat", async (route) => {
    await route.fulfill({
      contentType: "application/json",
      body: JSON.stringify({
        response: "I renamed the first column.",
        boardUpdate: updatedBoard,
      }),
    });
  });

  await page.getByLabel("Message").fill("Rename the first column");
  await page.getByRole("button", { name: "Send" }).click();

  await expect(page.getByText("I renamed the first column.")).toBeVisible();
  await expect(page.getByText("Board updated")).toBeVisible();
  await expect(page.getByLabel("Column title").first()).toHaveValue("AI planned");
});

test("adds a card to a column", async ({ page }) => {
  await signIn(page);
  const title = `Playwright card ${Date.now()}`;
  const firstColumn = page.locator('[data-testid^="column-"]').first();
  await firstColumn.getByRole("button", { name: /add a card/i }).click();
  await firstColumn.getByPlaceholder("Card title").fill(title);
  await firstColumn.getByPlaceholder("Details").fill("Added via e2e.");
  const saveRequest = page.waitForResponse(
    (response) =>
      response.url().endsWith("/api/board") &&
      response.request().method() === "PUT"
  );
  await firstColumn.getByRole("button", { name: /add card/i }).click();
  await saveRequest;
  await expect(firstColumn.getByText(title)).toBeVisible();
  await page.reload();
  await expect(page.getByText(title)).toBeVisible();
});

test("moves a card between columns", async ({ page }) => {
  await signIn(page);
  const sourceColumn = page.locator('[data-testid^="column-"]').first();
  const card = sourceColumn.locator('[data-testid^="card-"]').first();
  const cardId = await card.getAttribute("data-testid");
  const targetColumn = page.locator('[data-testid^="column-"]').nth(1);
  const cardBox = await card.boundingBox();
  const columnBox = await targetColumn.boundingBox();
  if (!cardBox || !columnBox) {
    throw new Error("Unable to resolve drag coordinates.");
  }

  await page.mouse.move(
    cardBox.x + cardBox.width / 2,
    cardBox.y + cardBox.height / 2
  );
  await page.mouse.down();
  await page.mouse.move(
    columnBox.x + columnBox.width / 2,
    columnBox.y + 120,
    { steps: 12 }
  );
  await page.mouse.up();
  await expect(targetColumn.getByTestId(cardId!)).toBeVisible();
});
