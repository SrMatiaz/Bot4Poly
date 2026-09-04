# Monitor de preço Polymarket → Telegram

Roda de graça no GitHub Actions, sem servidor, sem programar.
Já vem configurado com os 3 mercados: Lula (vencer), Flávio (2º lugar),
Renan Santos (3º lugar).

## Passo a passo completo no GitHub

### 1. Crie o bot no Telegram
- Abra o Telegram, procure @BotFather, mande `/newbot`, escolha um nome.
- Guarde o TOKEN que ele te der (formato `123456789:AAExxxxxxx`).
- Mande qualquer mensagem para o bot recém-criado (ex: "oi").
- No navegador, abra: `https://api.telegram.org/bot<SEU_TOKEN>/getUpdates`
  (trocando `<SEU_TOKEN>` pelo token). Procure `"chat":{"id":` — o número
  ali é o seu CHAT_ID.

### 2. Crie uma conta no GitHub
- Vá em github.com → Sign up (se ainda não tiver conta). É grátis.

### 3. Crie um repositório novo
- Clique no `+` no canto superior direito → "New repository".
- Dê um nome, ex: `polymarket-monitor`.
- Marque como **Public** (assim os minutos do GitHub Actions são
  ilimitados e gratuitos).
- Clique em "Create repository".

### 4. Suba os arquivos
- Na página do repositório recém-criado, clique em "uploading an
  existing file" (ou "Add file" → "Upload files").
- No seu computador, extraia o zip que te mandei.
- Arraste a pasta inteira (o conteúdo dela: monitor.py, markets.json,
  state.json, README.md e a pasta .github) para a área de upload do
  GitHub. Ele mantém a estrutura de pastas automaticamente.
- Role para baixo e clique em "Commit changes".
- Confirme depois que a pasta `.github/workflows/monitor.yml` apareceu
  no repositório (clique nela pra abrir e checar).

### 5. Cadastre os secrets (dados sensíveis)
- No repositório, vá em **Settings** (aba no topo) → no menu lateral
  esquerdo, **Secrets and variables** → **Actions**.
- Clique em "New repository secret".
  - Nome: `TELEGRAM_TOKEN` — Valor: o token do passo 1.
  - Clique em "Add secret".
- Repita para:
  - Nome: `TELEGRAM_CHAT_ID` — Valor: o chat id do passo 1.

### 6. Ative e teste
- Vá na aba **Actions** (topo do repositório).
- Se aparecer um aviso pra habilitar Actions, clique para habilitar.
- Clique no workflow "Monitor Polymarket" na lista à esquerda.
- Clique em "Run workflow" (botão à direita) → "Run workflow" de novo
  para confirmar.
- Espere uns 10-20 segundos e atualize a página. Clique na execução
  para ver o log — deve mostrar os 3 mercados com "preco inicial
  registrado" (primeira vez não manda alerta, só grava o preço base).

### 7. Pronto
- A partir daí ele roda sozinho a cada 5 minutos.
- Quando qualquer um dos 3 mercados variar 1 ponto percentual ou mais
  desde o último preço registrado, você recebe uma mensagem no
  Telegram.

## Ajustar depois

- **Mudar o threshold**: edite `markets.json` direto pelo site do
  GitHub (ícone de lápis no arquivo) e mude o valor de `threshold_pct`.
- **Adicionar mais mercados**: copie um bloco `{...}` dentro do
  `markets.json`, ajuste `event_slug` (parte da URL do Polymarket
  depois de `/event/`) e `market_slug` (parte seguinte da URL).
- **Mudar a frequência**: edite `.github/workflows/monitor.yml`, linha
  `cron: "*/5 * * * *"` — troque o `5` por outro número de minutos.
