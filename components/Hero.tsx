import Image from "next/image";
import { Button } from "@/components/Button";
import { Container } from "@/components/Container";
import { siteContent } from "@/lib/siteContent";

export function Hero() {
  return (
    <section className="py-10 md:py-14">
      <Container className="grid items-center gap-10 lg:grid-cols-[1fr_0.9fr]">
        <div>
          <p className="mb-6 flex items-center gap-4 text-xs font-semibold uppercase tracking-[0.18em]">
            <span className="h-px w-9 bg-current" />
            {siteContent.hero.eyebrow}
          </p>
          <h1 className="font-serif-editorial max-w-2xl text-5xl leading-[1.05] md:text-6xl">
            {siteContent.hero.title}
          </h1>
          <p className="mt-6 max-w-xl text-lg leading-8 text-[var(--muted)]">{siteContent.hero.description}</p>
          <div className="mt-8 flex flex-wrap gap-4">
            <Button href="/contato">Agendar consulta</Button>
            <Button href="/atendimentos" variant="text">
              Conheça os atendimentos →
            </Button>
          </div>
        </div>
        <div className="relative mx-auto aspect-[4/3] w-full max-w-[520px] overflow-hidden">
          <Image
            alt="Retrato em ambiente de consultório usado como referência visual do site"
            className="object-cover"
            fill
            priority
            src="/images/hero-julia.png"
          />
        </div>
      </Container>
    </section>
  );
}
