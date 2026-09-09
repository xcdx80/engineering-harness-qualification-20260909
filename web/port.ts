export interface Entry {
  id: number;
  title: string;
}
export type SaveEntry = () => Promise<Entry>;
