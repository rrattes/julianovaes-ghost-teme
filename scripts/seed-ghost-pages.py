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
        "excerpt": "Julia Novaes, psicóloga clínica CRP 05/35722, com atuação clínica desde 2007 e escuta orientada pela abordagem fenomenológico-existencial.",
        "meta_title": "Sobre Julia Novaes | Psicóloga clínica no Rio de Janeiro",
        "meta_description": "Conheça a trajetória de Julia Novaes, psicóloga clínica CRP 05/35722, com atuação desde 2007 em psicoterapia para adultos e casais.",
        "image": "/content/images/2026/05/post-psicoterapia.png",
        "html": """
<section class="page-panel page-panel-intro">
  <p>Julia Novaes é psicóloga clínica, CRP 05/35722, com atuação clínica desde 2007. Seu trabalho é voltado ao atendimento de adultos e casais, em um espaço de escuta cuidadosa, ética e reservado à singularidade de cada história.</p>
  <p>A clínica é compreendida como um encontro em que relações, escolhas, sofrimentos e modos de existir podem ser olhados com tempo, presença e responsabilidade.</p>
</section>
<section class="page-split">
  <div>
    <p class="kicker">Trajetória clínica</p>
    <h2>Uma prática construída entre consultório e saúde mental</h2>
  </div>
  <div>
    <p>Formada em Psicologia pelo Instituto Brasileiro de Medicina de Reabilitação (IBMR), Julia atua em consultório particular desde 2007.</p>
    <p>Sua formação inclui especialização em psicologia clínica na perspectiva fenomenológico-existencial pelo IFEN e especialização em saúde mental e atenção psicossocial pela ENSP/Fiocruz.</p>
  </div>
</section>
<section class="page-split">
  <div>
    <p class="kicker">Abordagem</p>
    <h2>Escuta fenomenológico-existencial</h2>
  </div>
  <div>
    <p>A abordagem fenomenológico-existencial orienta uma escuta atenta à experiência vivida, aos vínculos, às escolhas e às possibilidades que se apresentam em cada momento da vida.</p>
    <p>O processo terapêutico não parte de respostas prontas ou promessas de solução. Ele oferece um espaço clínico para compreender como cada pessoa se relaciona consigo, com os outros e com as exigências que atravessam sua história.</p>
  </div>
</section>
<section class="page-split">
  <div>
    <p class="kicker">Saúde mental</p>
    <h2>Experiência em serviços públicos e institucionais</h2>
  </div>
  <div>
    <p>Entre 2008 e 2014, Julia atuou em serviços de saúde mental no estado do Rio de Janeiro, incluindo CAPS, CAPSi, CAPSad, hospital psiquiátrico e residências terapêuticas.</p>
    <p>Essa experiência compõe uma trajetória clínica marcada pelo cuidado com diferentes formas de sofrimento psíquico e pela atenção à complexidade das histórias de vida.</p>
  </div>
</section>
<section class="page-list">
  <h2>Temas frequentes no consultório</h2>
  <ul>
    <li>Ansiedade, autocobrança, sobrecarga emocional e dificuldade de reconhecer limites.</li>
    <li>Conflitos afetivos, conjugais e familiares.</li>
    <li>Separações, reorganizações de vida e transições importantes.</li>
    <li>Dificuldades em escolhas, limites e relações.</li>
    <li>Questões relacionadas a vínculos, projetos de vida e modos de existir.</li>
  </ul>
</section>
<section class="page-cta">
  <div>
    <p class="kicker">Primeiro contato</p>
    <h2>Um espaço reservado para conversar sobre o que você está vivendo</h2>
  </div>
  <a class="button" href="https://wa.me/5521999988956?text=Ol%C3%A1%2C%20Julia.%20Gostaria%20de%20solicitar%20disponibilidade%20de%20agenda.">Solicitar disponibilidade de agenda</a>
</section>
""",
    },
    {
        "title": "Atendimentos",
        "slug": "atendimentos",
        "excerpt": "Cuidado psicológico para diferentes momentos, necessidades e formas de relação.",
        "meta_title": "Atendimentos em psicoterapia | Julia Novaes",
        "meta_description": "Psicoterapia para adultos e casais em temas como ansiedade, relações, escolhas, conflitos afetivos e transições importantes da vida.",
        "image": "/content/images/2026/05/post-akna.png",
        "html": """
<section class="page-panel page-panel-intro">
  <p>Os atendimentos oferecem um espaço de escuta para compreender o que se vive, elaborar experiências e construir novas possibilidades de relação consigo e com outras pessoas.</p>
</section>
<section class="service-list">
  <article>
    <span>01</span>
    <h2>Psicoterapia individual para adultos</h2>
    <p>Um espaço de escuta clínica para ansiedade, autocobrança, relações, escolhas e transições de vida.</p>
  </article>
  <article>
    <span>02</span>
    <h2>Terapia de casal</h2>
    <p>Um acompanhamento para casais que desejam compreender conflitos, silêncios, afastamentos e possibilidades de reconstrução ou elaboração.</p>
  </article>
  <article>
    <span>03</span>
    <h2>Psicoterapia online</h2>
    <p>Atendimento particular e reservado para adultos que buscam continuidade de cuidado com discrição e flexibilidade.</p>
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
        "meta_title": "Psicoterapia individual para adultos | Julia Novaes",
        "meta_description": "Psicoterapia individual para adultos que buscam elaborar ansiedade, autocobrança, relações, escolhas e transições de vida.",
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
    <li>Dificuldades em escolhas, limites e relações.</li>
    <li>Processos de mudança, perda ou transição de vida.</li>
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
        "title": "Psicoterapia particular online",
        "slug": "psicoterapia-particular-online",
        "excerpt": "Atendimento psicológico particular para adultos e casais, com escuta clínica, discrição e horário reservado.",
        "meta_title": "Psicoterapia particular online | Julia Novaes",
        "meta_description": "Atendimento psicológico particular online para adultos e casais, com escuta clínica, discrição e horário reservado.",
        "image": "/content/images/2026/05/post-psicoterapia.png",
        "html": """
<section class="page-panel page-panel-intro">
  <p>Um espaço clínico reservado para adultos e casais que buscam escuta, cuidado e elaboração em momentos de crise, mudança ou sofrimento emocional.</p>
</section>
<section class="page-split">
  <div>
    <p class="kicker">Atendimento particular</p>
    <h2>Para quem é este atendimento?</h2>
  </div>
  <div>
    <p>A psicoterapia particular online pode ser uma possibilidade para pessoas que desejam iniciar ou retomar um processo terapêutico com discrição, continuidade e horário reservado.</p>
    <p>O atendimento é voltado a adultos e casais que atravessam questões emocionais, relacionais ou existenciais e buscam um espaço de escuta clínica cuidadosa.</p>
  </div>
</section>
<section class="page-list">
  <h2>O que pode ser trabalhado em psicoterapia?</h2>
  <ul>
    <li>Ansiedade e sofrimento emocional.</li>
    <li>Autocobrança e sobrecarga.</li>
    <li>Conflitos afetivos e conjugais.</li>
    <li>Separações e reorganizações de vida.</li>
    <li>Escolhas importantes.</li>
    <li>Transições pessoais, familiares ou profissionais.</li>
    <li>Dificuldade de reconhecer limites.</li>
    <li>Questões relacionadas à história, aos vínculos e aos modos de viver.</li>
  </ul>
</section>
<section class="page-split">
  <div>
    <p class="kicker">Online</p>
    <h2>Atendimento online com discrição e continuidade</h2>
  </div>
  <div>
    <p>O formato online permite que o processo psicoterapêutico aconteça com regularidade, mesmo em rotinas mais complexas.</p>
    <p>Para isso, é importante que a pessoa esteja em um ambiente privado, com condições de fala e escuta, preservando o sigilo e a qualidade do encontro clínico.</p>
  </div>
</section>
<section class="page-cta">
  <div>
    <p class="kicker">Disponibilidade</p>
    <h2>Um primeiro contato reservado para compreender possibilidades de atendimento</h2>
  </div>
  <a class="button" href="https://wa.me/5521999988956?text=Ol%C3%A1%2C%20Julia.%20Gostaria%20de%20solicitar%20disponibilidade%20para%20psicoterapia%20particular%20online.">Solicitar disponibilidade de agenda</a>
</section>
""",
    },
    {
        "title": "Psicoterapia para pessoas em autocobrança e sobrecarga emocional",
        "slug": "psicoterapia-alta-exigencia-emocional",
        "excerpt": "Para quem sustenta muitas responsabilidades, decisões e relações — e percebe que seguir funcionando já não significa estar bem.",
        "meta_title": "Psicoterapia para autocobrança e sobrecarga emocional | Julia Novaes",
        "meta_description": "Psicoterapia para pessoas em autocobrança, sobrecarga emocional, dificuldade de reconhecer limites, relações e transições importantes.",
        "image": "/content/images/2026/05/post-psicoterapia.png",
        "html": """
<section class="page-panel page-panel-intro">
  <p>Para adultos, profissionais liberais, executivos, mulheres sobrecarregadas e pessoas em transições importantes que percebem que seguir funcionando já não significa estar bem.</p>
  <p>Um espaço clínico reservado para compreender o peso das responsabilidades, das escolhas, das relações e das exigências que atravessam a vida.</p>
</section>
<section class="page-split">
  <div>
    <p class="kicker">Quando procurar?</p>
    <h2>Quando funcionar no limite deixa de ser suficiente</h2>
  </div>
  <div>
    <p>Nem sempre o sofrimento aparece como uma crise evidente. Muitas vezes, ele se apresenta como cansaço constante, irritabilidade, dificuldade de descansar, necessidade de controle ou sensação de estar sempre em alerta. Por fora, a vida pode parecer organizada. Por dentro, algo começa a cobrar espaço.</p>
    <p>A psicoterapia pode ser buscada quando a pessoa percebe que tem funcionado no limite, mesmo mantendo suas responsabilidades. Não é preciso esperar que tudo desmorone para começar um processo de cuidado.</p>
  </div>
</section>
<section class="page-list">
  <h2>Temas frequentes</h2>
  <ul>
    <li>Ansiedade e excesso de antecipação.</li>
    <li>Autocobrança e dificuldade de reconhecer limites.</li>
    <li>Conflitos afetivos e conjugais.</li>
    <li>Decisões importantes de vida.</li>
    <li>Sensação de solidão mesmo em meio a muitas relações.</li>
    <li>Transições profissionais, familiares ou pessoais.</li>
    <li>Cansaço emocional de quem precisa dar conta de tudo.</li>
  </ul>
</section>
<section class="page-split">
  <div>
    <p class="kicker">Processo clínico</p>
    <h2>Como a psicoterapia pode ajudar</h2>
  </div>
  <div>
    <p>A psicoterapia oferece um espaço reservado para elaborar aquilo que, muitas vezes, não encontra lugar na rotina. O processo não busca respostas prontas nem soluções rápidas.</p>
    <p>A proposta é construir uma escuta cuidadosa sobre a forma como a pessoa se relaciona consigo, com os outros, com suas escolhas e com as exigências que atravessam sua vida.</p>
  </div>
</section>
<section class="page-cta">
  <div>
    <p class="kicker">Disponibilidade</p>
    <h2>Um primeiro contato discreto para entender possibilidades de atendimento</h2>
  </div>
  <a class="button" href="https://wa.me/5521999988956?text=Ol%C3%A1%2C%20Julia.%20Gostaria%20de%20solicitar%20disponibilidade%20de%20agenda%20para%20psicoterapia.">Solicitar disponibilidade de agenda</a>
</section>
""",
    },
    {
        "title": "Psicoterapia de casal",
        "slug": "psicoterapia-de-casal",
        "excerpt": "Um espaço de cuidado para o casal refletir sobre comunicação, vínculos, conflitos e possibilidades.",
        "meta_title": "Terapia de casal | Julia Novaes",
        "meta_description": "Terapia de casal para compreender conflitos, comunicação, afastamentos, escolhas e possibilidades de elaboração na relação.",
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
        "meta_title": "Psicoterapia de grupo | Julia Novaes",
        "meta_description": "Psicoterapia de grupo em um espaço clínico de escuta, elaboração de experiências, vínculos e construção de pertencimento.",
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
        "title": "Encaminhamentos profissionais",
        "slug": "encaminhamentos-profissionais",
        "excerpt": "Um canal para profissionais que desejam conhecer o trabalho clínico de Julia Novaes e realizar encaminhamentos responsáveis.",
        "meta_title": "Encaminhamentos profissionais | Julia Novaes",
        "meta_description": "Canal para profissionais conhecerem o trabalho clínico de Julia Novaes e realizarem encaminhamentos éticos e responsáveis.",
        "image": "/content/images/2026/05/post-psicoterapia.png",
        "html": """
<section class="page-panel page-panel-intro">
  <p>Um canal institucional para psiquiatras, médicos particulares, advogados de família, consultores de carreira, profissionais e instituições que atuam com cuidado individualizado em saúde, família, carreira e bem-estar e desejam conhecer o trabalho clínico de Julia Novaes e realizar encaminhamentos responsáveis.</p>
</section>
<section class="page-split">
  <div>
    <p class="kicker">Atuação clínica</p>
    <h2>Sobre a atuação clínica</h2>
  </div>
  <div>
    <p>Julia Novaes é psicóloga clínica, CRP 05/35722, com atuação voltada ao atendimento de adultos e casais.</p>
    <p>Seu trabalho se orienta por uma escuta clínica cuidadosa, considerando a singularidade de cada história, seus vínculos, escolhas e modos de existir.</p>
  </div>
</section>
<section class="page-list">
  <h2>Demandas frequentemente acompanhadas</h2>
  <ul>
    <li>Ansiedade e sofrimento emocional.</li>
    <li>Conflitos afetivos e conjugais.</li>
    <li>Separações e reorganizações de vida.</li>
    <li>Transições pessoais, familiares ou profissionais.</li>
    <li>Autocobrança, sobrecarga emocional e dificuldade de reconhecer limites.</li>
    <li>Questões relacionadas a vínculos, escolhas e projetos de vida.</li>
  </ul>
</section>
<section class="page-split">
  <div>
    <p class="kicker">Encaminhamento</p>
    <h2>Como encaminhar</h2>
  </div>
  <div>
    <p>Profissionais que desejam realizar um encaminhamento podem orientar a pessoa a entrar em contato diretamente pelo WhatsApp profissional ou pelo formulário do site.</p>
    <p>O primeiro contato é destinado ao envio de informações sobre disponibilidade, formato dos atendimentos e funcionamento do processo.</p>
  </div>
</section>
<section class="page-panel">
  <p><strong>Observação ética:</strong> os encaminhamentos são realizados de forma ética e responsável, sem qualquer comissão, contrapartida financeira ou promessa de vaga. A indicação deve ocorrer apenas quando fizer sentido clínico e profissional para a pessoa encaminhada.</p>
</section>
<section class="page-cta">
  <div>
    <p class="kicker">Contato profissional</p>
    <h2>Para encaminhamentos e informações institucionais</h2>
  </div>
  <a class="button" href="https://wa.me/5521999988956?text=Ol%C3%A1%2C%20Julia.%20Gostaria%20de%20falar%20sobre%20um%20encaminhamento%20profissional.">Entrar em contato</a>
</section>
""",
    },
    {
        "title": "Perguntas frequentes",
        "slug": "perguntas-frequentes",
        "excerpt": "Informações sobre atendimento psicológico, psicoterapia online, terapia de casal, sigilo, valores e disponibilidade de agenda.",
        "meta_title": "Perguntas frequentes | Julia Novaes",
        "meta_description": "Informações sobre atendimento psicológico, psicoterapia online, terapia de casal, sigilo, valores e disponibilidade de agenda.",
        "image": "/content/images/2026/05/post-psicoterapia.png",
        "html": """
<section class="page-panel page-panel-intro">
  <p>Algumas dúvidas costumam aparecer antes do início de um processo psicoterapêutico. Esta página reúne informações iniciais sobre formato dos atendimentos, sigilo, frequência, valores e primeiro contato.</p>
</section>
<section class="faq-list" aria-label="Perguntas frequentes sobre atendimento psicológico">
  <details open>
    <summary>A Julia atende por convênio?</summary>
    <p>Os atendimentos são particulares. Informações sobre valores e disponibilidade de horários são enviadas no primeiro contato profissional.</p>
  </details>
  <details>
    <summary>O atendimento é online ou presencial?</summary>
    <p>Os atendimentos podem acontecer online ou presencialmente, conforme disponibilidade de agenda e formato combinado no primeiro contato.</p>
  </details>
  <details>
    <summary>Como funciona o primeiro contato?</summary>
    <p>O primeiro contato pode ser feito pelo WhatsApp profissional ou pelo formulário do site. A partir dele, são enviadas informações sobre disponibilidade, valores, formato dos atendimentos e funcionamento do processo.</p>
  </details>
  <details>
    <summary>Qual é o valor da sessão?</summary>
    <p>Os valores são informados diretamente no primeiro contato. Essa escolha preserva um atendimento mais cuidadoso e permite apresentar as informações de acordo com o formato buscado: psicoterapia individual, terapia de casal ou outro acompanhamento disponível.</p>
  </details>
  <details>
    <summary>A terapia de casal é feita com os dois juntos?</summary>
    <p>Em geral, a terapia de casal envolve a presença dos dois parceiros no processo. A forma de condução, frequência e organização dos encontros é conversada no início do acompanhamento.</p>
  </details>
  <details>
    <summary>Com que frequência acontecem as sessões?</summary>
    <p>A frequência mais comum é semanal, mas isso pode variar de acordo com o tipo de atendimento, a disponibilidade de agenda e a avaliação clínica do processo.</p>
  </details>
  <details>
    <summary>A psicoterapia tem duração definida?</summary>
    <p>Não há uma duração única para todos os processos. A psicoterapia acompanha o tempo necessário de elaboração de cada pessoa ou casal, considerando a singularidade da história e das questões trazidas.</p>
  </details>
  <details>
    <summary>Como funciona o sigilo profissional?</summary>
    <p>O sigilo é parte fundamental do trabalho psicológico. As informações compartilhadas em atendimento são tratadas com cuidado, responsabilidade e de acordo com os princípios éticos da profissão.</p>
  </details>
  <details>
    <summary>Posso iniciar psicoterapia mesmo sem estar em crise?</summary>
    <p>Sim. A psicoterapia não precisa começar apenas em momentos de crise. Muitas pessoas procuram esse espaço para compreender melhor sua história, seus vínculos, suas escolhas e seus modos de viver.</p>
  </details>
  <details>
    <summary>Como solicitar disponibilidade de agenda?</summary>
    <p>Você pode entrar em contato pelo WhatsApp profissional ou pelo formulário do site. A disponibilidade de horários será verificada e as informações iniciais serão enviadas em seguida.</p>
  </details>
</section>
<section class="page-cta">
  <div>
    <p class="kicker">Primeiro contato</p>
    <h2>Para conversar sobre disponibilidade e formato de atendimento</h2>
  </div>
  <a class="button" href="https://wa.me/5521999988956?text=Ol%C3%A1%2C%20Julia.%20Gostaria%20de%20solicitar%20disponibilidade%20de%20agenda.">Solicitar disponibilidade de agenda</a>
</section>
""",
    },
    {
        "title": "Contato",
        "slug": "contato",
        "excerpt": "Entre em contato para conversar sobre disponibilidade, formato de atendimento e próximos passos.",
        "meta_title": "Contato | Julia Novaes Psicóloga",
        "meta_description": "Entre em contato para informações sobre disponibilidade de agenda, psicoterapia para adultos e casais, atendimento presencial e online.",
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
        meta_title = page.get("meta_title", page["title"])
        meta_description = page.get("meta_description", page["excerpt"])
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
        existing_meta = cur.execute("select id from posts_meta where post_id = ?", (page_id,)).fetchone()
        if existing_meta:
            cur.execute(
                """
                update posts_meta set
                  meta_title = ?, meta_description = ?,
                  og_title = ?, og_description = ?,
                  twitter_title = ?, twitter_description = ?
                where post_id = ?
                """,
                (
                    meta_title,
                    meta_description,
                    meta_title,
                    meta_description,
                    meta_title,
                    meta_description,
                    page_id,
                ),
            )
        else:
            cur.execute(
                """
                insert into posts_meta (
                  id, post_id, meta_title, meta_description,
                  og_title, og_description, twitter_title, twitter_description
                ) values (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    ghost_id(),
                    page_id,
                    meta_title,
                    meta_description,
                    meta_title,
                    meta_description,
                    meta_title,
                    meta_description,
                ),
            )

    con.commit()
    con.close()
    print(f"Seeded {len(PAGES)} Ghost pages.")


if __name__ == "__main__":
    main()
