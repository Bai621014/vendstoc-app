import http.client  # ✅ CORRIGÉ : "import" en minuscules
import json
import os

def initialiser_application_2fa():
    # Récupération sécurisée de l'URL et de la clé API depuis l'environnement
    # Si non configurées, le script utilisera tes valeurs par défaut automatiquement
    INFOBIP_URL = os.environ.get("INFOBIP_URL", "jrwjyk.api.infobip.com")
    API_KEY = os.environ.get("INFOBIP_API_KEY", "7029a057fc5ed3ded598d069b3b9b94e-c689f015-967e-4e35-aa52-f1e4e2b3eed4")

    if not API_KEY:
        print("Erreur : La variable d'environnement INFOBIP_API_KEY est manquante.")
        return

    print(f"Connexion à l'API Infobip via : {INFOBIP_URL}...")
    conn = http.client.HTTPSConnection(INFOBIP_URL)

    # Configuration complète et stricte pour GloirePay
    payload = json.dumps({
        "name": "GloirePay 2FA Application",
        "enabled": True,
        "configuration": {
            "pinAttempts": 10,
            "allowMultiplePinVerifications": True,
            "pinTimeToLive": "15m",
            "verifyPinLimit": "1/3s",
            "sendPinPerApplicationLimit": "100/1d",
            "sendPinPerPhoneNumberLimit": "10/1d"
        }
    })

    headers = {
        'Authorization': f'App {API_KEY}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    try:
        # Envoi de la requête de création de l'application
        conn.request("POST", "/2fa/2/applications", payload, headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        
        print("\n--- RÉPONSE INFOBIP ---")
        print(data)
        print("-----------------------\n")
        print("Action requise : Copie l' 'applicationId' reçu dans la réponse ci-dessus.")
        
    except Exception as e:
        print(f"Une erreur est survenue lors de la requête : {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    initialiser_application_2fa()
