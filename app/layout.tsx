import type { Metadata } from "next";
import "./globals.css";
import { Footer } from "@/components/Footer";
import { Header } from "@/components/Header";

export const metadata: Metadata = {
  title: "Julia Novaes | Psicóloga Clínica",
  description:
    "Psicoterapia para adultos, casais e grupos, com escuta clínica, ética e abordagem fenomenológico-existencial.",
  openGraph: {
    title: "Julia Novaes | Psicóloga Clínica",
    description:
      "Psicoterapia para adultos, casais e grupos, com escuta clínica, ética e abordagem fenomenológico-existencial.",
    type: "website",
    locale: "pt_BR"
  }
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body>
        <Header />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
