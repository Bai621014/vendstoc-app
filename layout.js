export const metadata = {
  title: 'Vends-Toc',
  description: 'Vends ton matos en 1 clic',
}

export default function RootLayout({ children }) {
  return (
    <html lang="fr">
      <body>{children}</body>
    </html>
  )
}
