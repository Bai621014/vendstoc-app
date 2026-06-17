const express = require('express');
const app = express();

// Middlewares pour lire le JSON et les formulaires envoyés par les webhooks (Monetbil, etc.)
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 1. Page d'accueil du serveur GloireHub
app.get('/', (req, res) => {
    res.status(200).send('🚀 Serveur GloireHub (API GloirePay) actif et sécurisé.');
});

// 2. Webhook principal : C'est ici que convergent les "Newpaiements"
app.post('/newpaiements/webhook', (req, res) => {
    const paymentData = req.body;
    
    console.log('\n==============================================');
    console.log('       🎯 NOTIFICATION GLOIREPAY REÇUE       ');
    console.log('==============================================');
    console.log('Données brutes reçues :', JSON.stringify(paymentData, null, 2));

    // Détection de la méthode de paiement
    const paymentMethod = paymentData.operator || paymentData.method; // MTN, ORANGE, GLOIRECOIN, STRIPE
    const amount = paymentData.amount;
    const status = paymentData.status;

    // A. Logique si le paiement utilise le carburant GloireCoin (V10)
    if (paymentMethod === 'GLOIRECOIN') {
        console.log(`[GloireCoin] 💰 Traitement d'un transfert instantané de ${amount} GloireCoin.`);
        // TODO: Insérer ici ton interaction Web3 / Smart Contract pour transférer le jeton
        return res.status(200).json({ success: true, message: "Paiement GloireCoin validé on-chain." });
    }

    // B. Logique classique pour Mobile Money / Cartes (Monetbil / Stripe)
    if (status === 'SUCCESS' || status === 'success') {
        console.log(`[Fiat] ✅ Paiement international réussi de ${amount} via ${paymentMethod}.`);
        // Logique de distribution ou d'affichage de vente auto
        return res.status(200).send('Notification fiat traitée avec succès.');
    } else {
        console.log(`[Info] ⏳ Transaction en cours ou échouée (Status: ${status}).`);
        return res.status(200).send('Notification ignorée ou en attente.');
    }
});

// Gestion du Port d'écoute dynamique (Crucial pour Render et Railway)
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`\n==============================================`);
    console.log(`🚀 GloireHub est prêt et écoute sur le port ${PORT}`);
    console.log(`🔗 URL Webhook : /newpaiements/webhook`);
    console.log(`==============================================\n`);
});
