/** @type {import('next').NextConfig} */
const nextConfig = {
  // Allow images from Unsplash
  images: {
    domains: ['images.unsplash.com'],
  },
  // Correct way to disable Turbopack
  experimental: {
    // Remove turbo: false which is causing an error
  },
  // Keep only valid Next.js configurations
  reactStrictMode: true,
}

module.exports = nextConfig

