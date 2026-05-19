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
        "excerpt": "Psicologa clinica com escuta cuidadosa, etica e abordagem fenomenologico-existencial.",
        "image": "/content/images/2026/05/post-psicoterapia.png",
        "html": """
<section class="page-panel page-panel-intro">
  <p>Acredito na importancia de uma escuta verdadeira e na construcao de um espaco seguro para que cada pessoa possa se compreender em sua singularidade.</p>
  <p>Minha atuacao clinica parte de uma perspectiva fenomenologico-existencial, olhando para a experiencia vivida, para os vinculos e para as possibilidades que podem se abrir quando uma historia e acolhida com cuidado.</p>
</section>
<section class="page-split">
  <div>
    <p class="kicker">Escuta clinica</p>
    <h2>Um encontro etico, cuidadoso e singular</h2>
  </div>
  <div>
    <p>A psicoterapia nao oferece respostas prontas. Ela cria um tempo de elaboracao para que sentimentos, escolhas e relacoes possam ser vistos com mais clareza.</p>
    <p>O trabalho acontece em uma relacao de presenca, respeito e investigacao conjunta, considerando a historia de cada pessoa e o modo como ela se relaciona consigo, com os outros e com o mundo.</p>
  </div>
</section>
<section class="page-list">
  <h2>Como esse trabalho se orienta</h2>
  <ul>
    <li>Escuta atenta e sem julgamentos apressados.</li>
    <li>Cuidado com a singularidade de cada historia.</li>
    <li>Reflexao sobre escolhas, vinculos e modos de existir.</li>
    <li>Construcao de um espaco clinico seguro e respeitoso.</li>
  </ul>
</section>
""",
    },
    {
        "title": "Atendimentos",
        "slug": "atendimentos",
        "excerpt": "Cuidado psicologico para diferentes momentos, necessidades e formas de relacao.",
        "image": "/content/images/2026/05/post-akna.png",
        "html": """
<section class="page-panel page-panel-intro">
  <p>Os atendimentos oferecem um espaco de escuta para compreender o que se vive, elaborar experiencias e construir novas possibilidades de relacao consigo e com outras pessoas.</p>
</section>
<section class="service-list">
  <article>
    <span>01</span>
    <h2>Psicoterapia individual</h2>
    <p>Um espaco para compreender sua historia, emocoes, padroes de relacao e escolhas, com cuidado para que novos caminhos possam ser construidos com mais liberdade e sentido.</p>
  </article>
  <article>
    <span>02</span>
    <h2>Psicoterapia de casal</h2>
    <p>Acolhimento e reflexao para o casal cuidar da comunicacao, fortalecer vinculos e encontrar modos mais verdadeiros de se relacionar.</p>
  </article>
  <article>
    <span>03</span>
    <h2>Psicoterapia de grupo</h2>
    <p>O encontro com outras historias pode ampliar percepcoes, elaborar questoes e construir pertencimento em um ambiente seguro.</p>
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
        "title": "Contato",
        "slug": "contato",
        "excerpt": "Entre em contato para conversar sobre disponibilidade, formato de atendimento e proximos passos.",
        "image": "/content/images/2026/05/post-casamentos.png",
        "html": """
<section class="contact-grid">
  <div class="contact-card">
    <p class="kicker">Agendamento</p>
    <h2>Para marcar uma consulta</h2>
    <p>Entre em contato pelo WhatsApp para conversar sobre disponibilidade, formato de atendimento e proximos passos.</p>
    <a class="button" href="https://wa.me/5521999988956">Chamar no WhatsApp</a>
  </div>
  <div class="contact-details">
    <article>
      <h3>Atendimento</h3>
      <p>Presencial e online a confirmar.</p>
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
  <p>Ao entrar em contato, voce pode contar brevemente o que busca neste momento. A partir disso, combinamos os proximos passos com cuidado e clareza.</p>
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
