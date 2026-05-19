import Link from "next/link";
import { Container } from "@/components/Container";
import { siteContent } from "@/lib/siteContent";

export function Footer() {
  return (
    <footer className="border-t border-[var(--border)] bg-[var(--surface-soft)] py-10 text-sm text-[var(--muted)]">
      <Container>
        <div className="grid gap-8 md:grid-cols-4">
          <div>
            <strong className="font-serif-editorial block text-2xl font-normal uppercase text-[var(--text)]">
              {siteContent.name}
            </strong>
            <p className="mt-4 max-w-xs">{siteContent.shortDescription}</p>
          </div>
          <div>
            <h2 className="text-xs font-bold uppercase tracking-[0.12em] text-[var(--text)]">Navegação</h2>
            <div className="mt-4 grid gap-2">
              {siteContent.navigation.map((item) => (
                <Link href={item.href} key={item.href}>
                  {item.label}
                </Link>
              ))}
            </div>
          </div>
          <div>
            <h2 className="text-xs font-bold uppercase tracking-[0.12em] text-[var(--text)]">Atendimento</h2>
            <p className="mt-4">Dados de contato e endereços devem ser confirmados antes da publicação.</p>
          </div>
          <div>
            <h2 className="text-xs font-bold uppercase tracking-[0.12em] text-[var(--text)]">Redes sociais</h2>
            <p className="mt-4">Links a confirmar.</p>
          </div>
        </div>
        <div className="mt-8 border-t border-[var(--border)] pt-4 text-xs">
          © 2026 Julia Novaes. Todos os direitos reservados.
        </div>
      </Container>
    </footer>
  );
}
