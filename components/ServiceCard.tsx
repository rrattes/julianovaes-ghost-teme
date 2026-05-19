import Link from "next/link";
import type { Service } from "@/lib/services";

type ServiceCardProps = {
  service: Service;
};

export function ServiceCard({ service }: ServiceCardProps) {
  return (
    <article className="border border-[var(--border)] bg-[var(--surface)] p-7">
      <h3 className="font-serif-editorial text-3xl leading-tight">{service.title}</h3>
      <p className="mt-5 leading-7 text-[var(--muted)]">{service.description}</p>
      <Link className="mt-6 inline-flex text-xs font-bold uppercase tracking-[0.1em]" href={service.href}>
        Saiba mais →
      </Link>
    </article>
  );
}
