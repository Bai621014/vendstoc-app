# 🚀 GloirePay (GloireHub API & Webhook Service)

Système automatisé de traitement et de distribution de paiements instantanés à l'international. L'application (propulsée par le serveur **GloireHub**) intercepte les notifications Mobile Money, gère l'écosystème **GloireMedia** et prépare l'intégration du carburant **GloireCoin (V10)**.

## 🛠️ Fichiers de l'Écosystème
* `server.js` : Serveur backend Node.js / Express gérant l'API et les Webhooks.
* `paiement.html` : Interface d'initialisation des paiements.
* `index.html` : Vitrine de l'application.

## 📋 Route du Webhook à configurer
Une fois déployé sur Render, configure l'URL de notification dans ton espace développeur (Monetbil, etc.) :
👉 `https://ton-application.onrender.com/newpaiements/webhook`
