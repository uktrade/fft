import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import svgr from "vite-plugin-svgr";

export default defineConfig({
  plugins: [react(), svgr()],
  root: "front_end",
  build: {
    outDir: "build",
    manifest: true,
    rollupOptions: {
      input: ["front_end/src/index.jsx", "front_end/styles/styles.scss"],
    },
  },
  server: {
    proxy: {
      "/static/": "http://localhost:8000",
    },
  },
});
