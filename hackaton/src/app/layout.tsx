import '../../styles/globals.css';
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr">
      <body className={inter.className}>
        {/* Div pour l'image de fond avec overlay */}
        <div className="background-image-container">
          <div className="background-overlay"></div>
        </div>
        {children}
      </body>
    </html>
  );
}

export const metadata = {
  title: 'Travel Swiper',
  description: 'Découvrez des destinations et créez votre itinéraire de voyage',
};
