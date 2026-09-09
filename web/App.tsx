import { useEntry } from "./use-entry";
import type { SaveEntry } from "./port";
export function App({ saveEntry }: { saveEntry: SaveEntry }) {
  const { message, save } = useEntry(saveEntry);
  return (
    <main>
      <h1>Qualification</h1>
      <button onClick={save}>Save entry</button>
      <p role="status">{message}</p>
    </main>
  );
}
