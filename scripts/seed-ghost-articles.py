import datetime as dt
import html
import json
import os
import secrets
import shutil
import sqlite3
import textwrap
import uuid


ROOT = os.environ.get("PROJECT_ROOT") or os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.environ.get("GHOST_DB_PATH") or os.path.join(ROOT, "ghost-local", "content", "data", "ghost-local.db")
IMAGES_TARGET = os.environ.get("GHOST_IMAGES_TARGET") or os.path.join(ROOT, "ghost-local", "content", "images", "2026", "05")
IMAGE_SOURCES = {
    "post-relacao-fim.png": os.path.join(ROOT, "ghost-theme", "julia-novaes", "assets", "images", "posts", "post-relacao-fim.png"),
    "post-casamentos.png": os.path.join(ROOT, "ghost-theme", "julia-novaes", "assets", "images", "posts", "post-casamentos.png"),
    "post-feliz-sozinho.png": os.path.join(ROOT, "ghost-theme", "julia-novaes", "assets", "images", "posts", "post-feliz-sozinho.png"),
    "post-akna.png": os.path.join(ROOT, "ghost-theme", "julia-novaes", "assets", "images", "posts", "post-akna.png"),
    "post-engravidar.png": os.path.join(ROOT, "ghost-theme", "julia-novaes", "assets", "images", "posts", "post-engravidar.png"),
    "post-psicoterapia.png": os.path.join(ROOT, "ghost-theme", "julia-novaes", "assets", "images", "posts", "post-psicoterapia.png"),
}


def ghost_id():
    return secrets.token_hex(12)


def now():
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%d %H:%M:%S")


def paragraph_html(paragraphs):
    return "\n".join(f"<p>{html.escape(p)}</p>" for p in paragraphs)


def plaintext(paragraphs):
    return "\n\n".join(paragraphs)


def mobiledoc(paragraphs):
    sections = [[1, "p", [[0, [], 0, p]]] for p in paragraphs]
    return json.dumps(
        {
            "version": "0.3.1",
            "atoms": [],
            "cards": [],
            "markups": [],
            "sections": sections,
            "ghostVersion": "4.0",
        },
        ensure_ascii=False,
    )


ARTICLES = [
    {
        "title": "É possível uma relação chegar ao fim de forma saudável?",
        "slug": "quando-nao-dura-para-sempre",
        "date": "2016-07-14 12:00:00",
        "image": "/content/images/2026/05/post-relacao-fim.png",
        "excerpt": "Reflexões sobre término, comunicação, respeito e as possibilidades que se abrem diante de uma decisão difícil.",
        "tags": ["Artigos", "Relacionamentos Afetivos", "Terapia de Casal"],
        "paragraphs": [
            "O fim de uma relação nunca é fácil. Ainda assim, é importante refletir sobre o que leva ao término, o que ele significa para cada pessoa envolvida e, principalmente, cuidar para que a comunicação seja a mais clara possível.",
            "Outro ponto fundamental para qualquer relação, especialmente no momento em que ela pode estar chegando ao fim, é o respeito mútuo. É importante que cada um consiga respeitar seus próprios desejos e sentimentos, assim como os do parceiro ou parceira.",
            "Pode parecer simples respeitar os próprios sentimentos, mas terminar uma relação é dar adeus a muitos projetos em comum, reconstruir projetos pessoais e abrir mão de uma vida que já foi desejada em algum momento.",
            "Geralmente não há um momento exato em que é possível identificar o fim do relacionamento. É um processo, um dar-se conta aos poucos do que está acontecendo e do que se está sentindo.",
            "Conversar em momentos em que ambos estejam dispostos a ouvir e falar com calma pode ser transformador. Essas conversas permitem perceber se ainda há desejo de construir a relação ou se o caminho possível é encerrá-la.",
            "Quando um casal consegue manter esse diálogo, a decisão de continuar ou terminar torna-se mais potente, e fica mais fácil olhar para as possibilidades que se abrem diante da decisão tomada.",
        ],
    },
    {
        "title": "Casamentos felizes não precisam durar para sempre",
        "slug": "casamentos-felizes-nao-precisam-durar-para-sempre",
        "date": "2016-07-11 12:00:00",
        "image": "/content/images/2026/05/post-casamentos.png",
        "excerpt": "Nem todo fim invalida uma história. Um olhar maduro sobre amor, separação e responsabilidade.",
        "tags": ["Artigos", "Relacionamentos Afetivos", "Terapia de Casal"],
        "paragraphs": [
            "Quando duas pessoas decidem se casar, é porque existem projetos em comum. Querem construir uma vida a dois e, provavelmente, no dia do casamento, sentem um desejo forte de ficarem juntas.",
            "Mas nem sempre o casamento dura todo esse tempo. Quando vem a separação, muitas vezes fica a sensação de que o amor não era verdadeiro, de que houve um fracasso ou de que foi tempo perdido.",
            "Em alguns casos, o casamento foi realmente difícil, com muitos conflitos e dificuldades na comunicação. Em outros, pode ter sido próspero pelo tempo que durou, com experiências felizes, projetos compartilhados e conquistas importantes.",
            "Talvez o amor não esteja ligado necessariamente a uma relação perfeita ou duradoura, mas a uma vontade de estar junto ao outro e crescer com ele. Essa vontade pode, em algum momento, tornar-se inviável na relação.",
            "O amor pode se transformar ou deixar de existir sem que isso invalide tudo o que proporcionou e construiu durante sua existência. O difícil é reconhecer isso no momento do término.",
            "Olhar para as experiências passadas, reconhecer o que trouxeram de bom e encarar a própria responsabilidade sobre parte do que passou é fundamental para as futuras experiências amorosas ou não.",
        ],
    },
    {
        "title": "“É impossível ser feliz sozinho”. Será?",
        "slug": "e-impossivel-ser-feliz-sozinho",
        "date": "2016-04-27 12:00:00",
        "image": "/content/images/2026/05/post-feliz-sozinho.png",
        "excerpt": "Sobre solidão, desejo de relação estável e a construção de vínculos possíveis.",
        "tags": ["Artigos", "Relacionamentos Afetivos"],
        "paragraphs": [
            "A música de Tom Jobim é facilmente interpretada como uma afirmação de que, para sermos felizes, precisamos necessariamente estar em um relacionamento amoroso. Mas será que isso é sempre uma verdade?",
            "Muitas pessoas dizem que sim, que só se sentem realizadas quando vivem uma relação estável. É compreensível: relações estáveis podem proporcionar companheirismo, segurança, cumplicidade e muitos outros afetos.",
            "É comum criarmos uma ideia de relacionamento baseada no que o mundo nos diz. O mundo, através das relações, nos dá pistas do que buscamos e do que imaginamos encontrar em uma relação.",
            "No entanto, cada pessoa é única, com seus próprios desejos, sentimentos e formas de expressá-los. Cada relação também é única, e não há garantia do que poderá ocorrer no futuro.",
            "Não há relação que, sozinha, consiga realizar alguém. Isso só cada pessoa pode fazer por si, ainda que muitas vezes conte com a ajuda de outras pessoas.",
            "Quando um relacionamento precisa ocupar o lugar de realização pessoal para qualquer um dos parceiros, fica com um peso difícil de ser carregado, tornando-se muitas vezes inviável.",
            "Podemos encontrar diferentes maneiras de nos relacionar com cada pessoa. Companheirismo, cumplicidade e amor podem aparecer de muitas formas diferentes, não apenas em uma relação amorosa estável.",
        ],
    },
    {
        "title": "Grupo terapêutico AKNA",
        "slug": "grupo-terapeutico-akna",
        "date": "2016-02-26 12:00:00",
        "image": "/content/images/2026/05/post-akna.png",
        "excerpt": "Uma proposta de apoio psicológico e social para mulheres em tratamento de fertilidade ou FIV.",
        "tags": ["Artigos", "Gravidez e maternidade", "Psicoterapia de Grupo"],
        "paragraphs": [
            "O Grupo terapêutico AKNA traz uma proposta terapêutica focada no apoio psicológico e social para mulheres que tentam engravidar, que estejam em tratamento de fertilidade ou FIV.",
            "Com a formação de um grupo psicoterápico e a utilização de recursos arteterapêuticos, o projeto visa oferecer às participantes a possibilidade de expressar seus sentimentos, compreendê-los, organizá-los e transformá-los.",
            "Com o apoio e a assistência de terapeutas, a experiência do tratamento médico, da expectativa, da idealização e das possíveis frustrações pode ser vivida de uma forma consciente e construtiva.",
            "O grupo tem como objetivo central oferecer, por meio da terapia de grupo, experiências transformadoras que contribuam para o fortalecimento psíquico dessas mulheres.",
            "Akna, na mitologia Inuit, representa a deusa da fertilidade e do parto e, na mitologia Maia, a deusa da maternidade e do nascimento.",
        ],
    },
    {
        "title": "Perdi o momento certo para engravidar?",
        "slug": "perdi-o-momento-certo-para-engravidar",
        "date": "2016-02-23 12:00:00",
        "image": "/content/images/2026/05/post-engravidar.png",
        "excerpt": "Reflexões sobre maternidade, desejo, pressão social e caminhos possíveis diante da dificuldade de engravidar.",
        "tags": ["Artigos", "Gravidez e maternidade", "Tratamento Individual"],
        "paragraphs": [
            "Quando um casal está junto há algum tempo, é comum que venha o desejo de ter filhos. Isso não é uma regra, mas é frequente.",
            "Nos últimos anos, especialmente nas classes média e alta, muitas mulheres têm escolhido ter filhos mais tarde, quando a carreira e a vida parecem mais organizadas.",
            "Mas nem sempre a vida segue os planos com a facilidade imaginada. Algumas vezes, quando se decide que é a hora certa, surgem dificuldades inesperadas, como a dificuldade de engravidar.",
            "Vivenciar uma situação como essa pode trazer muitos questionamentos, ansiedade e angústia. Também é preciso lidar com a pressão externa de uma sociedade que ainda espera que todo casal tenha filhos.",
            "Para lidar com esses sentimentos, é importante lembrar do próprio desejo, do que o sustenta e do sentido que ele tem para a vida de cada pessoa.",
            "Se esse desejo permanece cheio de sentido, pode ser necessário buscar caminhos possíveis: conversar com profissionais, compreender se há questões orgânicas envolvidas e pensar em outras formas de realizar esse projeto.",
        ],
    },
    {
        "title": "Psicoterapia",
        "slug": "psicoterapia",
        "date": "2016-01-07 12:00:00",
        "image": "/content/images/2026/05/post-psicoterapia.png",
        "excerpt": "O que é psicoterapia, como funciona e quando esse espaço pode trazer benefícios.",
        "tags": ["Artigos", "Terapia", "Tratamento Individual"],
        "paragraphs": [
            "Apesar de ser bastante comum ouvirmos falar sobre fazer psicoterapia, muitas vezes não conseguimos definir bem o que é uma psicoterapia, como funciona ou quando devemos buscar um psicoterapeuta.",
            "É comum, e até saudável, passarmos por momentos difíceis na vida. Isso não significa que devemos buscar psicoterapia a cada situação difícil.",
            "No entanto, algumas vezes nos encontramos presos a situações que se prolongam a ponto de prejudicar nossas relações ou trazer um sofrimento do qual não conseguimos sair.",
            "É quando a psicoterapia pode trazer benefícios. Ela pode ser compreendida como um processo, já que não se propõe a uma resolução imediata de um problema e acontece a cada encontro com o terapeuta.",
            "A relação terapeuta-paciente, construída sessão a sessão, possibilita ao paciente levar suas questões para o espaço da terapia, desvelando seu modo de ser e abrindo possibilidades de intervenção.",
            "No espaço psicoterapêutico é possível ouvir-se, perceber-se e olhar de novos modos para aquilo que nos mobiliza. A psicoterapia oferece um espaço de cuidado e reflexão sobre nossas construções na vida.",
        ],
    },
]


def ensure_images():
    os.makedirs(IMAGES_TARGET, exist_ok=True)
    for filename, source in IMAGE_SOURCES.items():
        if os.path.exists(source):
            shutil.copyfile(source, os.path.join(IMAGES_TARGET, filename))


def ensure_tag(cur, name):
    slug = (
        name.lower()
        .replace("á", "a")
        .replace("à", "a")
        .replace("ã", "a")
        .replace("â", "a")
        .replace("é", "e")
        .replace("ê", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ô", "o")
        .replace("õ", "o")
        .replace("ú", "u")
        .replace("ç", "c")
        .replace(" ", "-")
    )
    existing = cur.execute("select id from tags where slug = ?", (slug,)).fetchone()
    if existing:
        return existing[0]

    tag_id = ghost_id()
    timestamp = now()
    cur.execute(
        """
        insert into tags (
          id, name, slug, description, feature_image, parent_id, visibility,
          og_image, og_title, og_description, twitter_image, twitter_title,
          twitter_description, meta_title, meta_description, codeinjection_head,
          codeinjection_foot, canonical_url, accent_color, created_at, updated_at
        ) values (?, ?, ?, null, null, null, 'public', null, null, null, null, null, null, null, null, null, null, null, null, ?, ?)
        """,
        (tag_id, name, slug, timestamp, timestamp),
    )
    return tag_id


def main():
    if not os.path.exists(DB_PATH):
        raise SystemExit(f"Ghost database not found: {DB_PATH}")

    ensure_images()

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    author = cur.execute("select id from users order by created_at limit 1").fetchone()
    if not author:
        raise SystemExit("No Ghost user found to assign as author.")
    author_id = author[0]

    cur.execute("update posts set status = 'draft', updated_at = ? where slug = 'coming-soon'", (now(),))

    for article in ARTICLES:
        existing = cur.execute("select id from posts where slug = ? and type = 'post'", (article["slug"],)).fetchone()
        timestamp = now()
        article_html = paragraph_html(article["paragraphs"])
        article_text = plaintext(article["paragraphs"])
        article_mobiledoc = mobiledoc(article["paragraphs"])

        if existing:
            post_id = existing[0]
            cur.execute(
                """
                update posts set
                  title = ?, mobiledoc = ?, lexical = null, html = ?, plaintext = ?,
                  feature_image = ?, featured = 0, status = 'published', type = 'post',
                  visibility = 'public', email_recipient_filter = 'none',
                  updated_at = ?, published_at = ?, published_by = ?,
                  custom_excerpt = ?, show_title_and_feature_image = 1
                where id = ?
                """,
                (
                    article["title"],
                    article_mobiledoc,
                    article_html,
                    article_text,
                    article["image"],
                    timestamp,
                    article["date"],
                    author_id,
                    article["excerpt"],
                    post_id,
                ),
            )
            cur.execute("delete from posts_tags where post_id = ?", (post_id,))
            cur.execute("delete from posts_authors where post_id = ?", (post_id,))
        else:
            post_id = ghost_id()
            cur.execute(
                """
                insert into posts (
                  id, uuid, title, slug, mobiledoc, lexical, html, comment_id,
                  plaintext, feature_image, featured, type, status, locale,
                  visibility, email_recipient_filter, created_at, updated_at,
                  published_at, published_by, custom_excerpt, codeinjection_head,
                  codeinjection_foot, custom_template, canonical_url, newsletter_id,
                  show_title_and_feature_image
                ) values (?, ?, ?, ?, ?, null, ?, ?, ?, ?, 0, 'post', 'published', null, 'public', 'none', ?, ?, ?, ?, ?, null, null, null, null, null, 1)
                """,
                (
                    post_id,
                    str(uuid.uuid4()),
                    article["title"],
                    article["slug"],
                    article_mobiledoc,
                    article_html,
                    str(uuid.uuid4()),
                    article_text,
                    article["image"],
                    article["date"],
                    timestamp,
                    article["date"],
                    author_id,
                    article["excerpt"],
                ),
            )

        cur.execute(
            "insert into posts_authors (id, post_id, author_id, sort_order) values (?, ?, ?, 0)",
            (ghost_id(), post_id, author_id),
        )

        for index, tag_name in enumerate(article["tags"]):
            tag_id = ensure_tag(cur, tag_name)
            cur.execute(
                "insert into posts_tags (id, post_id, tag_id, sort_order) values (?, ?, ?, ?)",
                (ghost_id(), post_id, tag_id, index),
            )

    con.commit()
    con.close()
    print(f"Seeded {len(ARTICLES)} Ghost articles.")


if __name__ == "__main__":
    main()
