import './globals.css';

export const metadata = {
  title: 'B2B Market Intelligence',
  description: 'AI-powered competitive intelligence and market scouting powered by CrewAI',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
