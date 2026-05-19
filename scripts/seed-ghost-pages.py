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
        "title": "Psicoterapia individual",
        "slug": "psicoterapia-individual",
        "excerpt": "Um espaco de escuta para compreender sua historia, emocoes, escolhas e modos de relacao.",
        "image": "/content/images/2026/05/post-psicoterapia.png",
        "html": """
<section class="page-panel page-panel-intro">
  <p>A psicoterapia individual e um espaco de escuta para que voce possa olhar com cuidado para sua historia, seus sentimentos, seus vinculos e os modos como tem vivido suas escolhas.</p>
  <p>O processo nao parte de respostas prontas. Ele se constroi no encontro, respeitando o tempo, a singularidade e as questoes que aparecem para cada pessoa.</p>
</section>
<section class="page-split">
  <div>
    <p class="kicker">Cuidado individual</p>
    <h2>Um tempo para se escutar com mais clareza</h2>
  </div>
  <div>
    <p>Buscar terapia pode fazer sentido em momentos de sofrimento, ansiedade, luto, mudancas, conflitos relacionais ou quando algo parece se repetir e pede compreensao.</p>
    <p>A partir de uma escuta fenomenologico-existencial, o trabalho acompanha a experiencia vivida e ajuda a abrir novas possibilidades de compreensao e escolha.</p>
  </div>
</section>
<section class="page-list">
  <h2>Quando pode ajudar</h2>
  <ul>
    <li>Momentos de angustia, ansiedade ou tristeza persistente.</li>
    <li>Dificuldades em escolhas, limites e relacoes.</li>
    <li>Processos de mudanca, perda ou transicao de vida.</li>
    <li>Desejo de compreender melhor a propria historia.</li>
  </ul>
</section>
<section class="page-cta">
  <div>
    <p class="kicker">Agendamento</p>
    <h2>Vamos conversar sobre o que voce esta vivendo?</h2>
  </div>
  <a class="button" href="https://wa.me/5521999988956?text=Ola%2C%20Julia.%20Gostaria%20de%20saber%20mais%20sobre%20psicoterapia%20individual.">Chamar no WhatsApp</a>
</section>
""",
    },
    {
        "title": "Psicoterapia de casal",
        "slug": "psicoterapia-de-casal",
        "excerpt": "Um espaco de cuidado para o casal refletir sobre comunicacao, vinculos, conflitos e possibilidades.",
        "image": "/content/images/2026/05/post-casamentos.png",
        "html": """
<section class="page-panel page-panel-intro">
  <p>A psicoterapia de casal oferece um espaco de escuta para que duas pessoas possam compreender como se relacionam, como se comunicam e que sentidos sustentam seus conflitos e escolhas.</p>
  <p>O objetivo nao e apontar culpados, mas favorecer um dialogo mais cuidadoso, consciente e responsavel sobre a relacao.</p>
</section>
<section class="page-split">
  <div>
    <p class="kicker">Relacao e vinculo</p>
    <h2>Escutar o casal sem perder a singularidade de cada pessoa</h2>
  </div>
  <div>
    <p>O processo pode ajudar casais que atravessam crises, dificuldades de comunicacao, distanciamento, decisoes importantes ou repeticoes que fragilizam o vinculo.</p>
    <p>A terapia cria condicoes para que o casal possa falar e ouvir de outro modo, reconhecendo impasses e possibilidades.</p>
  </div>
</section>
<section class="page-list">
  <h2>Temas frequentes</h2>
  <ul>
    <li>Comunicacao dificil e conflitos recorrentes.</li>
    <li>Crises, separacao, reaproximacao ou transicoes.</li>
    <li>Expectativas, frustracoes e combinados da vida a dois.</li>
    <li>Construcao de escolhas mais conscientes sobre a relacao.</li>
  </ul>
</section>
<section class="page-cta">
  <div>
    <p class="kicker">Agendamento</p>
    <h2>Quer conversar sobre a terapia de casal?</h2>
  </div>
  <a class="button" href="https://wa.me/5521999988956?text=Ola%2C%20Julia.%20Gostaria%20de%20saber%20mais%20sobre%20psicoterapia%20de%20casal.">Chamar no WhatsApp</a>
</section>
""",
    },
    {
        "title": "Psicoterapia de grupo",
        "slug": "psicoterapia-de-grupo",
        "excerpt": "Um espaco terapeutico em grupo para elaborar experiencias, ampliar percepcoes e construir pertencimento.",
        "image": "/content/images/2026/05/post-akna.png",
        "html": """
<section class="page-panel page-panel-intro">
  <p>A psicoterapia de grupo possibilita que cada participante encontre um espaco de fala e escuta junto a outras historias, reconhecendo diferencas, aproximacoes e novas formas de compreender o que vive.</p>
  <p>O grupo pode ampliar percepcoes e favorecer elaboracoes que nascem do encontro com outras pessoas em um ambiente seguro e conduzido clinicamente.</p>
</section>
<section class="page-split">
  <div>
    <p class="kicker">Encontro em grupo</p>
    <h2>Outras historias tambem ajudam a compreender a propria</h2>
  </div>
  <div>
    <p>Em grupo, a experiencia individual ganha novos contornos. Ao falar, ouvir e ser afetado pelo encontro, cada pessoa pode perceber modos de relacao que talvez nao aparecessem sozinha.</p>
    <p>O trabalho preserva o cuidado etico e o respeito ao tempo de cada participante.</p>
  </div>
</section>
<section class="page-list">
  <h2>O que o grupo pode oferecer</h2>
  <ul>
    <li>Escuta compartilhada em um ambiente seguro.</li>
    <li>Ampliacao de percepcoes sobre si e os outros.</li>
    <li>Elaboracao de experiencias e questoes comuns.</li>
    <li>Construcao de pertencimento e novos sentidos.</li>
  </ul>
</section>
<section class="page-cta">
  <div>
    <p class="kicker">Agendamento</p>
    <h2>Vamos conversar sobre grupos disponiveis?</h2>
  </div>
  <a class="button" href="https://wa.me/5521999988956?text=Ola%2C%20Julia.%20Gostaria%20de%20saber%20mais%20sobre%20psicoterapia%20de%20grupo.">Chamar no WhatsApp</a>
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
