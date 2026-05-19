type SectionTitleProps = {
  eyebrow: string;
  title: string;
  align?: "center" | "left";
};

export function SectionTitle({ eyebrow, title, align = "center" }: SectionTitleProps) {
  return (
    <div className={`mb-10 ${align === "center" ? "mx-auto max-w-2xl text-center" : "max-w-sm"}`}>
      <p className="mb-3 text-xs font-bold uppercase tracking-[0.16em] text-[var(--accent)]">{eyebrow}</p>
      <h2 className="font-serif-editorial text-4xl leading-tight text-[var(--text)]">{title}</h2>
    </div>
  );
}
