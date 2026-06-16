// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title VendstocPaiement
 * @dev Système de paiement autonome, sécurisé avec gestion centralisée de la commission.
 */
contract VendstocPaiement {
    address payable public admin;
    uint256 public commissionPct; // Stocké de manière sécurisée sur la blockchain

    // Événements
    event PaymentShared(
        address indexed acheteur,
        address indexed vendeur,
        uint256 montantTotal,
        uint256 commission,
        uint256 partVendeur
    );
    event CommissionUpdated(uint256 nouveauPourcentage);
    event AdminChanged(address indexed ancienAdmin, address indexed nouvelAdmin);

    modifier onlyAdmin() {
        require(msg.sender == admin, "Seul l'admin peut effectuer cette action");
        _;
    }

    constructor() {
        admin = payable(msg.sender);
        commissionPct = 4; // Configuration de la commission par défaut (4%)
    }

    /**
     * @dev Gère le paiement d'un article et sépare automatiquement les fonds de manière sécurisée.
     * @param _vendeur L'adresse du portefeuille crypto du vendeur.
     */
    function payerArticle(address payable _vendeur) public payable {
        require(msg.value > 0, "Le montant doit etre superieur a 0");
        require(_vendeur != address(0), "Adresse du vendeur invalide");
        require(_vendeur != admin, "Le vendeur ne peut pas etre l'administrateur");

        // 1. Calcul des parts
        uint256 montantCommission = (msg.value * commissionPct) / 100;
        uint256 montantVendeur = msg.value - montantCommission;

        // 2. Distribution moderne et sécurisée via .call (anti-blocage de gas)
        if (montantCommission > 0) {
            (bool successAdmin, ) = admin.call{value: montantCommission}("");
            require(successAdmin, "Échec du transfert de la commission a l'admin");
        }

        (bool successVendeur, ) = _vendeur.call{value: montantVendeur}("");
        require(successVendeur, "Échec du transfert des fonds au vendeur");

        // 3. Suivi de l'événement pour l'App
        emit PaymentShared(msg.sender, _vendeur, msg.value, montantCommission, montantVendeur);
    }

    /**
     * @dev Permet à l'admin de modifier le taux de commission de la plateforme.
     * @param _nouveauPct Le nouveau pourcentage (ex: 5 pour 5%).
     */
    function modifierCommission(uint256 _nouveauPct) public onlyAdmin {
        require(_nouveauPct <= 20, "La commission ne peut pas depasser 20%"); // Sécurité pour les utilisateurs
        commissionPct = _nouveauPct;
        emit CommissionUpdated(_nouveauPct);
    }

    /**
     * @dev Modifie l'adresse de l'administrateur.
     * @param _nouvelAdmin La nouvelle adresse.
     */
    function changerAdmin(address payable _nouvelAdmin) public onlyAdmin {
        require(_nouvelAdmin != address(0), "Nouvelle adresse invalide");
        emit AdminChanged(admin, _nouvelAdmin);
        admin = _nouvelAdmin;
    }
}
