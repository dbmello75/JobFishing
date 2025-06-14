# JobFishing

Plataforma para publicação de vagas de emprego e serviços, com envio automatizado para grupos de WhatsApp e rastreamento de cliques por link curto.

---

## 📁 Estrutura do Projeto

```
jobfishing/
├── backend/           # API FastAPI com SQLite e encurtador de links
│   ├── main.py
│   └── requirements.txt
├── frontend/          # HTML/JS do site com formulário e visualização de anúncio
│   ├── index.html
│   ├── anuncio.html
│   └── Makefile
├── .env.example       # Exemplo de variáveis de ambiente
├── .gitignore         # Exclusões padrão para Git
├── Makefile           # Makefile unificado de deploy e automações
├── roadmap.md         # Planejamento de versões e funcionalidades
└── README.md          # Este arquivo
```


📡 Arquitetura da Plataforma de Automação de Grupos WhatsApp

```

          ┌────────────────────────┐
          │        Frontend        │
          │ (HTML + JS estáticos) │
          └─────────┬──────────────┘
                    │
                    ▼
          ┌────────────────────────┐
          │       FastAPI          │◄────┐
          │ (Anúncios, Grupos API) │     │
          └─────────┬──────────────┘     │
                    │                    │
      (Webhook ou HTTP Request)          │
                    │                    │
                    ▼                    │
          ┌────────────────────────┐     │
          │         n8n            │─────┘
          │ (Automações, Lógica)  │
          └─────────┬──────────────┘
                    │
                    ▼
          ┌────────────────────────┐
          │      Venom Bot         │
          │ (WhatsApp Web Driver) │
          └─────────┬──────────────┘
                    │
                    ▼
          Grupos e usuários do WhatsApp


```

---

## 🚀 Deploy

Use os comandos abaixo para gerenciar o deploy no servidor:

```bash
make deploy-all     # Sincroniza backend e frontend com o servidor
make clearrestart        # Reinicia o serviço FastAPI via systemd
make logs           # Exibe os logs do serviço
```

---

## ⚙️ Variáveis de Ambiente

Crie um `.env` com base no `.env.example`:

```env
REDIRECT_DOMAIN=https://jobfishing.us
SHORTLINK_DOMAIN=https://jfsh.io
DATABASE_PATH=./ads.db
```

---

## 📌 Roadmap

Consulte o arquivo [`roadmap.md`](./roadmap.md) para ver a evolução do projeto e funcionalidades planejadas.

---

## 📞 Comunicação

Toda a comunicação com empregadores é feita exclusivamente via WhatsApp. O uso de e-mail não é necessário.
