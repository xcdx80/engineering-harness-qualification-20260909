import { defineConfig } from "@playwright/test";
export default defineConfig({
  testDir: "web",
  testMatch: "*.spec.ts",
  workers: 1,
  retries: 0,
  forbidOnly: true,
  use: { baseURL: "http://127.0.0.1:5173", headless: true },
  webServer: [
    {
      command: "python3 -m api.server",
      url: "http://127.0.0.1:8765",
      reuseExistingServer: false,
      env: { QUALIFICATION_DB: process.env.QUALIFICATION_DB! },
    },
    {
      command: "node node_modules/vite/bin/vite.js --host 127.0.0.1",
      url: "http://127.0.0.1:5173",
      reuseExistingServer: false,
    },
  ],
});
