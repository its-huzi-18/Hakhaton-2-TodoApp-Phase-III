import type { NextConfig } from "next";
import path from "path";

const nextConfig: NextConfig = {
  webpack: (config, { isServer }) => {
    config.resolve.alias["@"] = path.resolve(__dirname, "./src");
    config.resolve.alias["@/lib"] = path.resolve(__dirname, "./src/lib");
    config.resolve.alias["@/components"] = path.resolve(__dirname, "./src/components");
    config.resolve.alias["@/hooks"] = path.resolve(__dirname, "./hooks");
    config.resolve.alias["@/app"] = path.resolve(__dirname, "./app");
    return config;
  },
};

export default nextConfig;
