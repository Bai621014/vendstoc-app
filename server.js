require('dotenv').config();
const express = require('express');
const app = express();

// Middleware pour lire les données envoyées par Monetbil (format URL-encoded ou JSON)
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Route principale pour vérifier que le serveur tourne
app.get('/', (req, res) => {
    res.send('🚀 Serveur GloireHub en ligne. Traçabilité Web3 active.');
});

// ROUTE DE TRAÇABILITÉ (WEBHOOK)
app.post('/api/monetbil-webhook', (req, res) => {
    const txData = req.body;

    console.log(`\n=== 📥 NOUVELLE TRANSACTION REÇUE [${new Date().toISOString()}] ===`);
    
    // 1. Récupération de la clé secrète configurée sur Railway
    const secretKey = process.env.MONETBIL_SECRET_KEY;
    if (!secretKey) {
        console.error("[ERREUR CRITIQUE] La variable MONETBIL_SECRET_KEY n'est pas définie sur Railway !");
        return res.status(500).send("Erreur de configuration serveur");
    }

    // 2. Extraction et affichage des données pour la traçabilité
    // Monetbil envoie généralement : txid, payment_id, status, amount, currency, phone...
    const transactionId = txData.txid || txData.payment_id || 'ID_INCONNU';
    const status = txData.status ? txData.status.toUpperCase() : 'INCONNU';
    const amount = txData.amount || '0';
    const currency = txData.currency || 'XAF';
    const userPhone = txData.phone || 'Non spécifié';

    console.log(`🆔 ID Transaction : ${transactionId}`);
    console.log(`💰 Montant        : ${amount} ${currency}`);
    console.log(`📱 Client         : ${userPhone}`);
    console.log(`📊 Statut Actuel  : ${status}`);

    // 3. Logique de validation de la traçabilité
    if (status === 'SUCCESS') {
        console.log(`✅ [SUCCÈS] Le paiement a été complété avec succès !`);
        console.log(`🔗 [Web3 Sync] Prêt pour enregistrement sécurisé ou exécution de contrat intelligent.`);
        // C'est ici que vous pourrez ajouter la connexion à Supabase plus tard :
        // await supabase.from('transactions').insert([{ id: transactionId, status: 'success' }]);
    } else if (status === 'FAILED') {
        console.log(`❌ [ÉCHEC] La transaction a échoué ou a été annulée par l'utilisateur.`);
    } else {
        console.log(`⏳ [ATTENTE] La transaction est en cours de traitement (Statut : ${status}).`);
    }

    console.log(`========================================================\n`);

    // IMPORTANT : Toujours répondre "OK" à Monetbil pour lui dire que vous avez reçu l'information
    res.status(200).send("OK");
});

// Gestion du port pour Railway
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`\n========================================================`);
    console.log(`🚀 GloireHub est prêt et écoute sur le port ${PORT}`);
    console.log(`📍 Route Webhook disponible : /api/monetbil-webhook`);
    console.log(`========================================================\n`);
});
