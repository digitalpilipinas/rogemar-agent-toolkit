import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

export function ensureDependenciesInstalled(): void {
  const root = import.meta.dir;
  const path = join(root, "node_modules/commander/package.json");
  const required = JSON.parse(readFileSync(join(root, "package.json"), "utf8")).dependencies.commander;
  if (!existsSync(path) || JSON.parse(readFileSync(path, "utf8")).version !== required) {
    throw new Error("Forge dependencies are unavailable. With installation authority, run bun install --frozen-lockfile in the skill scripts directory. This diagnostic did not install anything.");
  }
}
