import { test, expect } from "@playwright/test";
import { execFileSync } from "node:child_process";
test("browser action stores exactly one real database entry", async ({
  page,
}) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Save entry" }).click();
  await expect(page.getByRole("status")).toHaveText("Saved verified #1");
  await page.getByRole("button", { name: "Save entry" }).click();
  await expect(page.getByRole("status")).toHaveText("Saved verified #1");
  const stored = execFileSync(
    "python3",
    [
      "-c",
      'import sqlite3,sys; c=sqlite3.connect(sys.argv[1]); print(c.execute("SELECT COUNT(*) FROM entries").fetchone()[0])',
      process.env.QUALIFICATION_DB!,
    ],
    { encoding: "utf8" },
  );
  expect(stored.trim()).toBe("1");
});
