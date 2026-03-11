import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "jsdom",
    include: ["dashboard/static/js/__tests__/**/*.test.js"],
    coverage: {
      provider: "v8",
      include: ["dashboard/static/js/**/*.js"],
      exclude: ["dashboard/static/js/__tests__/**"],
      thresholds: {
        lines: 70,
        functions: 70,
        branches: 70,
        statements: 70,
      },
      reporter: ["text", "text-summary"],
    },
  },
});
