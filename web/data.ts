import type { Entry } from "./port";
export async function saveEntry(): Promise<Entry> {
  const response = await fetch("http://127.0.0.1:8765/entries", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title: "verified", key: "qualification-entry" }),
  });
  if (!response.ok) throw new Error("Entry could not be saved.");
  return response.json() as Promise<Entry>;
}
