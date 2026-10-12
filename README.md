# Capi — seu dinheiro, de boa na lagoa


**Abrir o app:** https://gusvilella.github.io/Capi/ (atualiza sozinho a cada mudança publicada)

Web app simples para organizar o dinheiro do mês. Sem cadastro, sem instalação, sem servidor: o app inteiro está num único arquivo, `index.html`.

## Como abrir

Baixe o projeto, extraia a pasta e dê dois cliques no `index.html`. Também dá para publicar no GitHub Pages / Netlify / Vercel e usar no celular.

## Instalar no celular (app)

Para ter o app com ícone na tela inicial, abrindo em tela cheia e funcionando sem internet, ele precisa estar publicado num endereço. O jeito grátis é o GitHub Pages:

1. No GitHub, abra o repositório → **Settings** → **Pages**.
2. Em **Branch**, escolha a branch do app e a pasta `/ (root)` e clique em **Save**.
3. Depois de uns minutos o endereço aparece no topo da página (algo como `https://seu-usuario.github.io/Capi/`).
4. Abra esse endereço no celular:
   - **Android (Chrome)**: menu **⋮** → **Instalar app**.
   - **iPhone (Safari)**: **Compartilhar** → **Adicionar à Tela de Início**.

Na engrenagem também tem **Instalar como app**, com essas instruções.

No app instalado, segure o ícone para ver os atalhos **Lançamento rápido** e **Visão geral** (Android e computador).

Os dados ficam em cada aparelho. Para usar o mesmo conteúdo no celular e no computador, veja **Sincronizar** mais abaixo.

## Como funciona

No topo ficam os 4 números do mês:

- **Receita**: tudo o que entrou.
- **Investir**: quanto da receita você separa para investir. Em **Ajustar**, escolha a porcentagem ou digite o valor.
- **Despesas**: despesas fixas + variáveis.
- **Saldo**: em **Contas**, informe quanto tem em cada banco (Itaú, Bradesco, Nubank, Mercado Pago…); o cartão mostra a soma de todas, e embaixo a sobra do mês (receita − investir − despesas). Toque em "R$" para marcar uma conta como negativa (cheque especial). Com duas contas ou mais, *Transferir entre contas* move dinheiro de uma para outra sem contar como receita ou despesa. Os bancos aparecem com logo. Sem contas cadastradas, o cartão mostra só a sobra do mês.

**Visão geral** (primeira aba): um painel com a previsão do saldo nos próximos 30 dias (com aviso se a conta vai ficar negativa, a prévia das faturas ainda não lançadas e o detalhe de cada dia ao passar o mouse ou tocar), o calendário do mês com o que entra e sai em cada dia, para onde vai o dinheiro (todas as despesas), a fatura da vez de cada cartão com o uso do limite, e metas e patrimônio.

Os lançamentos ficam nas abas:

- **Receita**: salário, freelas etc. Marque *Receita recorrente* para repetir todo mês, ou *Recebimento futuro* para só contar quando você marcar como recebido.
- **Despesa fixa**: aluguel, internet, academia… Vale deste mês em diante, com dia de vencimento. Toque em *Pendente/Pago* para marcar o pagamento. O sino avisa as contas que vencem nos próximos dias.
- **Despesa variável**: gastos do dia a dia, com categoria. Marque *Parcelado* para dividir uma compra nos próximos meses.

- **Assinaturas**: Netflix, Spotify, Crunchyroll, Prime, Disney+ e outras, com logo. Escolha o serviço, o valor e se a cobrança é mensal ou anual (a anual só entra nas despesas no mês da renovação). Mostra o custo por mês e por ano, e o sino avisa as renovações dos próximos dias. Reajuste de preço vale deste mês em diante.
- **Cartões**: cadastre cada cartão com banco, bandeira (Visa, Mastercard, Elo, Amex, Hipercard, Diners), final, limite, dia de fechamento e de vencimento. Cada fatura tem datas reais (fecha dd/mm, vence dd/mm) e status pelas datas: **Aberta** (ainda recebendo compras), **A pagar** (fechada), **Vencida** ou **Paga**. No mês atual a aba mostra a fatura "da vez" de cada cartão, e as setas na janela da fatura navegam entre as faturas. Uma fatura vencida sem pagar tem o botão "Mover para a fatura de…", para corrigir valores lançados no mês errado. O sino avisa as faturas fechadas perto do vencimento ou vencidas.
- **Limite disponível**: com o limite cadastrado, cada cartão mostra quanto ainda tem livre (limite − faturas em aberto − compras e parcelas que ainda vão entrar). Compras parceladas no cartão caem uma parcela em cada fatura, e enquanto a fatura não é lançada aparece uma prévia com o que já está nela.
- **Valor que muda todo mês**: conta fixa (luz, água, gás) ou entrada mensal (salário) pode ser marcada como "o valor muda todo mês". Até você confirmar, o mês usa a média dos últimos 3 meses confirmados e aparece como "≈ estimado". Ao marcar a conta como paga (ou tocar em "Quanto caiu?" no salário), o app pergunta o valor de verdade daquele mês; editar o valor nessa conta muda só o mês aberto.
- **Pago com / Recebido em**: todo lançamento pode dizer de onde saiu ou pra onde foi: uma conta (Pix, débito, boleto) ou um cartão. O app lembra a última escolha. Conta: o saldo dela se atualiza sozinho (receitas somam, gastos descontam, na data do lançamento, até hoje). Cartão: a cobrança entra na fatura certa pela data (depois do fechamento, vai para a próxima) e, quando essa fatura é lançada, deixa de somar separado, porque já está dentro dela. No cadastro do cartão dá para dizer com qual conta a fatura é paga: ao marcar como paga, o valor sai dessa conta. Conta fixa ligada a um banco só sai do saldo quando você marca como paga (no dia em que marcou), pra nunca aparecer "atrasada" com o dinheiro já descontado. Corrigir um saldo à mão em Contas faz a conta recomeçar daquele valor.
- **Investimentos**: onde seu dinheiro está guardado (ex.: conta Mercado Pago a 120% do CDI, CDB, Tesouro). Informe o saldo e o rendimento (% do CDI, prefixado ou sem rendimento), e o app estima o saldo de hoje dia a dia (dias úteis) e quanto rende por mês. Em *Editar* dá para corrigir o saldo, aportar ou resgatar (e dizer de qual conta o dinheiro saiu ou para qual voltou). A taxa do CDI é buscada no Banco Central uma vez por dia; se não der, dá para ajustar clicando nela. Os valores são brutos, antes do IR.

**Importar extrato** (engrenagem → *Importar extrato do banco*): aceita CSV (Nubank conta e cartão, Inter, Itaú — inclusive o extrato sem cabeçalho —, C6 conta e cartão, Mercado Pago, Banco do Brasil e outros com colunas de data/descrição/valor, de entrada/saída ou com uma coluna de tipo débito/crédito, separados por vírgula ou ponto e vírgula), planilhas do Excel (.xlsx) e OFX. Mostra uma prévia para conferir: você diz de qual conta ou cartão é o extrato, cada lançamento vem com categoria sugerida (por palavras como iFood, posto, farmácia e pelo que você já categorizou antes) e o que já foi lançado, pagamentos de fatura e estornos vêm desmarcados. Dá para desfazer logo depois de importar.

- **Metas**: objetivos com valor e prazo (viagem, carro, reserva de emergência…). O app mostra o progresso e quanto guardar por mês para chegar lá. O guardado pode ser digitado (com o atalho *+ Guardar*) ou vir dos seus investimentos (soma o saldo estimado deles). O botão *Calcular reserva de emergência* usa 6 meses da sua média de despesas. O resumo avisa se as metas pedem mais do que você reserva em Investir.

- **Limite por categoria**: em *Gerenciar categorias* (aba Despesa variável), dê um limite por mês a cada categoria. A aba mostra uma barra por categoria (⚠️ a partir de 80%, ⛔ quando passa), a janela de nova despesa diz quanto ainda cabe, e o sino avisa.

**Evolução** (cartão embaixo das abas): colunas de receita × despesas dos últimos 6 ou 12 meses (passe o mouse ou toque para ver os valores, clique ou toque de novo para ir ao mês, ou *Ver tabela*, com total e média), e comparações automáticas: quanto você gastou a mais/menos que no mês anterior, as categorias que mais mudaram, a média de despesas, quanto sobrou da receita e o patrimônio (contas + investimentos, registrado mês a mês).

Cada aba tem um gráfico de rosca mostrando para onde vai o dinheiro, filtro/busca e **Gerenciar categorias** (nome e cor).

- **Busca em todos os meses**: no Filtro de Receita e Despesa variável, marque *Buscar em todos os meses* para achar um lançamento de qualquer mês e ver o total.
- **Duplicar**: na edição de uma receita ou despesa variável, *Duplicar* abre um lançamento igual com a data de hoje.
- **Compras parceladas**: ao editar uma parcela, *Aplicar a todas as parcelas* muda descrição, categoria e forma de pagamento de todas.
- **Desfazer**: depois de adicionar, editar, excluir, pagar fatura, restaurar backup ou apagar tudo, o aviso embaixo tem *Desfazer*.
- **Backup**: sem sincronização, o sininho lembra de fazer backup a cada 30 dias.

**Lançamento rápido** (botão **+** no canto, ou tecla `Q`): escreva do seu jeito, como `mercado 45,90 nubank`, `uber 23 crédito itaú`, `café 6,50 ontem`, `tv 2400 12x nubank` (parcelado), `transferi 200 nubank itau` (entre contas) ou `recebi 300 freela pix nubank`. O app entende valor, data, categoria, e se foi na conta ou no cartão (também pelo final, ex.: `cartão 8890`), e mostra o que entendeu antes de lançar. Gastos frequentes viram ⭐ favoritos: um toque e está lançado.

Outros detalhes:

- O olho no topo esconde os valores.
- Alterar algo recorrente num mês posterior vale daquele mês em diante, e o passado não muda. Ao excluir, dá para escolher *só este mês* (pula o mês) ou *deste mês em diante*.
- O ícone de lua/sol ao lado da engrenagem alterna entre tema claro e escuro.
- A engrenagem tem a escolha de fonte (Urbanist, Outfit, Sora, Parkinsans ou Syne, embutidas no arquivo, funcionam sem internet), exportação do mês ou de todos os meses para CSV (abre no Excel / Google Planilhas), backup e restauração.
- Atalhos: `N` novo lançamento, `Q` lançamento rápido, `/` buscar, `H` volta para o mês atual, `←` `→` troca o mês, `Esc` fecha. No celular, arraste o dedo para os lados para trocar o mês.

## Dados

Tudo fica salvo no `localStorage` do navegador. Faça backup pela engrenagem de vez em quando, porque limpar os dados do navegador apaga os lançamentos. Dados de versões anteriores do app são migrados automaticamente.

## Sincronizar celular e computador

Engrenagem → **Sincronizar entre aparelhos**. Usa um Gist secreto da sua conta do GitHub, de graça:

1. Crie um token no GitHub só com permissão de **gist** (o app tem o link direto).
2. Cole o token e crie uma **senha de sincronização**.
3. Nos outros aparelhos, conecte com **o mesmo token e a mesma senha**.

Os dados vão **criptografados** (AES-GCM 256, chave derivada da senha com PBKDF2): o GitHub só guarda texto embaralhado. Sem a senha não dá para recuperar o conteúdo da nuvem. Cada mudança sobe sozinha em poucos segundos e os outros aparelhos baixam ao abrir o app. Se os dois aparelhos mudarem ao mesmo tempo sem internet, vale a versão salva por último.

## Resumo do mês em PDF

Em **⚙ → Resumo do mês em PDF** (ou em "Resumo em PDF" na Visão geral) o app monta um relatório do mês que está na tela: receita, despesas, saldo, para onde foi o dinheiro, os últimos 6 meses, maiores gastos, contas fixas, assinaturas, cartões, patrimônio e metas. Na janela de impressão, escolha **Salvar como PDF**. No celular, use "Imprimir" e depois compartilhe como PDF. O relatório sai sempre em fundo branco, mesmo no tema escuro.

## Detector de assinaturas

O app olha seus gastos e acha o que parece assinatura: serviços conhecidos (Netflix, Spotify, ChatGPT…) e gastos que se repetem todo mês com valor parecido (academia, por exemplo). Aparece um aviso na aba **Assinaturas** e no sininho. É só revisar e tocar em **Adicionar**, ou em **Não é** para ele não perguntar de novo.

Quando você importa um extrato e uma assinatura veio com valor diferente, o app avisa ("Spotify subiu de R$ 21,90 para R$ 23,90") e atualiza o preço com um toque, guardando o valor antigo no histórico.

## Só eu ou em família

Na apresentação da primeira vez, o app pergunta **como vai usar**: **Só eu** ou **Em família** (casal ou a casa toda). Em família você coloca quem faz parte (Leo, Ane, Bia…). Dá pra mudar depois em **⚙ → Uso do app**.

Tudo continua sendo **um orçamento só**: os números somam tudo junto, do mesmo jeito. A família muda o jeito do app falar ("Boa noite, Leo e Ane", "Dinheiro de vocês") e deixa marcar **de quem é** cada entrada (o salário de cada um), gasto, cartão e banco, com uma bolinha com a inicial. Sem marcar, fica "da família".

- **Entradas por pessoa:** o card *Entrou* mostra quanto veio de cada um, e o gráfico de Entradas mostra *Por pessoa* ou *Por tipo*.
- **Bancos:** em *Meus bancos*, toque na bolinha de cada banco pra dizer de quem é (ou da família, numa conta conjunta).
- **Lançamento rápido:** o nome de alguém marca como dessa pessoa ("tênis 250 do leo"); "família" ou "nosso" marcam como da família.
- **Cada um no seu celular:** com a sincronização ligada, *Convidar alguém da família* gera um link e um código. A pessoa abre o link, passa pela apresentação do app e digita o código, sem precisar de conta no GitHub. O token vai criptografado no link e só abre com o código.
- **Lançando ao mesmo tempo:** a sincronização junta o que cada celular lançou, item por item, em vez de um substituir o outro.

## Primeira vez

Não tem cadastro nem senha. Na primeira vez, o app abre uma **apresentação em telas** (dá pra arrastar pro lado no celular): pergunta **como você quer ser chamado** (com sugestões de apelido: Fernanda → Fer, Nanda) e se vai usar **só você ou em família**, e mostra em telas animadas como o app funciona (entradas, contas fixas e gastos; o lançamento rápido; o gráfico e os avisos). Dá pra pular as explicações.

Em **⚙ → Seu nome** dá pra trocar o nome ou o apelido e **ver a apresentação de novo**. Os lançamentos ficam só neste aparelho; pra proteger, use **⚙ → Senha para abrir o app**.

## Senha e digital

Em **⚙ → Senha e digital** você cria um PIN de 4 dígitos para abrir o app. No celular (e no computador com Windows Hello / Touch ID) dá para ativar a **digital ou o rosto**. O app também se tranca sozinho quando fica mais de 1 minuto em segundo plano. O PIN não fica salvo em texto: só um hash dele fica no aparelho.

Esqueceu o PIN? Em "Esqueci a senha" você pode apagar os dados deste aparelho e depois recuperar tudo conectando a sincronização de novo (ou pelo backup).

## Logos

Os logos ficam embutidos no arquivo (funcionam sem internet):

- Bancos: [Bancos-em-SVG](https://github.com/Tgentil/Bancos-em-SVG)
- Serviços: [svgl](https://svgl.app) e [Simple Icons](https://simpleicons.org) (CC0)
- Bandeiras de cartão: [svg-credit-card-payment-icons](https://github.com/aaronfagan/svg-credit-card-payment-icons) (Apache 2.0)

Marcas sem logo disponível aparecem com a inicial na cor da marca. Não dá para enviar imagens próprias: só aparecem os logos que já vêm no app. O símbolo do Bradesco vem do pacote react-bancos (MIT). Nos gráficos, os símbolos de um tom só vêm do Simple Icons (CC0) e do @edusites/icons (MIT). As marcas pertencem aos seus donos e aparecem aqui só para identificar as contas, cartões e assinaturas de quem usa o app.
