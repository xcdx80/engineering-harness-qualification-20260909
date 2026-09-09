import { createRoot } from "react-dom/client";
import { App } from "./App";
import { saveEntry } from "./data";
createRoot(document.getElementById("root")!).render(
  <App saveEntry={saveEntry} />,
);
