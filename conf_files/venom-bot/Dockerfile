FROM node:20-alpine

# Diretório da aplicação
WORKDIR /usr/src/app

# Instala o venom-bot
RUN npm install venom-bot

# Cria script simples de envio
COPY bot.js .

# Expõe a porta (caso use webhooks/API)
EXPOSE 3000

# Comando padrão
CMD ["node", "bot.js"]
