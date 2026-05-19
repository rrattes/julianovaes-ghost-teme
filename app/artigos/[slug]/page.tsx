import { Container } from "@/components/Container";

type ArticlePageProps = {
  params: Promise<{ slug: string }>;
};

export default async function ArticlePage({ params }: ArticlePageProps) {
  const { slug } = await params;

  return (
    <Container className="py-20">
      <h1 className="font-serif-editorial text-5xl">Artigo</h1>
      <p className="mt-6 text-[var(--muted)]">Slug: {slug}</p>
    </Container>
  );
}
