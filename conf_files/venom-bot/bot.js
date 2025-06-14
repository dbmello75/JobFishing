const venom = require('venom-bot');
const express = require('express');
const app = express();
const port = 3000;

let client = null;

app.use(express.json());

// Endpoint para envio de mensagens
app.post('/send-message', async (req, res) => {
  const { to, message } = req.body;
  if (!to || !message) {
    return res.status(400).json({ error: 'Parâmetros "to" e "message" são obrigatórios' });
  }

  try {
    await client.sendText(to, message);
    return res.status(200).json({ status: 'Mensagem enviada com sucesso' });
  } catch (err) {
    console.error('Erro ao enviar mensagem:', err);
    return res.status(500).json({ error: 'Erro ao enviar mensagem' });
  }
});

venom
  .create({ headless: true })
  .then((_client) => {
    client = _client;
    console.log('✅ Venom conectado com sucesso');

    // Inicia servidor web após a conexão
    app.listen(port, () => {
      console.log(`🚀 API disponível em http://localhost:${port}`);
    });
  })
  .catch((error) => {
    console.error('❌ Erro ao iniciar o bot:', error);
  });
