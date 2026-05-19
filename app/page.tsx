import { AboutPreview } from "@/components/AboutPreview";
import { ArticleCard } from "@/components/ArticleCard";
import { Container } from "@/components/Container";
import { CTASection } from "@/components/CTASection";
import { Hero } from "@/components/Hero";
import { SectionTitle } from "@/components/SectionTitle";
import { ServiceCard } from "@/components/ServiceCard";
import { articles } from "@/lib/articles";
import { services } from "@/lib/services";

export default function Home() {
  return (
    <>
      <Hero />

      <section className="py-20">
        <Container>
          <SectionTitle
            eyebrow="Atendimentos"
            title="Cuidado psicológico para diferentes momentos e necessidades"
          />
          <div className="grid gap-5 md:grid-cols-3">
            {services.map((service) => (
              <ServiceCard key={service.slug} service={service} />
            ))}
          </div>
        </Container>
      </section>

      <AboutPreview />
      <CTASection />

      <section className="py-20">
        <Container className="grid gap-10 lg:grid-cols-[280px_1fr]">
          <SectionTitle
            align="left"
            eyebrow="Artigos"
            title="Reflexões para a vida e as relações"
          />
          <div className="grid gap-6 md:grid-cols-3">
            {articles.slice(0, 3).map((article) => (
              <ArticleCard key={article.slug} article={article} />
            ))}
          </div>
        </Container>
      </section>
    </>
  );
}
