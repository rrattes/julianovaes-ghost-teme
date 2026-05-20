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
        "title": "O cansaço de quem parece sempre dar conta",
        "slug": "cansaco-de-quem-parece-sempre-dar-conta",
        "date": "2026-05-20 12:00:00",
        "image": "/content/images/2026/05/post-psicoterapia.png",
        "excerpt": "Um olhar clínico sobre o cansaço emocional de quem sustenta responsabilidades, vínculos e cobranças sem encontrar espaço para reconhecer seus próprios limites.",
        "meta_description": "Um olhar clínico sobre o cansaço emocional de quem sustenta responsabilidades, vínculos e cobranças sem encontrar espaço para reconhecer seus próprios limites.",
        "tags": ["Artigos", "Psicoterapia", "Ansiedade"],
        "paragraphs": [
            "Há um tipo de cansaço que nem sempre aparece como exaustão visível. A pessoa trabalha, responde mensagens, cuida de prazos, acompanha a família, toma decisões, organiza a rotina e, por fora, parece seguir bem. Talvez receba elogios pela competência, pela força, pela capacidade de resolver problemas. Mas por dentro pode existir uma sensação constante de alerta, como se relaxar fosse perigoso ou como se qualquer pausa colocasse tudo em risco.",
            "Esse cansaço costuma se instalar justamente em pessoas que aprenderam a funcionar. Funcionam mesmo com medo, mesmo com tristeza, mesmo com dúvidas, mesmo com o corpo pedindo descanso. Em muitos casos, não se trata de falta de recursos. Ao contrário: são pessoas que desenvolveram muitos recursos para sustentar responsabilidades. O problema é que, com o tempo, esses mesmos recursos podem virar uma prisão silenciosa.",
            "Dar conta pode se tornar uma identidade. A pessoa passa a se reconhecer, e a ser reconhecida, como aquela que resolve, ampara, antecipa e suporta. Quando isso acontece, pedir ajuda pode parecer falha. Descansar pode parecer descuido. Dizer não pode parecer abandono. A vida vai se organizando em torno da exigência de permanecer disponível, lúcida e produtiva, mesmo quando internamente já não há espaço.",
            "O sofrimento, então, nem sempre vem como uma crise evidente. Pode aparecer como irritabilidade, dificuldade de dormir, impaciência com pequenas demandas, sensação de estar sempre atrasado para a própria vida. Pode surgir como uma incapacidade de aproveitar o silêncio, como uma mente que não desliga, como um corpo que só percebe o peso quando a agenda finalmente desacelera.",
            "Muitas pessoas chegam à psicoterapia dizendo que não sabem exatamente o que está errado. A vida parece organizada. As obrigações estão sendo cumpridas. As relações seguem existindo. Mas algo ficou estreito. A pessoa percebe que responde ao mundo de modo automático, que perdeu espontaneidade, que vive administrando riscos, expectativas e demandas. É como se a existência tivesse se reduzido a desempenho.",
            "A autocobrança costuma ocupar um lugar central nesse processo. Ela pode ter sido, em algum momento, uma forma de proteção, uma maneira de conquistar autonomia, reconhecimento ou segurança. Mas quando a cobrança se torna permanente, ela deixa de orientar e passa a consumir. A pessoa já não faz apenas o que precisa ser feito; ela precisa fazer bem, rápido, sem falhar, sem incomodar, sem precisar demais.",
            "O descanso, nesse cenário, não é vivido como repouso. É vivido como ameaça. Ao parar, aparecem pensamentos, pendências, culpa, medo de perder controle. Algumas pessoas só conseguem descansar quando adoecem, quando o corpo interrompe aquilo que a vontade insistia em manter. Outras seguem, mas com uma espécie de distanciamento afetivo: estão presentes nas tarefas, porém ausentes de si.",
            "A psicoterapia não entra nesse campo como uma técnica para produzir mais equilíbrio rapidamente. Ela oferece, antes, um espaço de escuta para aquilo que ficou sem lugar. Um espaço onde a pessoa pode começar a ouvir o próprio cansaço sem imediatamente transformá-lo em problema a ser resolvido. Isso é importante porque nem todo cansaço pede apenas férias, organização de agenda ou mudança de hábito. Às vezes ele aponta para uma forma inteira de se relacionar com a vida.",
            "Escutar o cansaço significa perguntar, com cuidado, de que modo a pessoa aprendeu a sustentar tanto. O que está em jogo quando ela não consegue decepcionar? Que medo aparece quando ela precisa dizer que não pode? Que lugar ela ocupa nas relações quando se torna indispensável? Essas perguntas não têm respostas simples, mas podem abrir uma compreensão mais profunda sobre escolhas, vínculos e limites.",
            "Em alguns processos, fica evidente que a dificuldade de reconhecer limites não nasce de descuido consigo. Muitas vezes ela nasce de uma história em que foi necessário amadurecer cedo, responder demais, cuidar demais ou provar valor. O que hoje aparece como excesso pode ter sido, em outro tempo, uma forma possível de seguir. A clínica não precisa condenar essa forma; precisa compreendê-la para que outras possibilidades possam surgir.",
            "Também é importante distinguir responsabilidade de fusão com a responsabilidade. Ser responsável não significa estar permanentemente disponível. Cuidar dos outros não significa desaparecer de si. Sustentar uma vida adulta não deveria exigir a perda completa de silêncio, descanso e desejo. Ainda assim, para muitas pessoas, essa separação não é evidente. Ela precisa ser construída pouco a pouco, em um trabalho de elaboração.",
            "A psicoterapia pode ajudar a pessoa a perceber onde sua presença está sendo convocada e onde sua ausência também poderia existir sem destruir tudo. Pode ajudar a reconhecer que limites não são apenas barreiras impostas aos outros, mas formas de preservar condições de encontro, trabalho, amor e continuidade. Um limite bem compreendido não empobrece a vida; ele impede que a vida se torne apenas obrigação.",
            "O cansaço de quem parece sempre dar conta merece ser levado a sério justamente porque costuma ser invisível. Ele se esconde atrás da competência, da autonomia e da imagem de força. Mas aquilo que não aparece também atua. E, muitas vezes, começa a cobrar seu lugar no corpo, nas relações e na forma como a pessoa se percebe.",
            "Começar um processo terapêutico pode ser uma maneira de interromper, com delicadeza, a obrigação de seguir funcionando sem escuta. Não para abandonar responsabilidades, mas para recolocar a pessoa dentro da própria vida. Julia Novaes realiza atendimentos psicológicos particulares para adultos e casais. Informações sobre disponibilidade de agenda podem ser solicitadas pelo site.",
        ],
    },
    {
        "title": "Quando a relação funciona por fora, mas se esvazia por dentro",
        "slug": "relacao-funciona-por-fora-mas-esvazia-por-dentro",
        "date": "2026-05-19 12:00:00",
        "image": "/content/images/2026/05/post-casamentos.png",
        "excerpt": "Nem toda crise de casal aparece em discussões intensas. Algumas relações se desgastam no silêncio, na distância e na perda gradual de intimidade.",
        "meta_description": "Nem toda crise de casal aparece em discussões intensas. Algumas relações se desgastam no silêncio, na distância e na perda gradual de intimidade.",
        "tags": ["Artigos", "Relacionamentos Afetivos", "Terapia de Casal"],
        "paragraphs": [
            "Nem toda crise de casal se apresenta como briga. Algumas relações continuam funcionando de maneira quase impecável por fora. A casa segue organizada, os compromissos são cumpridos, as responsabilidades são divididas, os filhos são cuidados, as famílias continuam sendo visitadas. Para quem olha de fora, talvez nada pareça muito diferente. Mas, por dentro da relação, algo vai perdendo presença.",
            "Esse esvaziamento costuma ser difícil de nomear. Não há necessariamente uma traição, uma ruptura clara ou um conflito que explique tudo. O que existe é uma distância que se acumula. Conversas que ficam práticas demais. Silêncios que já não repousam, apenas separam. Pequenas tentativas de aproximação que não encontram resposta. Uma convivência que permanece, mas já não produz encontro.",
            "Muitos casais demoram a buscar ajuda justamente porque a relação ainda funciona. Há rotina, história, afeto, projetos e responsabilidades compartilhadas. Em alguns casos, existe respeito e até carinho. O sofrimento não está na ausência completa de vínculo, mas na sensação de que o vínculo perdeu vitalidade. Estar junto deixa de significar sentir-se acompanhado.",
            "Quando isso acontece, cada pessoa pode viver a crise de forma diferente. Uma sente falta de conversa. Outra sente cobrança quando é chamada a falar. Uma tenta se aproximar. A outra se protege no silêncio. Uma nomeia a distância. A outra diz que está tudo normal, que é apenas uma fase, que a vida adulta é assim. Aos poucos, o casal passa a discutir não apenas os problemas, mas a própria existência dos problemas.",
            "O esvaziamento de uma relação raramente acontece de repente. Ele pode ser produzido por anos de pequenos desencontros, frustrações não elaboradas, ressentimentos guardados, expectativas que nunca foram conversadas com cuidado. Em certas relações, o silêncio não é falta de assunto; é uma forma de defesa. Fala-se menos porque falar passou a machucar, cansar ou parecer inútil.",
            "Também é comum que a vida prática engula a vida afetiva. O casal se torna uma equipe eficiente para administrar casa, trabalho, família e finanças, mas perde o espaço de intimidade que sustentava a escolha de estar junto. A parceria permanece, porém o desejo de partilha se enfraquece. Em alguns momentos, isso gera culpa, porque a pessoa reconhece qualidades no outro, mas já não sabe onde foi parar a proximidade.",
            "A terapia de casal pode oferecer um espaço para que essa experiência seja olhada sem pressa e sem julgamento. Ela não existe para decidir quem está certo, nem para forçar uma reconciliação. Também não deve funcionar como uma tentativa desesperada de restaurar uma versão idealizada do passado. O trabalho clínico busca compreender como a relação se construiu, onde se estreitou e o que ainda pode ser dito.",
            "Em um processo de casal, muitas vezes o mais importante não é encontrar imediatamente uma solução, mas criar condições para que o casal consiga escutar a si mesmo de outro modo. Há frases que, em casa, já chegam carregadas de defesas antigas. Há pedidos que soam como acusações. Há medos que aparecem disfarçados de irritação. O espaço terapêutico pode ajudar a desacelerar essas repetições.",
            "É frequente que um casal procure terapia perguntando se ainda há caminho. Essa pergunta é legítima, mas nem sempre pode ser respondida rapidamente. Antes dela, talvez seja necessário compreender que relação existe hoje, não apenas aquela que existiu no início. O casal precisa reconhecer o que foi preservado, o que foi perdido, o que foi ferido e o que ainda encontra possibilidade de cuidado.",
            "Em alguns casos, o processo favorece uma reconstrução. Não como retorno simples ao que era antes, mas como elaboração de uma nova forma de estar junto, mais consciente dos limites, das diferenças e das necessidades de cada um. Em outros casos, a terapia ajuda a reconhecer que a relação chegou a um limite. Mesmo assim, essa compreensão pode acontecer com mais responsabilidade, especialmente quando há filhos, história e decisões importantes envolvidas.",
            "Separar-se também pode exigir elaboração. Há casais que não precisam apenas decidir se continuam ou terminam; precisam compreender o que viveram, o que repetiram, o que esperavam um do outro e o que não pôde ser construído. Uma separação atravessada sem escuta pode prolongar a dor em acusações, disputas e ressentimentos. Uma separação elaborada não elimina o sofrimento, mas pode evitar que ele se transforme em destruição.",
            "Falar sobre o esvaziamento de uma relação exige cuidado porque ele costuma vir acompanhado de ambivalência. A pessoa pode amar e estar cansada. Pode reconhecer valor na história e, ainda assim, sentir solidão. Pode desejar proximidade e temer novas frustrações. A clínica precisa sustentar essa complexidade, sem reduzir a experiência a escolha simples entre ficar ou ir embora.",
            "Quando a relação funciona por fora, mas se esvazia por dentro, o sofrimento tende a ser discreto e persistente. Ele aparece na falta de vontade de contar algo, no alívio quando o outro se ausenta, na sensação de que conversas importantes foram adiadas por tempo demais. Olhar para isso não significa condenar a relação. Significa reconhecer que aquilo que se mantém também precisa ser cuidado.",
            "A terapia de casal pode ser um espaço para compreender o que ainda une, o que distancia e o que precisa ganhar palavra. Não promete reconciliação, nem deve transformar a permanência em obrigação. Oferece uma escuta para que o casal possa se aproximar da verdade possível daquele vínculo. Julia Novaes realiza atendimentos psicológicos particulares para adultos e casais. Informações sobre disponibilidade de agenda podem ser solicitadas pelo site.",
        ],
    },
    {
        "title": "Psicoterapia não é apenas para momentos de crise",
        "slug": "psicoterapia-nao-e-apenas-para-momentos-de-crise",
        "date": "2026-05-18 12:00:00",
        "image": "/content/images/2026/05/post-feliz-sozinho.png",
        "excerpt": "A psicoterapia também pode ser um espaço de cuidado contínuo, elaboração e compreensão da própria história, mesmo quando a vida ainda parece estar funcionando.",
        "meta_description": "A psicoterapia também pode ser um espaço de cuidado contínuo, elaboração e compreensão da própria história, mesmo quando a vida ainda parece estar funcionando.",
        "tags": ["Artigos", "Psicoterapia", "Terapia"],
        "paragraphs": [
            "Muitas pessoas chegam à psicoterapia depois de um limite. Um término, uma crise de ansiedade, um luto, uma decisão difícil, um conflito familiar, uma exaustão que já não permite continuar do mesmo modo. Há algo compreensível nisso: quando o sofrimento se torna incontornável, buscar ajuda parece mais autorizado. A crise, de certa maneira, dá permissão para parar.",
            "Mas a psicoterapia não precisa começar apenas quando a vida desmorona. Ela também pode começar quando a pessoa percebe que está vivendo de modo estreito, repetindo escolhas, adiando perguntas importantes ou sustentando uma rotina que funciona, mas já não encontra sentido suficiente. Nem todo sofrimento chega como urgência. Alguns aparecem como empobrecimento gradual da relação consigo e com o mundo.",
            "Existe uma ideia ainda bastante presente de que terapia é recurso para momentos graves. Essa ideia faz com que muitas pessoas esperem demais. Tentam resolver sozinhas, racionalizam, ocupam-se, conversam rapidamente com amigos, mudam a agenda, procuram distrações. Às vezes isso ajuda. Outras vezes, apenas adia a escuta de algo que insiste em retornar.",
            "Quando a vida ainda está funcionando, o sofrimento pode ser mais difícil de reconhecer. A pessoa trabalha, se relaciona, cumpre tarefas, toma decisões. Por isso, tende a duvidar da legitimidade do que sente. Pode pensar que não tem motivo suficiente para procurar terapia, que outras pessoas sofrem mais, que seria exagero abrir esse espaço. Essa comparação costuma silenciar experiências que mereceriam atenção.",
            "A clínica não se organiza apenas em torno de sintomas evidentes. Ela também se interessa pelos modos de viver. Pela forma como uma pessoa escolhe, ama, se defende, espera, se cobra, se cala, suporta, se afasta ou se aproxima. Às vezes, o que leva alguém à terapia não é uma crise delimitada, mas a percepção de que certas formas de existir já não cabem como antes.",
            "A psicoterapia pode ser um lugar para elaborar a própria história sem precisar transformá-la em explicação fechada. Há experiências que continuam atuando na vida adulta mesmo quando parecem antigas. Formas de se vincular, expectativas sobre si, medos de decepcionar, dificuldade de receber cuidado, necessidade de controle. Nem tudo isso aparece como problema imediato, mas pode atravessar relações e escolhas de maneira persistente.",
            "Começar terapia antes do limite não significa procurar problemas onde eles não existem. Significa reconhecer que a vida emocional não precisa ser cuidada apenas quando entra em colapso. Muitas vezes, o cuidado contínuo permite perceber com mais delicadeza aquilo que estava sendo empurrado para depois. E esse depois, quando se acumula, pode se tornar pesado demais.",
            "Há pessoas que procuram psicoterapia em momentos de transição. Uma mudança profissional, a saída de um filho de casa, o início ou fim de uma relação, uma reorganização familiar, uma nova fase da vida adulta. Nem sempre essas situações são vividas como crise, mas podem abrir perguntas importantes: o que ainda faz sentido? O que foi construído até aqui? Que escolhas se repetem? Que vida se deseja sustentar?",
            "Outras procuram porque percebem um distanciamento de si. Não sabem dizer exatamente o que sentem, têm dificuldade de nomear desejos, vivem respondendo ao que é esperado, mas pouco se perguntam sobre o que de fato querem. A psicoterapia pode oferecer um tempo diferente daquele da produtividade. Um tempo de escuta, de elaboração e de construção de linguagem para experiências que talvez nunca tenham encontrado lugar.",
            "Esse processo não precisa prometer transformação rápida. Ao contrário, parte de sua importância está justamente em permitir uma aproximação mais cuidadosa daquilo que não se resolve por decisão imediata. Há questões que precisam ser compreendidas em sua complexidade. Há sofrimentos que não desaparecem porque alguém decidiu pensar positivo. Há escolhas que só podem amadurecer quando a pessoa se escuta com menos pressa.",
            "A psicoterapia também não substitui a vida. Ela não decide pela pessoa, não entrega respostas universais, não ensina uma forma correta de existir. O que ela pode oferecer é um espaço para que a pessoa observe como tem vivido, que sentidos atribui ao que acontece, como responde às exigências e que possibilidades talvez estejam encobertas por medo, hábito ou repetição.",
            "Em um contexto em que tantas pessoas estão sempre disponíveis, aceleradas e exigidas, ter um espaço reservado para falar sem precisar performar clareza já é algo significativo. Na clínica, a pessoa pode chegar confusa, contraditória, cansada, ambivalente. Não precisa transformar sua experiência em discurso perfeito. Pode, aos poucos, reconhecer o que sente e o que evita sentir.",
            "Buscar terapia antes de uma crise extrema também pode ser uma forma de responsabilidade consigo. Não no sentido moral de obrigação de autocuidado, mas no sentido de reconhecer que a própria vida merece atenção antes de chegar ao esgotamento. Existem perguntas que, se ouvidas mais cedo, talvez não precisem aparecer depois como ruptura.",
            "A psicoterapia é um espaço de cuidado, mas também de elaboração. Ela acompanha vínculos, escolhas, perdas, desejos e modos de viver. Pode começar em uma crise, mas não se reduz a ela. Muitas vezes, começa quando a pessoa percebe que continuar funcionando não é o mesmo que estar bem. Julia Novaes realiza atendimentos psicológicos particulares para adultos e casais. Informações sobre disponibilidade de agenda podem ser solicitadas pelo site.",
        ],
    },
    {
        "title": "O que se repete nas relações também merece escuta",
        "slug": "o-que-se-repete-nas-relacoes-tambem-merece-escuta",
        "date": "2026-05-17 12:00:00",
        "image": "/content/images/2026/05/post-relacao-fim.png",
        "excerpt": "Alguns sofrimentos aparecem como repetição: escolhas parecidas, conflitos semelhantes e formas de vínculo que parecem retornar em diferentes momentos da vida.",
        "meta_description": "Alguns sofrimentos aparecem como repetição: escolhas parecidas, conflitos semelhantes e formas de vínculo que parecem retornar em diferentes momentos da vida.",
        "tags": ["Artigos", "Relacionamentos Afetivos", "Psicoterapia"],
        "paragraphs": [
            "Alguns sofrimentos não aparecem como acontecimento isolado. Eles retornam. Mudam os nomes, os cenários, as fases da vida, mas algo parece se repetir. A pessoa se vê novamente em relações onde precisa provar valor, onde sente que fala e não é escutada, onde teme ser abandonada, onde se aproxima de quem se mantém distante, ou onde transforma afeto em esforço permanente.",
            "Falar em repetição nas relações exige cuidado. Não se trata de reduzir experiências complexas a fórmulas simples, nem de dizer que alguém escolhe sofrer. Relações acontecem entre pessoas, histórias, circunstâncias, desejos e limites. Ainda assim, quando certas formas de vínculo retornam muitas vezes, talvez haja algo ali que mereça ser escutado com mais atenção.",
            "A repetição pode aparecer na escolha de parceiros emocionalmente indisponíveis, mas também pode surgir em amizades, relações familiares, ambientes de trabalho e modos de se posicionar diante dos outros. Às vezes a pessoa ocupa sempre o lugar de quem entende, espera, cede, cuida, desculpa. Outras vezes se percebe sempre desconfiando, testando, antecipando perdas ou se retirando antes de ser rejeitada.",
            "Esses movimentos não surgem do nada. Muitas vezes, são formas de proteção que tiveram sentido em algum momento da vida. Alguém que aprendeu cedo a não incomodar pode, na vida adulta, ter dificuldade de pedir. Alguém que precisou se defender de instabilidade pode viver o vínculo como ameaça. Alguém que recebeu amor condicionado ao desempenho pode buscar reconhecimento onde deveria encontrar encontro.",
            "Na experiência cotidiana, porém, a repetição raramente aparece com essa clareza. Ela costuma ser percebida depois, quando a dor já se instalou. A pessoa olha para trás e percebe semelhanças entre relações que pareciam diferentes. Frases parecidas, sensações parecidas, finais parecidos. Pode surgir vergonha, impaciência consigo ou a impressão de que deveria ter aprendido antes. A clínica precisa cuidar para que essa percepção não se transforme em nova cobrança.",
            "Compreender uma repetição não é culpar a pessoa pelo que vive. É criar condições para que ela reconheça seu modo de participar das relações sem apagar a responsabilidade dos outros. Esse ponto é importante. A psicoterapia não deve transformar toda dor relacional em problema individual. Mas também não precisa retirar da pessoa a possibilidade de compreender seus movimentos, seus medos e seus modos de escolha.",
            "Algumas repetições se sustentam porque oferecem familiaridade. O familiar nem sempre é bom, mas é reconhecível. Uma relação que exige esforço demais pode parecer natural para quem aprendeu que amor precisa ser conquistado o tempo todo. Um vínculo frio pode parecer suportável para quem se acostumou a receber pouco. A ausência, quando é antiga, pode ser confundida com normalidade.",
            "Outras repetições se organizam em torno da esperança. A pessoa se envolve, insiste, tenta fazer diferente, acredita que desta vez será possível ser vista, escolhida ou acolhida. Há algo profundamente humano nisso. O problema não está em desejar encontro, mas em permanecer presa a lugares onde o desejo se transforma em espera sem retorno, em esforço solitário ou em renúncia constante de si.",
            "Na psicoterapia, a repetição pode ser observada sem pressa. Não como diagnóstico rápido, mas como uma trama que vai se revelando aos poucos. O que acontece quando alguém se aproxima? O que a pessoa teme perder se disser o que sente? Que tipo de cuidado ela espera e que tipo de cuidado consegue receber? Em que momentos ela se abandona para preservar o vínculo?",
            "Essas perguntas não têm a função de produzir respostas bonitas. Elas ajudam a aproximar a pessoa de sua experiência. Muitas vezes, antes de mudar uma forma de se relacionar, é preciso compreendê-la. É preciso reconhecer o que ela protege, o que ela repete, o que ela evita e que preço cobra. Mudanças impostas de fora tendem a ser frágeis quando não atravessam essa compreensão.",
            "Também é necessário considerar que relações não se repetem apenas pela escolha de pessoas parecidas. Às vezes, repetem-se pela forma como a pessoa se posiciona quando sente medo, desejo ou insegurança. Ela pode se calar para não perder, controlar para não ser surpreendida, agradar para não frustrar, afastar-se para não depender. Cada movimento tem uma história, ainda que no presente produza sofrimento.",
            "Escutar a repetição é diferente de procurar culpa. É sustentar a pergunta sobre como certos caminhos se tornaram possíveis e por que continuam sendo percorridos mesmo quando machucam. Essa escuta pode abrir pequenas diferenças. Talvez a pessoa perceba mais cedo quando está se apagando. Talvez consiga nomear uma necessidade sem transformá-la em acusação. Talvez reconheça um limite antes de ultrapassá-lo novamente.",
            "Não há garantia de que compreender uma repetição elimine imediatamente sua força. A vida emocional não se reorganiza por decreto. Mas a compreensão pode diminuir a estranheza, a vergonha e a sensação de estar condenado a viver sempre a mesma história. Quando algo ganha linguagem, deixa de atuar apenas no silêncio. Pode ser olhado, questionado, elaborado.",
            "O que se repete nas relações merece escuta porque costuma carregar uma tentativa antiga de cuidado, proteção ou pertencimento. A psicoterapia pode ajudar a pessoa a reconhecer esses movimentos sem se reduzir a eles. Não para prometer relações sem conflito, mas para abrir modos mais conscientes de estar com os outros e consigo. Julia Novaes realiza atendimentos psicológicos particulares para adultos e casais. Informações sobre disponibilidade de agenda podem ser solicitadas pelo site.",
        ],
    },
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

        meta_title = article.get("meta_title", article["title"])
        meta_description = article.get("meta_description", article["excerpt"])
        existing_meta = cur.execute("select id from posts_meta where post_id = ?", (post_id,)).fetchone()
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
                    post_id,
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
                    post_id,
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
    print(f"Seeded {len(ARTICLES)} Ghost articles.")


if __name__ == "__main__":
    main()
