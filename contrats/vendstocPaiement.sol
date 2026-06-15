// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title VendstocPaiement
 * @dev Système de paiement autonome et instantané avec prélèvement automatique de commission.
 */
contract VendstocPaiement {
    address payable public admin;

    // Événement déclenché à chaque paiement réussi pour informer l'application mobile/web
    event PaymentShared(
        address indexed acheteur,
        address indexed vendeur,
        uint256 montantTotal,
        uint256 commission,
        uint256 partVendeur
    );

    constructor() {
        // Le portefeuille qui déploie le contrat devient l'administrateur (reçoit les commissions)
        admin = payable(msg.sender);
    }

    /**
     * @dev Gère le paiement d'un article et sépare automatiquement les fonds.
     * @param _vendeur L'adresse du portefeuille crypto du vendeur.
     * @param _commissionPct Le pourcentage de commission prélevé par l'application (ex: 4).
     */
    function payerArticle(address payable _vendeur, uint256 _commissionPct) public payable {
        require(msg.value > 0, "Le montant doit etre superieur a 0");
        require(_vendeur != address(0), "Adresse du vendeur invalide");
        require(_commissionPct <= 100, "Le pourcentage de commission est invalide");

        // 1. Calcul de la commission et de la part du vendeur
        uint256 montantCommission = (msg.value * _commissionPct) / 100;
        uint256 montantVendeur = msg.value - montantCommission;

        // 2. Distribution automatique, sécurisée et instantanée
        if (montantCommission > 0) {
            admin.transfer(montantCommission); // Envoi des % à l'admin
        }
        _vendeur.transfer(montantVendeur); // Envoi du reste au vendeur

        // 3. Émission de l'événement pour le suivi dans l'interface de l'App
        emit PaymentShared(msg.sender, _vendeur, msg.value, montantCommission, montantVendeur);
    }

    /**
     * @dev Permet de modifier l'adresse de l'administrateur si vous changez de portefeuille principal.
     * @param _nouvelAdmin La nouvelle adresse qui encaissera les commissions.
     */
    function changerAdmin(address payable _nouvelAdmin) public {
        require(msg.sender == admin, "Seul l'admin actuel peut effectuer cette action");
        require(_nouvelAdmin != address(0), "Nouvelle adresse invalide");
        admin = _nouvelAdmin;
    }
}
