/** Root layout — fonts, navbar, footer, aurora background. */

import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { AuroraBackground } from "@/components/background/AuroraBackground";
import { APP_NAME, APP_TAGLINE } from "@/lib/constants";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata: Metadata = {
  title: {
    default: `${APP_NAME} — ${APP_TAGLINE}`,
    template: `%s — ${APP_NAME}`,
  },
  description: APP_TAGLINE,
  openGraph: {
    title: `${APP_NAME} — ${APP_TAGLINE}`,
    description: APP_TAGLINE,
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: APP_NAME,
    description: APP_TAGLINE,
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className={inter.variable}>
        <AuroraBackground />
        <Navbar />
        <main className="relative min-h-screen pt-20 pb-20 md:pb-0">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
