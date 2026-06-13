export const metadata = {
  title: 'Vends-Toc',
  description: 'Parle et encaisse',
}

export default function RootLayout({ children }) {
  return (
    <html lang="fr">
      <body style={{margin: 0}}>{children}</body>
    </html>
  )
}
