import datetime as dt
import html
import json
import os
import secrets
import sqlite3
import uuid


ROOT = os.environ.get("PROJECT_ROOT") or os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.environ.get("GHOST_DB_PATH") or os.path.join(ROOT, "ghost-local", "content", "data", "ghost-local.db")


def ghost_id():
    return secrets.token_hex(12)


def now():
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%d %H:%M:%S")


def mobiledoc(markup):
    return json.dumps(
        {
            "version": "0.3.1",
            "atoms": [],
            "cards": [["html", {"html": markup}]],
            "markups": [],
            "sections": [[10, 0]],
            "ghostVersion": "4.0",
        },
        ensure_ascii=False,
    )


PAGES = [
    {
        "title": "Sobre mim",
        "slug": "sobre",
        "excerpt": "Psicóloga clínica com escuta cuidadosa, ética e abordagem fenomenológico-existencial.",
        "image": "/content/images/2026/05/post-psicoterapia.png",
        "html": """
<section class="page-panel page-panel-intro">
  <p>Acredito na importância de uma escuta verdadeira e na construção de um espaço seguro para que cada pessoa possa se compreender em sua singularidade.</p>
  <p>Minha atuação clínica parte de uma perspectiva fenomenológico-existencial, olhando para a experiência vivida, para os vínculos e para as possibilidades que podem se abrir quando uma história é acolhida com cuidado.</p>
</section>
<section class="page-split">
  <div>
    <p class="kicker">Escuta clínica</p>
    <h2>Um encontro ético, cuidadoso e singular</h2>
  </div>
  <div>
    <p>A psicoterapia não oferece respostas prontas. Ela cria um tempo de elaboração para que sentimentos, escolhas e relações possam ser vistos com mais clareza.</p>
    <p>O trabalho acontece em uma relação de presença, respeito e investigação conjunta, considerando a história de cada pessoa e o modo como ela se relaciona consigo, com os outros e com o mundo.</p>
  </div>
</section>
<section class="page-list">
  <h2>Como esse trabalho se orienta</h2>
  <ul>
    <li>Escuta atenta e sem julgamentos apressados.</li>
    <li>Cuidado com a singularidade de cada história.</li>
    <li>Reflexão sobre escolhas, vínculos e modos de existir.</li>
    <li>Construção de um espaço clínico seguro e respeitoso.</li>
  </ul>
</section>
""",
    },
    {
        "title": "Atendimentos",
        "slug": "atendimentos",
        "excerpt": "Cuidado psicológico para diferentes momentos, necessidades e formas de relação.",
        "image": "/content/images/2026/05/post-akna.png",
        "html": """
<section class="page-panel page-panel-intro">
  <p>Os atendimentos oferecem um espaço de escuta para compreender o que se vive, elaborar experiências e construir novas possibilidades de relação consigo e com outras pessoas.</p>
</section>
<section class="service-list">
  <article>
    <span>01</span>
    <h2>Psicoterapia individual</h2>
    <p>Um espaço para compreender sua história, emoções, padrões de relação e escolhas, com cuidado para que novos caminhos possam ser construídos com mais liberdade e sentido.</p>
  </article>
  <article>
    <span>02</span>
    <h2>Psicoterapia de casal</h2>
    <p>Acolhimento e reflexão para o casal cuidar da comunicação, fortalecer vínculos e encontrar modos mais verdadeiros de se relacionar.</p>
  </article>
  <article>
    <span>03</span>
    <h2>Psicoterapia de grupo</h2>
    <p>O encontro com outras histórias pode ampliar percepções, elaborar questões e construir pertencimento em um ambiente seguro.</p>
  </article>
</section>
<section class="page-cta">
  <div>
    <p class="kicker">Primeiro contato</p>
    <h2>Vamos conversar sobre o atendimento mais adequado?</h2>
  </div>
  <a class="button" href="/contato/">Entrar em contato</a>
</section>
""",
    },
    {
        "title": "Psicoterapia individual",
        "slug": "psicoterapia-individual",
        "excerpt": "Um espaço de escuta para compreender sua história, emoções, escolhas e modos de relação.",
        "image": "/content/images/2026/05/post-psicoterapia.png",
        "html": """
<section class="page-panel page-panel-intro">
  <p>A psicoterapia individual é um espaço de escuta para que você possa olhar com cuidado para sua história, seus sentimentos, seus vínculos e os modos como tem vivido suas escolhas.</p>
  <p>O processo não parte de respostas prontas. Ele se constrói no encontro, respeitando o tempo, a singularidade e as questões que aparecem para cada pessoa.</p>
</section>
<section class="page-split">
  <div>
    <p class="kicker">Cuidado individual</p>
    <h2>Um tempo para se escutar com mais clareza</h2>
  </div>
  <div>
    <p>Buscar terapia pode fazer sentido em momentos de sofrimento, ansiedade, luto, mudanças, conflitos relacionais ou quando algo parece se repetir e pede compreensão.</p>
    <p>A partir de uma escuta fenomenológico-existencial, o trabalho acompanha a experiência vivida e ajuda a abrir novas possibilidades de compreensão e escolha.</p>
  </div>
</section>
<section class="page-list">
  <h2>Quando pode ajudar</h2>
  <ul>
    <li>Momentos de angústia, ansiedade ou tristeza persistente.</li>
    <li>Dificuldades em escolhas, limites e relacoes.</li>
    <li>Processos de mudanca, perda ou transicao de vida.</li>
    <li>Desejo de compreender melhor a própria história.</li>
  </ul>
</section>
<section class="page-cta">
  <div>
    <p class="kicker">Disponibilidade</p>
    <h2>Vamos conversar sobre o que você está vivendo?</h2>
  </div>
  <a class="button" href="https://wa.me/5521999988956?text=Ol%C3%A1%2C%20Julia.%20Gostaria%20de%20solicitar%20disponibilidade%20para%20psicoterapia%20individual.">Solicitar disponibilidade</a>
</section>
""",
    },
    {
        "title": "Psicoterapia de casal",
        "slug": "psicoterapia-de-casal",
        "excerpt": "Um espaço de cuidado para o casal refletir sobre comunicação, vínculos, conflitos e possibilidades.",
        "image": "/content/images/2026/05/post-casamentos.png",
        "html": """
<section class="page-panel page-panel-intro">
  <p>A psicoterapia de casal oferece um espaço de escuta para que duas pessoas possam compreender como se relacionam, como se comunicam e que sentidos sustentam seus conflitos e escolhas.</p>
  <p>O objetivo não é apontar culpados, mas favorecer um diálogo mais cuidadoso, consciente e responsável sobre a relação.</p>
</section>
<section class="page-split">
  <div>
    <p class="kicker">Relação e vínculo</p>
    <h2>Escutar o casal sem perder a singularidade de cada pessoa</h2>
  </div>
  <div>
    <p>O processo pode ajudar casais que atravessam crises, dificuldades de comunicação, distanciamento, decisões importantes ou repetições que fragilizam o vínculo.</p>
    <p>A terapia cria condições para que o casal possa falar e ouvir de outro modo, reconhecendo impasses e possibilidades.</p>
  </div>
</section>
<section class="page-list">
  <h2>Temas frequentes</h2>
  <ul>
    <li>Comunicação difícil e conflitos recorrentes.</li>
    <li>Crises, separação, reaproximação ou transições.</li>
    <li>Expectativas, frustrações e combinados da vida a dois.</li>
    <li>Construção de escolhas mais conscientes sobre a relação.</li>
  </ul>
</section>
<section class="page-cta">
  <div>
    <p class="kicker">Disponibilidade</p>
    <h2>Quer conversar sobre a terapia de casal?</h2>
  </div>
  <a class="button" href="https://wa.me/5521999988956?text=Ol%C3%A1%2C%20Julia.%20Gostaria%20de%20solicitar%20disponibilidade%20para%20psicoterapia%20de%20casal.">Solicitar disponibilidade</a>
</section>
""",
    },
    {
        "title": "Psicoterapia de grupo",
        "slug": "psicoterapia-de-grupo",
        "excerpt": "Um espaço terapêutico em grupo para elaborar experiências, ampliar percepções e construir pertencimento.",
        "image": "/content/images/2026/05/post-akna.png",
        "html": """
<section class="page-panel page-panel-intro">
  <p>A psicoterapia de grupo possibilita que cada participante encontre um espaço de fala e escuta junto a outras histórias, reconhecendo diferenças, aproximações e novas formas de compreender o que vive.</p>
  <p>O grupo pode ampliar percepções e favorecer elaborações que nascem do encontro com outras pessoas em um ambiente seguro e conduzido clinicamente.</p>
</section>
<section class="page-split">
  <div>
    <p class="kicker">Encontro em grupo</p>
    <h2>Outras histórias também ajudam a compreender a própria</h2>
  </div>
  <div>
    <p>Em grupo, a experiência individual ganha novos contornos. Ao falar, ouvir e ser afetado pelo encontro, cada pessoa pode perceber modos de relação que talvez não aparecessem sozinha.</p>
    <p>O trabalho preserva o cuidado ético e o respeito ao tempo de cada participante.</p>
  </div>
</section>
<section class="page-list">
  <h2>O que o grupo pode oferecer</h2>
  <ul>
    <li>Escuta compartilhada em um ambiente seguro.</li>
    <li>Ampliação de percepções sobre si e os outros.</li>
    <li>Elaboração de experiências e questões comuns.</li>
    <li>Construção de pertencimento e novos sentidos.</li>
  </ul>
</section>
<section class="page-cta">
  <div>
    <p class="kicker">Disponibilidade</p>
    <h2>Vamos conversar sobre grupos disponíveis?</h2>
  </div>
  <a class="button" href="https://wa.me/5521999988956?text=Ol%C3%A1%2C%20Julia.%20Gostaria%20de%20solicitar%20disponibilidade%20para%20psicoterapia%20de%20grupo.">Solicitar disponibilidade</a>
</section>
""",
    },
    {
        "title": "Contato",
        "slug": "contato",
        "excerpt": "Entre em contato para conversar sobre disponibilidade, formato de atendimento e próximos passos.",
        "image": "/content/images/2026/05/post-casamentos.png",
        "html": """
<section class="contact-grid">
  <div class="contact-card">
    <p class="kicker">Disponibilidade</p>
    <h2>Solicitar disponibilidade</h2>
    <p>Entre em contato pelo WhatsApp para conversar sobre disponibilidade, formato de atendimento e próximos passos.</p>
    <a class="button" href="https://wa.me/5521999988956?text=Ol%C3%A1%2C%20Julia.%20Gostaria%20de%20solicitar%20disponibilidade%20de%20agenda.">Entrar em contato</a>
  </div>
  <div class="contact-details">
    <article>
      <h3>Atendimento</h3>
      <p>Presencial no Rio de Janeiro e online.</p>
    </article>
    <article>
      <h3>Local</h3>
      <p>Rua Engenheiro Enaldo Cravo Peixoto<br>Rio de Janeiro, RJ<br>20540-106</p>
    </article>
    <article>
      <h3>WhatsApp</h3>
      <p><a href="https://wa.me/5521999988956">(21) 99998-8956</a></p>
    </article>
  </div>
</section>
<section class="page-panel">
  <p>Ao entrar em contato, você pode contar brevemente o que busca neste momento. A partir disso, combinamos os próximos passos com cuidado e clareza.</p>
</section>
""",
    },
]


def plain_text(markup):
    return " ".join(html.unescape(markup.replace("<", " <")).split())


def main():
    if not os.path.exists(DB_PATH):
        raise SystemExit(f"Ghost database not found: {DB_PATH}")

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    author = cur.execute("select id from users order by created_at limit 1").fetchone()
    if not author:
        raise SystemExit("No Ghost user found to assign as author.")
    author_id = author[0]

    for page in PAGES:
        timestamp = now()
        text = plain_text(page["html"])
        existing = cur.execute("select id from posts where slug = ? and type = 'page'", (page["slug"],)).fetchone()
        if existing:
            page_id = existing[0]
            cur.execute(
                """
                update posts set
                  title = ?, mobiledoc = ?, lexical = null, html = ?, plaintext = ?,
                  feature_image = ?, featured = 0, status = 'published', type = 'page',
                  visibility = 'public', email_recipient_filter = 'none',
                  updated_at = ?, published_at = coalesce(published_at, ?), published_by = ?,
                  custom_excerpt = ?, show_title_and_feature_image = 1
                where id = ?
                """,
                (
                    page["title"],
                    mobiledoc(page["html"]),
                    page["html"],
                    text,
                    page["image"],
                    timestamp,
                    timestamp,
                    author_id,
                    page["excerpt"],
                    page_id,
                ),
            )
            cur.execute("delete from posts_authors where post_id = ?", (page_id,))
        else:
            page_id = ghost_id()
            cur.execute(
                """
                insert into posts (
                  id, uuid, title, slug, mobiledoc, lexical, html, comment_id,
                  plaintext, feature_image, featured, type, status, locale,
                  visibility, email_recipient_filter, created_at, updated_at,
                  published_at, published_by, custom_excerpt, codeinjection_head,
                  codeinjection_foot, custom_template, canonical_url, newsletter_id,
                  show_title_and_feature_image
                ) values (?, ?, ?, ?, ?, null, ?, ?, ?, ?, 0, 'page', 'published', null, 'public', 'none', ?, ?, ?, ?, ?, null, null, null, null, null, 1)
                """,
                (
                    page_id,
                    str(uuid.uuid4()),
                    page["title"],
                    page["slug"],
                    mobiledoc(page["html"]),
                    page["html"],
                    str(uuid.uuid4()),
                    text,
                    page["image"],
                    timestamp,
                    timestamp,
                    timestamp,
                    author_id,
                    page["excerpt"],
                ),
            )

        cur.execute(
            "insert into posts_authors (id, post_id, author_id, sort_order) values (?, ?, ?, 0)",
            (ghost_id(), page_id, author_id),
        )

    con.commit()
    con.close()
    print(f"Seeded {len(PAGES)} Ghost pages.")


if __name__ == "__main__":
    main()
