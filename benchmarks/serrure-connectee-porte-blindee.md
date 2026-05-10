# Benchmark : Serrure connectee pour porte blindee 5 points

**Date** : 10 mai 2026
**Besoin** : Ne plus avoir besoin de chercher ses cles / penser a les prendre. Porte blindee 5 points neuve (pas encore installee). Ne pas reduire la securite. Acces pour Amandine + invites occasionnels.
**Preferences d'ouverture** : code > empreinte > NFC smartphone > smartphone (BT/WiFi) >> badge > cles

---

## TL;DR — Recommandation

**Puisque la porte n'est pas encore installee**, la meilleure approche est de **commander la motorisation integree avec la porte blindee** (surcout estime 300-1000 EUR vs retrofit a ~360 EUR, mais moteur dimensionne, certification A2P coherente, installation pro incluse).

- **Tordjman** : meilleur rapport qualite/prix des integrees, double certification A2P *@ (mecanique + cyber), reseau solide en PACA. Devis a demander.
- **Picard Parade 2** : alternative solide, fabrication francaise, digicode + badges + app.
- **Fichet Kibolt S** : haut de gamme absolu (camera, 9 pts, alertes), mais prix eleve.

**Si retrofit quand meme** : Nuki Pro 5 + Keypad 2 (~360 EUR) ou SwitchBot Lock Ultra Touch (~250 EUR).

---

## Le defi specifique : porte blindee 5 points

C'est LE point critique. Un petit moteur a pile doit faire tourner un cylindre qui actionne 5 points de verrouillage simultanement.

### Prerequis non-negociable
- **Cylindre debrayable** : on peut ouvrir de l'exterieur meme si une cle est inseree a l'interieur. Sans ca, batterie morte ou moteur bloque = enferme dehors sans recours.

### Probleme du relevage de poignee
Sur beaucoup de portes multipoints, il faut lever la poignee avant de fermer. La serrure connectee ne peut pas faire ca seule — sauf le Tedee PRO (fonction pull-spring).

### Couple moteur
Seuil minimum 1.2 Nm, recommande 1.5 Nm. En dessous, le moteur "abdique" sur 5 points.

---

## 2 approches possibles

| | Motorisation integree (porte neuve) | Retrofit (ajoute apres) |
|---|---|---|
| **Principe** | Serrure motorisee commandee avec la porte | Moteur pose sur le cylindre existant |
| **Couple moteur** | Dimensionne pour la porte | Peut etre insuffisant |
| **Certification A2P** | Coherente sur l'ensemble | Casse la chaine A2P |
| **Installation** | Pro, incluse | DIY, a tester soi-meme |
| **Fiabilite multipoints** | Garantie par le fabricant | "Ca devrait marcher" |
| **Assurance** | Couverte | Potentiellement pas |
| **Prix** | 300-1000 EUR de surcout sur la porte | 250-480 EUR |

---

## Solutions integrees (recommandees pour porte neuve)

### 1. Tordjman — serrure connectee integree (RECOMMANDE)
- **Prix** : 2 700 – 4 800 EUR TTC (porte + option connectee)
- **Certification** : A2P *@ (double : mecanique + electronique) — seul fabricant avec cette double certif
- **Acces** : code, badges, smartphone (app)
- **Autonomie** : ~1 an
- **Points forts** : meilleur rapport qualite/prix des integrees, reseau PACA solide, disponible sur toutes leurs portes (3, 5 ou 7 points)
- **A verifier** : modes d'ouverture exacts (empreinte digitale dispo ?)

### 2. Picard Parade 2 — serrure motorisee 5 points
- **Prix** : 3 000 – 6 000 EUR TTC (porte + serrure), devis obligatoire
- **Certification** : A2P
- **Acces** : digicode, badges, app, telecommande. Options domotique (Z-Wave, io, EnOcean, Alexa, Google)
- **Autonomie** : 3 mois (batterie integree)
- **Points forts** : fabrication francaise, serrure nativement concue pour multipoints
- **Points faibles** : prix sur devis uniquement, autonomie faible (3 mois)

### 3. Fichet Kibolt S — haut de gamme absolu
- **Prix** : 4 000 – 6 000 EUR TTC (porte + option)
- **Certification** : A2P 1* + A2P @
- **Acces** : camera grand-angle, interphone, detecteur de mouvement, alertes smartphone, anti-squat, gestion d'acces a distance
- **Points** : 9 points
- **Points forts** : la solution la plus complete (camera + serrure + interphone), top securite
- **Points faibles** : prix tres eleve, ecosysteme Fichet ferme

---

## Solutions retrofit (si on prefere ajouter apres)

### 1. Nuki Smart Lock Pro 5 + Keypad 2 NFC — reference europeenne
- **Prix** : ~360 EUR (bundle serrure + keypad)
- **Acces** : empreinte (20 max), code PIN, NFC, app, Bluetooth, WiFi integre, auto-unlock GPS
- **Certification** : aucune A2P (le cylindre sous-jacent garde la sienne)
- **Autonomie** : ~6 mois (rechargeable)
- **Compatibilite multipoints** : oui avec moteur brushless Gen 5, mais a tester
- **Points forts** : meilleure app du marche, WiFi integre (pas de hub), Matter over Thread natif, Apple HomeKit
- **Points faibles** : 20 empreintes max, prix eleve en bundle, problemes moteur documentes sur Gen 3 (resolus Gen 5 ?)
- **Note experts** : reference unanime

### 2. SwitchBot Lock Ultra Touch Combo — meilleur rapport fonctionnalites/prix
- **Prix** : ~250 EUR (bundle complet avec hub)
- **Acces** : empreinte (100), code PIN, NFC, app, Bluetooth, WiFi (via hub inclus), 17 modes au total
- **Certification** : aucune
- **Autonomie** : ~9 mois (batterie rechargeable + batterie secours CR123A)
- **Compatibilite multipoints** : moteur puissant nouvelle generation, compatible selon fabricant
- **Points forts** : prix, nombre de modes d'acces, hub inclus, Matter
- **Points faibles** : marque chinoise, fiabilite long terme incertaine, adhesif 3M qui peut lacher
- **Note experts** : 9/10 Tom's Guide

### 3. Tedee GO2 + Keypad PRO — bon mais couple limite
- **Prix** : ~250-280 EUR (bundle GO2 + Bridge + Keypad PRO)
- **Acces** : empreinte (100), code PIN, app, Bluetooth
- **Certification** : aucune
- **Autonomie** : serrure quelques mois, keypad 12 mois
- **Compatibilite multipoints** : **couple trop faible pour 5 points** (confirme par plusieurs sources)
- **Points forts** : bon support francais, biometrie securisee (tokenisation), compact
- **Points faibles** : bridge WiFi separe, **risque sur multipoints**

### 4. Yale Linus L2 — seul certifie A2P en retrofit
- **Prix** : ~200-230 EUR
- **Acces** : app, code PIN, WiFi integre
- **Certification** : **A2P 1 etoile** (unique en retrofit)
- **Autonomie** : **15 mois** (record, piles AA)
- **Points forts** : certification A2P, WiFi integre sans hub, autonomie record
- **Points faibles** : empreinte pas toujours dispo selon version, couple moyen pour multipoints

---

## Problemes reels documentes (retours utilisateurs)

### Moteur bloque (Nuki 3.0 — le plus grave)
- Cas documentes d'utilisateurs qui ont du **couper la serrure de leur porte** pour rentrer (forum Nuki, mars 2023)
- Moteur qui tourne en continu et chauffe sans s'arreter
- Gen 5 (brushless) cense resoudre le probleme, mais firmware beta 5.5.x montre encore des soucis

### Batteries : autonomie reelle divisee par 2-3 sur multipoints
- Annonce 6-12 mois, realite 2-3 mois sur porte blindee 5 points
- Certains utilisateurs changent les piles tous les mois

### Bug auto-lock Nuki
- La serrure "croit" etre verrouillee alors qu'elle ne l'est pas — porte ouverte toute la journee

### SwitchBot : adhesif qui lache
- Adhesif 3M qui cede apres quelques mois, serrure retrouvee par terre

### Tedee GO : couple insuffisant sur multipoints
- Confirme par SmartHomePerfected et plusieurs utilisateurs

### Securite
- Pas de hack documente des marques premium (Nuki, Tedee, Yale) dans la vraie vie
- Risques theoriques : relay attack Bluetooth, brute force PIN, firmware exploit
- En pratique les cambrioleurs fracturent, ils ne hackent pas
- **Risque assurantiel** : effraction via hacking ne laisse aucune trace physique — assureur peut refuser indemnisation

---

## Certifications a connaitre

| Certification | Origine | Signification |
|---|---|---|
| **A2P 1-3 etoiles** | France (CNPP) | Resistance mecanique a l'effraction (5/10/15 min) |
| **A2P @** | France (CNPP + ANSSI) | Securite mecanique + cybersecurite |
| **SKG****** | Pays-Bas | Equivalent A2P 2-3 etoiles, reconnu en Europe |
| **AV-Test** | Allemagne | Certification cybersecurite independante |

**Regle critique** : le cylindre ET la serrure doivent etre au meme niveau A2P que la porte. Installer un cylindre non certifie sur une porte A2P = chaine cassee.

---

## Tableau recapitulatif final

| Solution | Type | Prix estime | Code | Empreinte | A2P | Autonomie | Multipoints 5 pts |
|---|---|---|---|---|---|---|---|
| **Tordjman connecte** | Integree | 2 700–4 800 EUR | Oui | A verifier | A2P *@ | ~1 an | Garanti |
| **Picard Parade 2** | Integree | 3 000–6 000 EUR | Oui | Non | A2P | 3 mois | Garanti |
| **Fichet Kibolt S** | Integree | 4 000–6 000 EUR | Oui | Non | A2P 1*+@ | N/A | Garanti (9 pts) |
| **Nuki Pro 5 + Keypad 2** | Retrofit | ~360 EUR | Oui | Oui (20) | Non | 6 mois | Compatible (tester) |
| **SwitchBot Ultra Touch** | Retrofit | ~250 EUR | Oui | Oui (100) | Non | 9 mois | Compatible (tester) |
| **Yale Linus L2** | Retrofit | ~200 EUR | Oui | Partiel | A2P 1* | 15 mois | Moyen |
| **Tedee GO2 + Keypad PRO** | Retrofit | ~260 EUR | Oui | Oui (100) | Non | ~3 mois | **Risque** |

---

## Prochaines etapes
1. Demander un devis Tordjman avec option serrure connectee (reseau PACA)
2. Demander un devis Picard Parade 2 pour comparer
3. Comparer le surcout de l'option connectee vs Nuki Pro 5 (~360 EUR)

---

## Sources principales
- [Tom's Guide FR — Meilleure serrure connectee](https://www.tomsguide.fr/serrure-connectee-comment-choisir-laquelle-acheter/)
- [Les Alexiens — Meilleures serrures connectees Matter 2025](https://www.lesalexiens.fr/actualites/meilleures-serrures-connectees-2025/)
- [Futura Sciences — Comparatif](https://www.futura-sciences.com/conso/comparatifs/meilleure-serrure-connectee-comparatif/)
- [A2P Certification — Serrure connectee et securite](https://a2p-certification.org/une-serrure-connectee-est-elle-une-serrure-de-securite/)
- [Forum Somfy — Serrure connectee porte blindee lourde](https://forum.somfy.fr/questions/3008623-serrure-connectee-porte-blindee-lourde)
- [Nuki Developers Forum — Motor blocked](https://developer.nuki.io/t/motor-blocked-and-cant-access-the-home/20348)
- [SmartHomePerfected — Best Multipoint Smart Locks](https://www.smarthomeperfected.com/best-multipoint-smart-locks/)
- [Picard Serrures — Parade 2](https://www.picard-serrures.com/global/fr/produits/parade-2)
- [Tordjman Metal — Serrure connectee](https://www.tordjmanmetal.fr/serrures/la-serrure-connectee/)
- [Fichet — Kibolt S](https://www.porte-blindee.paris/serrure-multipoints-connectee-kibolt-s/)
- [Kaspersky — 3 Reasons Not to Use Smart Locks](https://www.kaspersky.com/blog/3-reasons-not-to-use-smart-locks/47866/)
- [Home Assistant Community — Smart Locks 2025](https://community.home-assistant.io/t/smart-locks-in-2025/828608)
- [SwitchBot EU — Lock Ultra Touch Combo](https://eu.switch-bot.com/fr/products/switchbot-lock-ultra-touch-combo-fr)
