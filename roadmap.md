## ✅ Base Atual (V0.05)
- [x] Criação de anúncio (título, descrição, telefone, validade)
- [x] Geração de link encurtado
- [x] Redirecionamento funcional
- [x] Formulário com pré-visualização, confirmação e botão de copiar link

---

## 🔹 V0.06 – Aprimoramento UX e Dados
- [x] Adicionar campo “Localização” ou “Região”
- [ ] Botão “Criar novo anúncio” após sucesso
- [x] Mensagem de sucesso mais amigável
- [x] Início da padronização visual com CSS global

---

## 🔹 V0.07 – Monitoramento e Notificações
- [x] Armazenar logs de acessos e cliques
- [ ] API de relatório de desempenho
- [ ] Notificação por WhatsApp após criação do anúncio
- [ ] Implementar endpoint `/cancel-ad` via token

---

## 🔹 V0.08 – Publicidade de Serviços (Ads)
- [ ] Formulário separado para prestadores de serviço
- [ ] Sistema de pacotes (quantidade ou tempo)
- [ ] Envio automático para grupos WhatsApp
- [ ] Relatório diário de cliques

---

## 🔹 V0.09 – Integração com Pagamentos (Square App)
- [ ] Redirecionamento para checkout do Square App
- [ ] Webhook para validar pagamento
- [ ] Suporte a planos pagos (avulso, pacote, assinatura)

---

## 🔹 V0.10 – Integração com Grupos de WhatsApp

- [x] Tabelas para estados, regiões, categorias e grupos (normalizadas)
- [x] Cadastro manual de grupos com links curtos rastreáveis
- [ ] Página `grupos.html` com listagem dinâmica por região/categoria
- [ ] Endpoint `GET /g/{short_id}` com redirecionamento e contagem de cliques
- [ ] API para consulta dos grupos disponíveis (por frontend)
- [ ] Relatório de acessos aos grupos
- [ ] Controle de ativação/desativação de regiões e grupos


---

## 🔹 V1.0 – Painel do Usuário
- [ ] Login opcional por link mágico (sem senha)
- [ ] Listagem dos anúncios criados com status
- [ ] Histórico de relatórios e pagamentos
