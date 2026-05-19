import Link from "next/link";
import type { Article } from "@/lib/articles";

type ArticleCardProps = {
  article: Article;
};

export function ArticleCard({ article }: ArticleCardProps) {
  return (
    <article>
      <div className="mb-5 aspect-[5/3] bg-[var(--surface-soft)]" />
      <h3 className="text-lg font-semibold">{article.title}</h3>
      <p className="mt-2 text-sm leading-6 text-[var(--muted)]">{article.description}</p>
      <Link className="mt-5 inline-flex text-xs font-bold uppercase tracking-[0.1em]" href={article.href}>
        Ler artigo →
      </Link>
    </article>
  );
}
