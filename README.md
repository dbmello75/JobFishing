# JobFishing Backend

Sistema de redirecionamento de links curtos com rastreamento e validade para anúncios de vagas, integrado ao domínio `https://jfsh.io`.

## 🔗 Exemplo de Fluxo

1. Criar um anúncio via API → gera um link curto como `https://jfsh.io/r/abc123`
2. Quando acessado:
   - Se ativo: redireciona para `https://jobfising.us/anuncio/{uuid}`
   - Se expirado ou desativado: mostra mensagem de "vaga preenchida"

---

## 🧱 Estrutura do Projeto

jobfishing-backend/
├── app/
│ ├── main.py
│ └── models.py (opcional)
├── requirements.txt
└── jobfishing.service (systemd)
