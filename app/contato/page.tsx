import { Container } from "@/components/Container";

export default function ContatoPage() {
  return (
    <Container className="py-20">
      <h1 className="font-serif-editorial text-5xl">Contato</h1>
      <p className="mt-6 max-w-2xl leading-7 text-[var(--muted)]">
        Dados de contato devem ser confirmados antes da publicação.
      </p>
    </Container>
  );
}
