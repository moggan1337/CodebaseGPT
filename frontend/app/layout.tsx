import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'CodebaseGPT - Chat with your codebase',
  description: 'AI-powered code understanding - ask questions about any codebase with cited answers',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  )
}
