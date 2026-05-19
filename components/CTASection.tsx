import { Button } from "@/components/Button";
import { Container } from "@/components/Container";

export function CTASection() {
  return (
    <section className="bg-[var(--accent)] py-10 text-white">
      <Container className="grid items-center gap-6 lg:grid-cols-[1fr_auto]">
        <div>
          <h2 className="font-serif-editorial text-4xl">Agende sua consulta</h2>
          <p className="mt-3 max-w-lg text-white/80">
            Vamos conversar sobre o que você está vivendo e sobre como posso te acompanhar.
          </p>
        </div>
        <div className="flex flex-wrap gap-3">
          <Button href="/contato" variant="secondary">
            Agendar pelo WhatsApp
          </Button>
          <Button href="/contato" variant="secondary">
            Outras formas de contato
          </Button>
        </div>
      </Container>
    </section>
  );
}
