import "./globals.css"
import { Inter } from "next/font/google"
import type React from "react"
import type { Metadata } from "next"
import MouseMoveEffect from "@/components/mouse-move-effect"
import ParticleBackground from "@/components/particle-background"
import Navbar from "@/components/navbar"
// import { NextAuthProvider } from "./provid /ers"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "WebBuidlers",
  description: "Transform your ideas into stunning websites with our AI-powered website generator.",
  // generator: 'v0.dev'
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} bg-background text-foreground antialiased`}>
        {/* <NextAuthProvider> */}
          <ParticleBackground />
          <MouseMoveEffect />
          <Navbar />
          {children}
        {/* </NextAuthProvider> */}
      </body>
    </html>
  )
}