# Protocole de recherche et protocole de validation

Ce document formalise des règles déjà appliquées de façon informelle dans ce
projet (ex. sur H003) pour qu'elles soient systématiques à partir de
maintenant, quel que soit le marché retenu.

## Protocole de recherche (comment une idée devient une hypothèse)

1. **Source identifiée et tracée.** Toute idée entre dans le registre avec un
   champ `source` renseigné (vidéo+timestamp, papier académique+DOI/URL,
   observation personnelle datée). Aucune hypothèse "orpheline".
2. **Séparation stricte affirmation / hypothèse.** Reprend le tagging déjà en
   place ([A]/[B]/[C]/[D]/[E], voir `ingestion/SKILL.md`). Une vidéo n'est
   jamais une preuve — règle déjà posée par l'utilisateur et non négociable.
3. **Formulation falsifiable obligatoire avant entrée dans le registre.** Si
   une idée ne peut pas être réduite à des conditions chiffrées/vérifiables,
   elle n'entre pas comme hypothèse testable — elle reste de la connaissance
   qualitative dans la knowledge base, ou elle est marquée `non_testable`
   avec le verdict expliquant précisément le blocage de formulation (cas déjà
   fait pour H004 et H007).
4. **Vérifier l'absence de doublon** avant toute création d'ID (même
   principe que posé dans `ingestion/SKILL.md` étape 4) — fusionner les
   sources sur une entrée existante plutôt que dupliquer.
5. **Aucune opinion sur la qualité d'une méthode** à ce stade — le jugement
   vient uniquement du protocole de validation ci-dessous.

## Protocole de validation (comment une hypothèse change de statut)

Reprend et généralise les règles déjà posées dans `hypotheses/schema.md`, en
les rendant plus précises à la lumière de ce qui a été appris sur H003.

### Étape A — Test initial (event study ou backtest simple)

- Définir la métrique de comparaison : toujours contre une **baseline**
  (jamais un rendement absolu seul).
- Calculer un test de significativité (permutation ou équivalent).
- **Vérifier explicitement l'indépendance des observations** avant de
  compter N. C'est l'étape qui a fait chuter H003 de "21 occurrences
  significatives" à "7 épisodes indépendants, significatif seulement à 3-6
  mois" — doit être systématique, pas une vérification ponctuelle qu'on
  pense à faire parfois.

### Étape B — Robustesse

- **Stabilité par sous-période** : refaire le test en excluant tour à tour
  chaque épisode/sous-période dominant. Si le résultat ne survit qu'avec un
  seul épisode inclus (ex: 2008 ou 2020), il n'est pas robuste.
- **Stabilité par perturbation de paramètres** : si l'hypothèse a un seuil
  (ex: "VIX > 45"), retester avec 40, 42, 48, 50 — un edge réel ne devrait
  pas disparaître pour une variation mineure du seuil (signe d'overfitting
  au seuil exact sinon).
- **Correction pour tests multiples** : si plusieurs hypothèses sont testées
  dans la même session de recherche, ajuster le seuil de signification en
  conséquence (ne pas traiter chaque p<0.05 isolément comme si c'était la
  seule hypothèse testée ce jour-là).

### Étape C — Coûts réels

- Modéliser spread/slippage/commissions réalistes pour le marché concerné
  (voir `01_market_comparison.md` pour les ordres de grandeur par
  catégorie) avant toute promotion. Un edge qui ne survit pas aux coûts
  réels n'est pas un edge exploitable, même s'il est statistiquement
  significatif sur prix "parfaits".

### Étape D — Promotion de statut

Reprend `hypotheses/schema.md` :
- `non_testee → en_test` dès le premier test lancé.
- `en_test → validee` **seulement si** toutes les conditions suivantes sont
  réunies : p < 0.05 sur données réellement indépendantes, ≥20 occurrences
  indépendantes, stable sur ≥2 sous-périodes distinctes, survit à une
  modélisation de coûts réaliste, survit à une perturbation de paramètres.
  Manquer un seul critère = rester `en_test` avec le critère manquant
  explicitement noté (c'est l'état actuel de H003 : 2 des 5 critères
  manquent — taille d'échantillon et test de coûts).
- `en_test → rejetee` si un des tests ci-dessus contredit franchement
  l'hypothèse (pas seulement "pas encore assez de preuve" — un vrai signal
  contraire).

### Étape E — Après "validee" : jamais directement en capital réel

Reprend `backtest/README.md` : paper trading obligatoire, comparaison des
résultats simulés vs backtest, démarrage en capital réel avec risque minimal
seulement après cette étape. **Mise en pause explicite pour l'instant** par
consigne de l'utilisateur — ce protocole est documenté mais pas encore
activé.

## Règles ajoutées à partir du corpus écrit (2026-10-04)

Chaque règle est tracée vers les claims qui la fondent (`CLAIMS_REGISTRY.md`,
section "Notes méthodologiques transversales"). Elles s'ajoutent aux étapes
A-E ci-dessus et s'appliquent à toute hypothèse issue du corpus.

**Données (étage DATA VALIDATION)**
- **R1 — Artefacts de microstructure** (N1 ; C-S003-07, C-S007-05, C-S015-10) : une autocorrélation négative à très court terme des prix de transaction peut n'être qu'un rebond bid-ask. Tester les hypothèses de retour à la moyenne court terme sur points milieux ou avec exécution décalée d'une période.
- **R2 — Mouvements extrêmes sans information** (N10 ; C-S005-05) : signaler les épisodes de type flash crash plutôt que les traiter comme signaux.
- **R3 — Contrats continus** (N14 ; C-S031-07) : documenter la méthode de raccordement aux dates de roulement.
- **R15 — Datation à la publication** (C-V002-01) : toute variable publiée avec retard (rapport COT : positions du mardi publiées le vendredi) est datée à sa **date de publication**, jamais à sa date d'observation. Ajoutée le 2026-10-04 pendant le pipeline vidéo.

**Conception des tests**
- **R4 — Validation chronologique** (N9 ; C-S020-01/02/04, C-S004-06) : jamais de k-fold standard sur séries temporelles ; validation chronologique avec purge et embargo dès que les horizons de labels se chevauchent.
- **R5 — Période de test intouchable** (N8 ; C-S009-04) : la période de test n'intervient dans **aucune** décision de sélection (actifs, paires, paramètres, sous-univers).
- **R6 — Journal de tous les essais** (N3 ; C-S027-08) : chaque configuration testée, y compris les échecs, est journalisée — condition pour calculer un PBO honnête.
- **R7 — Le PBO n'est pas une cible** (N2 ; C-S027-08) : il évalue un processus de sélection, il ne sert jamais de fonction objectif.
- **R8 — Placebo** (N5 ; C-S007-12) : comparer toute stratégie à la même règle appliquée à des sélections aléatoires.

**Inférence statistique**
- **R9 — Horizons chevauchants** (N4 ; C-S029-06) : erreurs standard corrigées (Hodrick 1992) ; un R² qui croît avec l'horizon sur un prédicteur persistant n'est pas une preuve.
- **R10 — Queues épaisses** (N11 ; C-S030-06) : préférer permutation et bootstrap aux tests supposant la normalité des rendements quotidiens (déjà le cas dans `backtest/metrics.py`).

**Coûts et économie de la stratégie**
- **R11 — Filtre brut d'abord** (N13 ; C-S031-04, C-S021-10) : vérifier que le rendement brut par trade dépasse le coût aller-retour avant toute analyse statistique.
- **R12 — Modèle de coûts minimal** (N7 ; C-S021-02/03) : coût fixe = demi-spread + frais par transaction ; termes d'impact seulement au-delà d'~1 % du volume journalier.
- **R13 — Primes nettes** (N6 ; C-S010-08, C-S007-06, C-S011-06) : toute prime académique est recalculée nette de coûts, rotation et contraintes d'investissabilité ; à notre petite taille, retenir les estimations de coûts pessimistes de la littérature.

**Critère de passage**
- **R14 — Gabarit à cinq critères** (N12 ; C-S031-01) : t ≥ 2 sur rendements **nets** hors échantillon ; effectif minimal par pli ; rendement net positif après friction ; **même signe sur chaque année de test** ; p-value de permutation < 0,05. S'ajoute aux critères de l'étape D (indépendance des observations, ≥ 20 occurrences indépendantes, perturbation de paramètres).

## Ce que ces deux protocoles garantissent ensemble

Une hypothèse ne peut jamais passer de "idée entendue dans une vidéo" à
"capital réel" sans traverser, dans l'ordre : traçabilité de la source →
formulation falsifiable → test contre baseline → vérification
d'indépendance → robustesse par sous-période → robustesse par paramètre →
coûts réels → paper trading. Chaque maillon a déjà un cas d'usage réel dans
ce projet (H003 pour illustrer le danger de sauter la vérification
d'indépendance) sauf les deux derniers (coûts réels, paper trading), qui
restent à exercer sur une future hypothèse.
