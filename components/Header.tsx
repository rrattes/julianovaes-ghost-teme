import Link from "next/link";
import { Button } from "@/components/Button";
import { siteContent } from "@/lib/siteContent";

export function Header() {
  return (
    <header className="border-b border-[var(--border)]/70 bg-[var(--background)]">
      <div className="mx-auto flex min-h-20 w-[min(1180px,calc(100%_-_32px))] items-center justify-between gap-8">
        <Link className="grid justify-items-center leading-none" href="/">
          <span className="font-serif-editorial text-2xl uppercase tracking-normal">{siteContent.name}</span>
          <span className="mt-2 text-[11px] font-semibold uppercase tracking-[0.18em] text-[var(--muted)]">
            Psicóloga
          </span>
        </Link>

        <nav className="hidden items-center gap-8 text-[13px] font-medium tracking-[0.02em] text-[var(--text)] lg:flex">
          {siteContent.navigation.map((item) => (
            <Link className="transition hover:text-[var(--accent)]" href={item.href} key={item.href}>
              {item.label}
            </Link>
          ))}
        </nav>

        <div className="hidden lg:block">
          <Button href="/contato">Agendar consulta</Button>
        </div>
      </div>
    </header>
  );
}
