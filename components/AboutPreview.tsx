import Image from "next/image";
import Link from "next/link";

export function AboutPreview() {
  return (
    <section className="grid bg-[var(--surface-soft)] lg:grid-cols-[0.56fr_1fr]">
      <div className="relative min-h-80">
        <Image alt="Ambiente acolhedor de consultório" className="object-cover" fill src="/images/consultorio.png" />
      </div>
      <div className="grid gap-10 px-8 py-14 lg:grid-cols-[1fr_280px] lg:px-16">
        <div>
          <p className="mb-3 text-xs font-bold uppercase tracking-[0.16em] text-[var(--accent)]">Sobre mim</p>
          <h2 className="font-serif-editorial max-w-xl text-4xl leading-tight">
            Psicóloga clínica com abordagem fenomenológico-existencial
          </h2>
          <p className="mt-6 max-w-xl leading-7 text-[var(--muted)]">
            Acredito na importância de uma escuta verdadeira e na construção de um espaço seguro para que cada
            pessoa possa se compreender em sua singularidade.
          </p>
          <Link className="mt-7 inline-flex text-xs font-bold uppercase tracking-[0.1em]" href="/sobre">
            Conhecer minha trajetória →
          </Link>
        </div>
        <div className="grid content-center gap-4 text-sm text-[var(--muted)]">
          <p className="border-b border-[var(--border)] pb-4">Atendimento para adultos, casais e grupos</p>
          <p className="border-b border-[var(--border)] pb-4">Abordagem fenomenológico-existencial</p>
          <p>Atendimento presencial e online a confirmar</p>
        </div>
      </div>
    </section>
  );
}
