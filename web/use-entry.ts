import { useState } from "react";
import type { SaveEntry } from "./port";
export function useEntry(saveEntry: SaveEntry) {
  const [message, setMessage] = useState("No entry saved");
  const save = async () => {
    try {
      const entry = await saveEntry();
      setMessage(`Saved ${entry.title} #${entry.id}`);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Save failed");
    }
  };
  return { message, save };
}
