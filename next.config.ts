import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  exports : {
    reactStrictMode: true,
    images: {
      domains: ['localhost'],
    },
  }
};

export default nextConfig;
