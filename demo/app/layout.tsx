import "./globals.css"

export const metadata = { title: "Fanus – Living Seal", description: "Fanus Demo" }

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
