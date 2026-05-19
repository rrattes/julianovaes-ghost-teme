export type Service = {
  title: string;
  slug: string;
  href: string;
  description: string;
};

export const services: Service[] = [
  {
    title: "Psicoterapia Individual",
    slug: "psicoterapia-individual",
    href: "/atendimentos/psicoterapia-individual",
    description:
      "Um espaço de escuta para compreender sua história, emoções e padrões de relação e construir novos caminhos com mais liberdade e sentido."
  },
  {
    title: "Psicoterapia de Casal",
    slug: "psicoterapia-de-casal",
    href: "/atendimentos/psicoterapia-de-casal",
    description:
      "Acolhimento e reflexão para o casal cuidar da comunicação, fortalecer vínculos e encontrar novos modos de se relacionar."
  },
  {
    title: "Psicoterapia de Grupo",
    slug: "psicoterapia-de-grupo",
    href: "/atendimentos/psicoterapia-de-grupo",
    description:
      "O encontro com outras histórias ajuda a ampliar percepções, elaborar questões e construir pertencimento de forma segura."
  }
];
