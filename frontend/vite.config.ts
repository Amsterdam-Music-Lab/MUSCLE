import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tsconfigPaths from "vite-tsconfig-paths";
import { analyzer, type AnalyzerPluginOptions } from "vite-bundle-analyzer";

// Bundle analyzer served on port 8888 when ANALYZE_BUNDLE is set to true:
// docker-compose exec client sh -c "ANALYZE_BUNDLE=true yarn vite build"
const analyze = process.env.ANALYZE_BUNDLE === "true";
const analyzerOpts: AnalyzerPluginOptions = {
    analyzerMode: "server",
    analyzerPort: 8888, // Port forwarded by Docker
    openAnalyzer: false,
};

export default defineConfig({
    plugins: [react(), tsconfigPaths(), ...(analyze ? [analyzer(analyzerOpts)] : [])],
    server: {
        host: "0.0.0.0",
        port: 3000,
        strictPort: true,
    },
    build: {
        outDir: "build",
        sourcemap: true,
    },
    resolve: {
        alias: {
            "@/": "/src/",
        },
    },
});
