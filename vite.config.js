import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  root: "front_end",
  build: {
    outDir: "build",
    manifest: true,
    rollupOptions: {
      input: "front_end/src/index.jsx",
    },
  },
});
