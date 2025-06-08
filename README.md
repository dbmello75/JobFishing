# JobFishing
=======
# 🛠️ JobFishing Backend

Backend FastAPI para gerenciamento de **anúncios com links curtos rastreáveis**, integrado ao domínio `https://jfsh.io`. Ele redireciona os acessos para o site principal `https://jobfising.us` e controla validade e contagem de cliques dos anúncios.

---

## 🔗 Como Funciona

1. **Criação de Anúncio**

   * Endpoint `POST /create-ad`
   * Gera um link curto como:
     `https://jfsh.io/r/abc123`

2. **Redirecionamento**

   * Se o anúncio estiver ativo:
     Redireciona para `https://jobfising.us/anuncio/{uuid}`
   * Se expirado ou desativado:
     Mostra: *"Esta vaga foi preenchida ou expirou."*

3. **Desativação Manual**

   * Endpoint `POST /deactivate-ad/{short_id}`
     Desativa o anúncio antes da data de validade.

---

## 🚀 Como Subir no Servidor

### 1. Instalar dependências

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Arquivo `requirements.txt`

```txt
fastapi
uvicorn
```

---

## ⚙️ Deploy com Gunicorn + systemd

### Criar o serviço: `/etc/systemd/system/jobfishing.service`

```ini
[Unit]
Description=JobFishing FastAPI backend
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/jobfishing-backend
ExecStart=/var/www/jobfishing-backend/venv/bin/gunicorn -k uvicorn.workers.UvicornWorker app.main:app -b 127.0.0.1:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

### Ativar e iniciar:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now jobfishing
```

---

## 🌐 Apache Proxy (jfsh.io)

No `jfsh.io.conf`:

```apache
ProxyPass /r/ http://127.0.0.1:8000/r/
ProxyPassReverse /r/ http://127.0.0.1:8000/r/
```

---

## 📦 Estrutura do Projeto

```
jobfishing-backend/
├── app/
│   └── main.py           # App FastAPI com rotas e lógica de redirecionamento
├── requirements.txt      # Dependências do projeto
└── jobfishing.service    # Arquivo systemd para rodar o backend
```

---

## 👤 Autor

Desenvolvido por [@dbmello75](https://github.com/dbmello75)
Contato via [GitHub](https://github.com/dbmello75) ou canal do JobFishing.

