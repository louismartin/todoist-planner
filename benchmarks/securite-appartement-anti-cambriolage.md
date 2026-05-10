# Benchmark: Securite appartement — Marseille 13006

**Date**: 10 mai 2026
**Statut**: Recherche terminee, plan d'action a executer
**Adresse**: 15 rue Marengo, 13006 Marseille

---

## Les 3 menaces et ce qui marche contre chacune

| Menace | Porte blindee | Alarme + sirene | Brouillard | Visiophone + entrebailleur | Protections crypto |
|---|---|---|---|---|---|
| **Cambriolage absent** | **Excellent** (4/5 entrent par la porte) | Bon (dissuasion + alerte) | Tres bon (intrus aveugle) | Sans objet | Sans objet |
| **Cambriolage nuit** | **Excellent** (passif, tu dors) | Bon (te reveille + alerte) | Bon si bouton panique | Sans objet | Sans objet |
| **Home jacking crypto** | **Inutile** (tu ouvres toi-meme) | Moyen (bouton panique, mais delai police 15-30 min) | Moyen (si tu atteins le bouton) | **Bon** (ne pas ouvrir) | **Seule vraie protection** |

**Constat** : pour le scenario home jacking crypto, aucune solution physique ne suffit seule. Meme avec porte blindee + alarme + brouillard, si quelqu'un te menace d'un pistolet, tu fais le virement. La seule protection qui marche sous contrainte armee = rendre le virement techniquement impossible.

---

## Hierarchie des investissements — par priorite

| Priorite | Solution | Cout | Temps setup | Protege contre |
|---|---|---|---|---|
| **1** | **Withdrawal lock** sur exchanges | 0 EUR | 5 min | Virement force instantane |
| **2** | **Passphrase hidden wallet** (Ledger/Trezor) + wallet leurre | 0 EUR (si hardware wallet existant) | 30 min | Wrench attack, inspection forcee |
| **3** | **OpSec** — ne jamais parler crypto publiquement | 0 EUR | Continu | Ciblage (le + efficace statistiquement) |
| **4** | **Whitelist adresses retrait** sur exchanges | 0 EUR | 5 min/exchange | Nouveau beneficiaire non autorise |
| **5** | **Visiophone + entrebailleur blinde** | 50-300 EUR | 1h | Home jacking (ne pas ouvrir) |
| **6** | **Alarme sans abonnement** (Ajax ou Somfy) | 300-700 EUR, 0 EUR/an | 2h | Cambriolage absent + nuit |
| **7** | **Porte blindee A2P BP1** | 2 500-4 000 EUR, 0 EUR/an | 1 jour (pose) | Cambriolage absent + nuit |
| **8** | **Multisig 2-of-3** (Nunchuk/Casa) | 150-350 EUR | 2-4h | Signature forcee (impossible seul) |
| **9** | **Telesurveillance** (Verisure/Sector) | 100-300 EUR + 35-50 EUR/mois | Pro | Tout sauf home jacking direct |
| **10** | **Brouillard** | 800-2 000 EUR + maintenance | Pro | Cambriolage (surdimensionne pour appart) |

---

## Phase 1 — Immediat (0 EUR, 30 min)

### 1.1 Binance Withdraw Protection

Gele tes retraits pour 1 a 7 jours. Meme avec ton mot de passe + 2FA + appareil, personne ne peut sortir de fonds. Tu peux continuer a trader.

**Setup:**
1. App Binance (v3.14.0+) ou web
2. Profil → Account → Security → Advanced Security → **Withdraw Protection**
3. Choisir la duree (recommande: 7 jours)
4. Activer **strict lockdown** → deverrouillage anticipe impossible
5. Confirmer

### 1.2 Kraken Global Settings Lock (GSL)

Tout changement de parametre (dont adresses de retrait) necessite 72h de delai + notification email.

**Setup:**
1. Kraken → Security Settings → **Global Settings Lock**
2. Activer

### 1.3 Coinbase Vault

Delai 48h avant tout retrait, avec confirmation email.

**Setup:**
1. Dashboard Coinbase → "Vault"
2. Creer un vault
3. Deplacer les fonds dans le vault

### 1.4 Whitelist d'adresses de retrait

Sur TOUS les exchanges: activer la whitelist. Tout retrait vers une adresse non whitelistee declenche un delai + confirmation.

### 1.5 Desactiver SMS 2FA partout

Passer sur TOTP (Google Authenticator, Ente Auth) ou YubiKey. Le SMS est vulnerable au SIM swap.

---

## Phase 2 — Court terme (0-200 EUR, 2-3h)

### 2.1 Passphrase / Hidden wallet sur Ledger

Le "25eme mot" BIP-39 cree un wallet entierement separe. Sans la passphrase, les fonds caches sont cryptographiquement invisibles.

**Strategie anti-wrench:**
- **PIN 1 → wallet decoy** : quelques centaines d'euros, transactions regulieres pour paraitre reel
- **PIN 2 → vrai wallet** : 95%+ des fonds

**Setup Ledger:**
1. Ledger Live → Settings → Security → Passphrase
2. Choisir "Attach to PIN"
3. Choisir un PIN different du PIN principal
4. Entrer la passphrase a associer
5. Confirmer
6. Envoyer quelques centaines d'euros sur le wallet decoy (PIN 1)
7. Deplacer le gros des fonds sur le wallet cache (PIN 2)

**Setup Trezor:**
1. Trezor Suite → Settings → Device → Passphrase → Enable
2. Passphrase vide → wallet standard (decoy)
3. Passphrase choisie → vrai wallet cache
4. **Attention**: Trezor affiche "+ Passphrase Wallet" dans le dropdown — un connaisseur peut suspecter un wallet cache. Ledger est plus discret.

### 2.2 Script de deni plausible

Preparer mentalement: *"Mon portefeuille principal est chez mon notaire, je n'y ai pas acces seul, ca prend 72h."* Couple au wallet leurre.

### 2.3 Code duress familial

Les clonages vocaux par IA sont courants (faux enlevement par telephone). Etablir un mot de code secret avec Amandine et la famille pour authentifier les appels.

---

## Phase 3 — Moyen terme (350-1 000 EUR)

### 3.1 Visiophone + entrebailleur blinde

**Visiophone**: voir qui sonne avant d'ouvrir. 50-300 EUR.
**Entrebailleur blinde**: ouvrir partiellement sans risque. 15-80 EUR.
**Regle**: ne JAMAIS ouvrir a quelqu'un d'inconnu sans verifier.

### 3.2 Alarme sans abonnement

**Ajax Systems (recommande)**
| Pack | Contenu | Prix |
|---|---|---|
| StarterKit | Hub 4G + detecteur mouvement + detecteur ouverture + telecommande | ~300 EUR |
| Pack appartement | Hub + capteurs multiples + sirene | ~500 EUR |
| Pack complet + MotionCam | Hub + capteurs + sirenes + camera | ~1 300 EUR |

- **IMPORTANT**: prendre le Hub 2 **4G** (pas 2G) — le reseau 2G s'arrete en France fin 2026
- Chiffrement militaire, detection brouillage radio, batterie secours 16h
- Aucun abonnement, portee 2 000m, autonomie capteurs 7 ans
- App smartphone, notifications push

**Somfy Home Alarm Advanced (alternative)**
| Pack | Prix |
|---|---|
| Standard | ~693 EUR |
| Integral | ~749 EUR |
| Video Plus | ~1 319 EUR |

- IntelliTAG: detecte les vibrations d'effraction AVANT l'ouverture de la porte
- GSM de secours gratuit 5 ans
- Telesurveillance optionnelle 9,99 EUR/mois
- Garantie 5 ans

**Verdict**: Ajax = meilleur rapport Q/P, plus flexible, sans abonnement. Somfy = plus cle en main.

### 3.3 Mode nuit — comment ca marche

1. Tu armes l'alarme en mode nuit (capteurs portes/fenetres actifs, detecteurs mouvement interieurs desactives)
2. Si quelqu'un force la porte → alarme immediate
3. Si toi tu ouvres la porte (poubelles, etc.) → pre-alarme bip-bip pendant 30-90 sec
4. Tu tapes ton code → alarme desarmee, pas de sirene
5. Si pas de code dans le delai → sirene a fond + notification smartphone

**Capteur a vibration (IntelliTAG / Ajax DoorProtect Plus)**: bonus, detecte le forcage AVANT l'ouverture. En mode nuit, peut etre configure pour n'alerter que sur vibrations de forcage, pas sur ouverture normale. ~30-50 EUR.

---

## Phase 4 — Si budget dispo (2 500-4 000 EUR)

### 4.1 Porte blindee A2P BP1

Reste un bon investissement long terme: 4 cambriolages sur 5 entrent par la porte. 80% des cambrioleurs abandonnent apres 5 min.

**Modeles:**

| Critere | Fichet Foxeo S | Tordjman BP1 | Bricard Centaure | Heracles MELISSA | Picard Diamant 10 |
|---|---|---|---|---|---|
| Certification | BP1 / EN 1627 cl.3 | BP1 a BP3 | BP1 (niv. 4 NF) | BP1 | BP1 |
| Points fermeture | 5 | 3 a 7 au choix | 6 + 6 anti-degondage | 5 | NC |
| Acoustique | 36 dB | 35 dB | **43 dB** | 38 dB | 40-42 dB |
| Thermique | 2.2 W/m2.K | NC | 2.1 | NC | **1.3** |
| Garantie porte | 10 ans | 10 ans | NC | 10 ans | NC |
| Fabrication | France | France | France (groupe US) | France | France |
| Prix reel (forums) | ~4 100 EUR | ~3 500 EUR | ~2 450 EUR | ~3 000 EUR | NC (haut) |

**Note Fichet**: la **Protecdoor+** (en dessous de la Foxeo S) a une meilleure isolation acoustique (40 dB vs 36 dB) pour un prix inferieur.

**Installateurs Marseille:**

| | **Devauze** (RECOMMANDE) | **GILLY** (ALTERNATIVE) |
|---|---|---|
| Adresse | 246 Rue Paradis, 13006 | 38 Bd Barral, 13008 |
| Google | **4.9/5** (285 avis) | Peu d'avis, tous positifs |
| Depuis | 1972 | 1985 |
| Prix | Des 1 895 EUR | Devis obligatoire |
| Fabrication | 48h | NC |
| Financement 0% | **Oui** (jusqu'au 31/07/2026) | A demander |
| Red flags | 1 incident isole | 0 |

**A eviter**: Mr Surete (incident qualite documente), Cle & Go (depannage, pas porte blindee), KparK, Huit Clos.

### 4.2 Multisig 2-of-3 (si holdings significatifs)

Pour signer une transaction, il faut 2 cles sur 3. Une chez toi, une chez un proche/coffre, une en backup. Meme sous contrainte physique totale, l'attaquant ne peut pas vider ton wallet seul.

**Setup Nunchuk:**
1. Installer Nunchuk (iOS, Android, desktop)
2. 2 hardware wallets (ex: Ledger + Trezor)
3. Nunchuk → "+" → Custom Wallet → 2-of-3
4. Ajouter les 3 cles
5. Stocker dans 3 lieux differents
6. Exporter et sauvegarder le fichier BSMS

**Cout**: 150-350 EUR (2 hardware wallets) + Nunchuk gratuit
**Limite**: plus complexe au quotidien, necessite bonne gestion des backups

---

## Phase 5 — Probablement pas necessaire

### Telesurveillance (35-50 EUR/mois)

Canal police prioritaire, levee de doute video, intervention 24h/24. Pertinent si tu voyages tres souvent. Cout sur 5 ans: 2 100-3 600 EUR. Verisure, Sector Alarm, Nexecur.

### Brouillard anti-intrusion

Ca marche (visibilite < 20cm en 3 sec) mais **surdimensionne pour un appart**:
- 98% des declenchements = fausses alertes
- Residus: "sale poussiere fine partout", "odeur qui impregne les murs pendant plusieurs jours" (forums)
- Peut declencher les detecteurs incendie → pompiers → voisins → syndic
- Un installateur pro honnete: *"Je ne conseille pas ce genre de materiel chez un particulier. Mieux vaut une deuxieme sirene."*
- 800-2 000 EUR + maintenance

---

## Points a ne pas oublier

### Assurance habitation
- Declarer toute installation de securite a l'assureur → reduction prime -5 a -20%
- Certification A2P souvent exigee pour l'indemnisation vol
- Verifier que la **cave et le parking** sont couverts (souvent en option)
- **Documenter tes biens MAINTENANT**: photos, numeros de serie, factures — pas apres le cambriolage
- Prejudice moyen d'un cambriolage: ~6 500 EUR. Indemnisation moyenne: ~1 800 EUR. Le delta est enorme.

### Copropriete
- Face exterieure de la porte = partie commune. Modification visible = vote en AG (majorite absolue art. 25)
- Contacter le syndic AVANT tout devis
- Si aspect exterieur identique = pas d'autorisation necessaire dans la plupart des cas

### Cave et parking
- Garantie vol en cave/parking rarement automatique — verifier le contrat
- Objets de valeur en cave = quasi jamais couverts
- Velos et trottinettes = tres cibles

### Digicode immeuble
- Fausse securite: +3 000 personnes/an peuvent connaitre le code d'un grand immeuble
- Un digicode seul sans interphone = pas de controle reel
- Proposer en AG (majorite simple art. 24) un visiophone si pas deja installe

### Etage et vulnerabilites
- RDC et 1er-2e etage: fenetres et balcons accessibles
- Au-dela du 3e-4e: la porte d'entree devient le seul point d'effraction
- 39.8% des cambriolages en 2024 ont eu lieu avec quelqu'un a l'interieur
- Temps moyen avant abandon: 5 minutes

### Statistiques France (2024)
- 218 200 cambriolages/an (1 toutes les 2h25)
- Taux d'elucidation: **7%** seulement
- Alarme reduit le risque de 47%
- Alarme + porte blindee + digicode: risque reduit de 85%
- Wrench attacks crypto: +75% en 2025, une attaque tous les 2.5 jours en France

---

## Top 10 des pieges a eviter

1. **"Porte blindee" sans certification A2P** — Le terme n'est pas protege. Sans A2P, certaines cedent en 9 secondes.

2. **Serrure A2P sur porte non certifiee** — L'ensemble doit etre certifie (porte + bati + serrure), pas juste la serrure.

3. **Oublier la copro** — Modification visible = vote en AG. Sans autorisation = demontage a ses frais.

4. **Negliger le bati/encadrement** — Si le mur est de mauvaise qualite, la porte ne sert a rien. Cas documente: porte 3 points arrachee de son encadrement.

5. **Dimensions hors standard** — Immeuble ancien (220-240 cm hauteur) = sur-mesure = +30 a 60% de surcout. Mesurer avant tout devis.

6. **Alarme Ajax Hub 2G** — Le reseau 2G s'arrete fin 2026 en France. Prendre le Hub 2 4G.

7. **SMS 2FA sur les exchanges crypto** — Vulnerable au SIM swap. Passer sur TOTP ou YubiKey.

8. **Pas de SAV local pour la porte blindee** — Serrure multipoints bloquee = 300-450 EUR d'urgence minimum.

9. **Securiser la porte en oubliant les fenetres** — Les cambrioleurs prennent l'entree la plus facile.

10. **Parler de ses crypto publiquement** — Les attaquants ciblent via OSINT. Si personne ne sait, personne ne vient.

---

## Checklist avant devis porte blindee (si phase 4)

### Mesurer (3x chaque)
- [ ] Hauteur embrasure (gauche, centre, droite — garder la + petite)
- [ ] Largeur embrasure (haut, milieu, bas — garder la + petite)
- [ ] Epaisseur du mur
- [ ] Sens d'ouverture (vu depuis le palier)

### Photographier
- [ ] Porte depuis le palier + depuis l'interieur
- [ ] Dormant (4 cotes), seuil, serrure, chant de la porte
- [ ] Murs adjacents (materiau)
- [ ] **Portes des voisins** (pour l'habillage copro)

### Verifier
- [ ] Materiau du mur (beton/pierre/brique)
- [ ] Solidite du dormant (appuyer dessus)
- [ ] Type de cylindre (europeen = cle plate avec encoches laterales)

### Copropriete
- [ ] Recuperer le reglement de copro
- [ ] Contacter le syndic: vote AG necessaire? Contraintes esthetiques?
- [ ] Obtenir un accord ecrit

### Questions a poser a l'installateur
1. Pose garantie decennale?
2. Certification A2P valide avec votre pose?
3. Bati remplace ou pose en renovation? (renovation = -30 mm largeur)
4. Inclus: depose, evacuation, finitions, rebouchage?
5. Delai fabrication pour mes dimensions?
6. Contrat de maintenance?
7. Financement 0%?

---

## Sources

### Crypto security
- [Binance Withdraw Protection — Coindesk](https://www.coindesk.com/business/2026/05/04/binance-is-launching-a-withdrawal-lock-to-help-deter-crypto-wrench-attacks)
- [How to Set Up Withdraw Protection — Binance](https://www.binance.com/en/support/faq/detail/95d6de0bc082498c9196e08846c522a4)
- [Kraken — Prevent unwanted withdrawals](https://support.kraken.com/articles/13644055237908-how-to-prevent-unwanted-withdrawals)
- [Nunchuk Decoy Wallet](https://nunchuk.io/blog/decoy-wallet)
- [Duress Wallet Ledger/Trezor — Exmon Academy](https://academy.exmon.pro/5-wrench-attack-setup-a-duress-wallet-on-ledger-trezor)
- [Trezor Passphrase](https://blog.trezor.io/passphrase-the-ultimate-protection-for-your-accounts-3a311990925b)
- [Edge App Duress Mode](https://edge.app/blog/crypto-basics/duress-mode/)
- [Crypto OpSec — Edouard.ai](https://edouard.ai/blog/crypto-opsec-personal-security-complete-guide)
- [Nunchuk DIY Multisig — BlockDyor](https://blockdyor.com/diy-bitcoin-multisig-wallet-nunchuk/)
- [Wrench attacks surge — CertiK/The Block](https://www.theblock.co/post/400601/crypto-wrench-attacks-rise-victims-family-members-risk-certik)
- [David Balland Ledger kidnapping — TRM Labs](https://www.trmlabs.com/resources/blog/the-rise-of-wrench-attacks-and-crypto-related-violent-crime)

### Alarmes
- [Ajax Alarm 2026 Guide — Sipko Security](https://sipkosecurity.com/ajax-alarm-systems-the-2026-comprehensive-installation-ecosystem-guide/)
- [Ajax Review — AVForums](https://www.avforums.com/reviews/ajax-smart-home-alarm-system-review.17658/)
- [Somfy Home Alarm Advanced — Boutique Somfy](https://boutique.somfy.fr/pack-home-alarm-advanced-integral.html)
- [Somfy IntelliTAG](https://www.somfy.fr/produits/2401487/detecteur-de-vibration-et-d-ouverture-intellitag-pour-gamme-home-alarm-et-one)
- [Ajax vs Somfy — Securexpert](https://www.securexpert.fr/alarme-ajax-ou-somfy-avis-comparatif/)
- [Alarme efficacite statistique — Generali](https://www.generali.fr/actu/alarme-prevention-securite-cambriolages/)

### Brouillard
- [ForumConstruire — Alarme fumigene](https://www.forumconstruire.com/construire/topic-214315.php)
- [ForumConstruire — Alarme fumigene 2](https://www.forumconstruire.com/construire/topic-417288-alarme-fumigene-choisir.php)
- [SecurityInfoWatch — Security Fog Systems](https://www.securityinfowatch.com/alarms-monitoring/alarm-systems-intrusion-detection/article/10551724/current-thinking-on-security-fog-systems)

### Portes blindees
- [Forum Que Choisir — Acheter une porte blindee](https://forum.quechoisir.org/acheter-une-porte-blindee-t13942.html)
- [Forum Que Choisir — Fichet Spheris HiS acoustique](https://forum.quechoisir.org/porte-blindee-fichet-spheris-his-et-isolation-acoustique-t249015.html)
- [Forum Serrurerie — Tordjman vs Picard vs Fichet](https://forum.serrurerie.info/travaux-de-serrurerie/porte-blindee-a2p-bp3-tordjman-versus-picard-versus-fichet/)
- [Certification A2P | CNPP](https://a2p-certification.org/porte-blindee/)
- [Fichet Foxeo S](https://www.fichet-pointfort.com/fr/fr/products/porte-blindee/porte-appartement/foxeo-s)
- [Devauze — Point Fort Fichet Marseille](https://www.devauze.com/)
- [Devauze — Financement 0%](https://www.devauze.com/financement-a-taux-zero)
- [GILLY — Point Fort Fichet](https://www.gilly.pro/)

### Home jacking
- [Home jacking — MAIF](https://www.maif.fr/habitation/guide-assurance-habitation/home-jacking)
- [Home jacking — Sector Alarm](https://www.sectoralarm.fr/blog/posts/homejacking/)
- [Cambriolages France 2024/2025 — Daitem](https://daitem.com/fr/actualite/cambriolages-et-home-jacking-en-france-chiffres-cles-2024-2025)

### Assurance et statistiques
- [Reduction assurance alarme — Sectoralarm](https://www.sectoralarm.fr/blog/posts/reduction-assurance-habitation-si-alarme)
- [Porte blindee et assurance — Meilleurtaux](https://www.meilleurtaux.com/comparateur-assurance/assurance-habitation/assurance-habitation-pas-cher/porte-blindee-assurance-habitation.html)
- [Cout cambriolage France — Homiris](https://www.homiris.fr/fr/le-cout-d-un-cambriolage.html)
- [Cambriolages et assureurs — Hellosafe](https://hellosafe.fr/blog/analyse-cambriolages-france)
- [Cave et garage assurance — Index-habitation](https://www.index-habitation.fr/multirisque/garanties/vol/vol-cave-garage)
