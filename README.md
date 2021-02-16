BOT do Telegram responsável por gerar relatórios gerenciais do sistema Industry Care

Configuração do Webhook

Hoster utilizado: Ngrok
Link de instalação: https://dashboard.ngrok.com/get-started/setup
Unzip to uninstall: unzip /path/to/ngrok.zip (ideal colocar na pasta raiz do software e adicioná-lo ao .gitignore)
Connect your account: ./ngrok authtoken 1oWJRTXONGJINIZGyAosh8omM5Q_5yUXjAb8SYxh7KPTQwCm9
Start a HTTP Tunnel: ./ngrok http 80 (ideal abrir em um terminal fora do editor de texto)
-------------------------------------- Exemplo de interface ngrok --------------------------------------

Web Interface http://127.0.0.1:4040
Forwarding http://9876115b8c2d.ngrok.io -> http://localhost:80 Forwarding https://9876115b8c2d.ngrok.io -> http://localhost:80

A URL https deverá ser adicionada em seu Allowed Hosts (settings) sempre que for atualizada.

-------------------------------------- Exemplo de Allowed Hosts --------------------------------------

ALLOWED_HOSTS = ['9876115b8c2d.ngrok.io']

Feito isto, agora é necessário setar o webhook junto a API do Telegram.

Em um navegador, digite:

https://api.telegram.org/{TOKEN}/setWebHook?url={URL WEBHOOK}/ Lembrando que a URL Webhook é a mesma gerada pelo ngrok e permitida em Settings. Portanto, sempre que iniciar um novo server ngrok, além de alterar em Allowed Hosts, deverá setar novamente.

-------------------------------------- Exemplo de Set Webhook --------------------------------------

https://api.telegram.org/bot1642202091:AAEUQIzu98bYbh0-AATR2UBzMDb8-VB5dgg/setWebHook?url=https://9876115b8c2d.ngrok.io/
