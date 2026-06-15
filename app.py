import os
import json
from flask import Flask, request, jsonify
from web3 import Web3
from dotenv import load_dotenv

# Chargement des variables d'environnement (Railway gère ça automatiquement)
load_dotenv()

app = Flask(__name__)

# ==========================================
# 1. CONFIGURATION DE LA BLOCKCHAIN (WEB3)
# ==========================================
RPC_URL = os.getenv("BLOCKCHAIN_RPC_URL", "https://rpc.ankr.com/eth_holesky")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
SERVER_PRIVATE_KEY = os.getenv("WALLET_PRIVATE_KEY")
SERVER_ADDRESS = os.getenv("SERVER_WALLET_ADDRESS") # Ton adresse publique de serveur

# Initialisation de la connexion Web3
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Vérification immédiate de la connexion de l'IA aux logs au démarrage
if w3.is_connected():
    print("🤖 [SYSTEM SYSTEM] Assistant connecté avec succès au nœud RPC Blockchain.")
else:
    print("⚠️ [SYSTEM WARNING] Échec initial de connexion au nœud RPC Blockchain. Vérifie tes variables.")

# ==========================================
# 2. CONFIGURATION DE L'ABI DU CONTRAT
# ==========================================
# Contient uniquement l'interface de ta fonction 'payerArticle' pour alléger la mémoire
ABI_JSON = """[
    {
        "inputs": [
            {"internalType": "address payable", "name": "_vendeur", "type": "address"},
            {"internalType": "uint256", "name": "_commissionPct", "type": "uint256"}
        ],
        "name": "payerArticle",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    }
]"""
contract = w3.eth.contract(address=w3.to_checksum_address(CONTRACT_ADDRESS), abi=json.loads(ABI_JSON))


# ==========================================
# 3. ROUTE WEBHOOK DE DÉTECTION AUTOMATIQUE
# ==========================================
@app.route('/webhook/monetbil', methods=['POST'])
def webhook_mobile_money():
    data = request.json  # Réception des données en arrière-plan envoyées par Monetbil
    
    # Extraction du statut du paiement Mobile Money
    status = data.get('status')
    
    if status in ['success', 'SUCCESS']:
        print("💰 [NOTIFICATION MONETBIL] Dépôt Mobile Money validé avec succès !")
        
        # Récupération dynamique des paramètres liés à l'achat envoyé par ton application
        adresse_vendeur = data.get('vendeur_crypto_address') 
        montant_eth = data.get('montant_crypto')  # Montant converti et dû en ETH/Crypto
        commission_pct = int(data.get('commission_pourcentage', 4))  # 4% par défaut si non spécifié
        
        try:
            print(f"🔄 [TRAITEMENT AUTOMATIQUE] Lancement du virement instantané vers le vendeur : {adresse_vendeur}")
            
            # Déclenchement autonome et instantané du contrat intelligent
            tx_hash = declencher_paiement_blockchain(adresse_vendeur, montant_eth, commission_pct)
            
            # Message de succès visible H24 dans ton tableau de bord Railway
            print(f"📢 [NOTIF GLOIREHUB] Succès ! Vendeur payé en crypto. Tx Hash: {tx_hash}")
            
            return jsonify({
                "status": "success", 
                "message": "Notification reçue, contrat intelligent exécuté au millième de seconde !", 
                "tx_hash": tx_hash
            }), 200
            
        except Exception as e:
            print(f"❌ [ERREUR CRITIQUE BLOCKCHAIN] Échec du traitement : {e}")
            return jsonify({
                "status": "error", 
                "message": "Erreur lors de l'exécution automatique du contrat intelligent",
                "details": str(e)
            }), 500
            
    else:
        print(f"⚠️ [TRAITEMENT REJETÉ] Événement ignoré. Statut reçu non valide : {status}")
        return jsonify({
            "status": "ignored", 
            "message": "Paiement non finalisé en Mobile Money, action annulée."
        }), 200


# ==========================================
# 4. ENGINE DE DISTRIBUTION CRYPTO AUTOMATIQUE
# ==========================================
def declencher_paiement_blockchain(vendeur, montant_eth, commission):
    # Conversion de la valeur humaine ETH en sous-unité Blockchain (Wei)
    montant_wei = w3.to_wei(montant_eth, 'ether')
    
    # Récupération sécurisée de l'index de transaction du portefeuille (Nonce)
    nonce = w3.eth.get_transaction_count(SERVER_ADDRESS)
    
    # Construction structurelle de l'appel vers ton contrat VendstocPaiement
    tx = contract.functions.payerArticle(
        w3.to_checksum_address(vendeur), 
        commission
    ).build_transaction({
        'from': SERVER_ADDRESS,
        'value': montant_wei,             # Total de la crypto injectée dans la machine de partage
        'gas': 120000,                    # Limite de gaz standard pour une exécution sécurisée
        'gasPrice': w3.eth.gas_price,     # Ajustement automatique aux frais réseau en temps réel
        'nonce': nonce,
    })
    
    # Signature électronique autonome via la clé privée de ton serveur
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=SERVER_PRIVATE_KEY)
    
    # Expédition brute et instantanée sur le réseau
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    
    return w3.to_hex(tx_hash)


# ==========================================
# 5. DÉMARRAGE DU SERVEUR AUTONOME
# ==========================================
if __name__ == '__main__':
    # Railway attribue son propre canal d'écoute dynamiquement via la variable d'environnement PORT
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 [STATUT LOG] Serveur GloireHub en mode écoute active H24 sur le port {port}...")
    app.run(host='0.0.0.0', port=port)
