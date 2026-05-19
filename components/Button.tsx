import Link from "next/link";
import type { ReactNode } from "react";

type ButtonProps = {
  children: ReactNode;
  href: string;
  variant?: "primary" | "secondary" | "text";
};

const variants = {
  primary: "bg-[var(--accent)] text-white hover:bg-[var(--accent-hover)]",
  secondary: "border border-[var(--border)] text-[var(--text)] hover:bg-[var(--surface)]",
  text: "text-[var(--text)] hover:text-[var(--accent)]"
};

export function Button({ children, href, variant = "primary" }: ButtonProps) {
  return (
    <Link
      className={`inline-flex min-h-11 items-center justify-center rounded-full px-6 text-sm font-semibold transition ${variants[variant]}`}
      href={href}
    >
      {children}
    </Link>
  );
}
