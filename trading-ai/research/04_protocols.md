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

## Ce que ces deux protocoles garantissent ensemble

Une hypothèse ne peut jamais passer de "idée entendue dans une vidéo" à
"capital réel" sans traverser, dans l'ordre : traçabilité de la source →
formulation falsifiable → test contre baseline → vérification
d'indépendance → robustesse par sous-période → robustesse par paramètre →
coûts réels → paper trading. Chaque maillon a déjà un cas d'usage réel dans
ce projet (H003 pour illustrer le danger de sauter la vérification
d'indépendance) sauf les deux derniers (coûts réels, paper trading), qui
restent à exercer sur une future hypothèse.
