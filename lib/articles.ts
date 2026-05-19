export type Article = {
  title: string;
  slug: string;
  href: string;
  description: string;
};

export const articles: Article[] = [
  {
    title: "É impossível ser feliz sozinho?",
    slug: "e-impossivel-ser-feliz-sozinho",
    href: "/artigos/e-impossivel-ser-feliz-sozinho",
    description: "Sobre solidão, escolha e relações verdadeiras."
  },
  {
    title: "Quando não dura para sempre",
    slug: "quando-nao-dura-para-sempre",
    href: "/artigos/quando-nao-dura-para-sempre",
    description: "Reflexões sobre término de relacionamentos e recomeços."
  },
  {
    title: "Casamentos: afinal, para quê?",
    slug: "casamentos-afinal-para-que",
    href: "/artigos/casamentos-afinal-para-que",
    description: "Sobre expectativas, idealizações e a vida a dois."
  }
];
