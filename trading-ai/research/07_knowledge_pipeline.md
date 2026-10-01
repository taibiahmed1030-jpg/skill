# Pipeline SOURCE → CLAIM → HYPOTHÈSE — architecture des registres

Formalise la demande du 2026-10 : construire une vraie base de connaissances
multi-sources (au-delà de la seule formation Elliot déjà ingérée), avec
déduplication et préservation des contradictions, **sans** backtester quoi
que ce soit avant d'avoir collecté, dédupliqué, formalisé et priorisé.

## 1. Le pipeline complet

```
SOURCE → INFORMATION → CLAIM → HYPOTHÈSE → FORMALISATION →
  TESTABLE / NON TESTABLE → (si testable) BACKTEST → VALIDATION → STATUT
```

| Étage | Ce qu'il produit | Qui le fait | Fichier |
|---|---|---|---|
| SOURCE | Une entrée candidate évaluée (titre, auteur, type, pourquoi elle mérite d'être lue) | Recherche (WebSearch + jugement), **avant** toute lecture complète | `research/SOURCE_REGISTRY.md` |
| INFORMATION | Contenu brut lu/visionné d'une source **sélectionnée** | Lecture humaine assistée / skill `watch` pour vidéo | Non stocké tel quel (coûteux en tokens) — passe directement à l'extraction |
| CLAIM | Affirmation atomique extraite, taguée [A]-[E], avec sa source exacte (timestamp/page) | LLM, une seule fois par source | `research/CLAIMS_REGISTRY.md` |
| HYPOTHÈSE | Un ou plusieurs claims équivalents fusionnés en une idée falsifiable unique, avec la liste de toutes ses sources | LLM (fusion/dédup) + vérification humaine si ambigu | `trading-ai/hypotheses/registry.json` |
| FORMALISATION | Conditions/entrée/sortie/no-trade/données nécessaires rendues vérifiables | LLM, suit `hypotheses/schema.md` | idem |
| TESTABLE / NON TESTABLE | Verdict de faisabilité (données disponibles ? condition chiffrable ?) | LLM + vérification de disponibilité des données | champ `statut` du registre |
| BACKTEST | Résultat empirique réel | **Code déterministe**, jamais le LLM | `trading-ai/backtest/results/*.json` |
| VALIDATION | Robustesse (indépendance, sous-périodes, coûts) — voir `04_protocols.md` | Code + revue humaine des seuils | idem |
| STATUT | État final dans le cycle de vie | Règles de promotion explicites, jamais "à l'instinct" | section 4 ci-dessous |

Ce pipeline **étend** celui déjà en place (`ingestion/SKILL.md`,
`04_protocols.md`) — il ne le remplace pas. Ce qui change : l'ajout d'un
étage CLAIM intermédiaire explicite (avant, les claims d'une vidéo allaient
directement en hypothèses ; avec plusieurs sources, il faut un endroit où
comparer des claims de sources différentes **avant** de décider s'ils
forment une seule hypothèse ou deux hypothèses contradictoires).

## 2. Pourquoi un registre de CLAIMS séparé du registre d'HYPOTHÈSES

Avec une seule source (Elliot), claim ≈ hypothèse : pas besoin de
distinguer. Avec plusieurs sources, deux problèmes apparaissent que seul un
étage intermédiaire résout proprement :

- **Doublon reformulé** : Source A dit "un VIX > 45 marque souvent un creux
  sur les actions US" ; Source B (papier académique) dit "les pics de
  volatilité implicite extrême coïncident historiquement avec des bas de
  marché actions". Ce sont deux *claims* différents (vocabulaire,
  rigueur, source différents) qui pointent vers **une seule hypothèse**
  (déjà H003 dans le registre). Sans registre de claims, on ne peut pas
  tracer facilement "combien de sources indépendantes disent la même
  chose" — on écraserait l'info ou on dupliquerait l'hypothèse.
- **Contradiction réelle** : Source C pourrait dire "les spikes de VIX
  extrêmes sont suivis en moyenne de nouvelle baisse à court terme (effet
  de panique qui continue)". C'est un claim qui **contredit** H003, pas un
  doublon. Les deux doivent rester visibles comme hypothèses séparées
  (ou une hypothèse avec statut `INCONCLUSIVE`/preuves mixtes) — jamais
  arbitrées par jugement LLM, seulement par le backtest.

Le registre de claims est donc la table de travail où la fusion/distinction
se décide, **avant** que quoi que ce soit touche le registre d'hypothèses
(qui doit rester propre — une ligne = une idée testable unique).

## 3. Format des registres

### `research/SOURCE_REGISTRY.md` (déjà créé séparément, voir tâche suivante)

Un tableau, une ligne par source candidate : `SOURCE_ID`, Titre, Auteur,
Type, URL, Sujet (domaine(s) de `06_domain_coverage.md`), Pourquoi elle
mérite d'être analysée, Qualité/pertinence apparente, Redondance avec
l'existant. **Un seul fichier markdown**, pas un fichier par source — avec
30 sources ciblées (pas 500), un tableau reste lisible et évite la
dispersion sur des dizaines de petits fichiers (contrainte explicite
"ne pas dupliquer l'info dans 5 fichiers").

### `research/CLAIMS_REGISTRY.md` (nouveau, créé maintenant, vide/squelette tant qu'aucune source n'est encore analysée en profondeur)

Même logique : un tableau markdown, une ligne par claim atomique.

| Colonne | Contenu |
|---|---|
| `CLAIM_ID` | `C001`, `C002`, ... (jamais réutilisé) |
| `SOURCE_ID` | Référence vers `SOURCE_REGISTRY.md` |
| Tag | `[A]` affirmation du formateur/auteur · `[B]` règle explicite · `[C]` hypothèse testable · `[D]` opinion/interprétation · `[E]` info nécessitant validation externe (reprend le tagging déjà en place dans `ingestion/SKILL.md`) |
| Claim (texte court) | L'affirmation telle qu'extraite, reformulée de façon neutre |
| Domaine | Un ou plusieurs domaines de `06_domain_coverage.md` |
| Localisation | Timestamp vidéo / page / section |
| Statut de fusion | `nouveau` / `fusionné dans HXXX` / `contredit HXXX` |

Seuls les claims tagués `[B]` ou `[C]` (règle explicite ou hypothèse
testable) donnent lieu à une entrée dans le registre d'hypothèses — `[A]`,
`[D]`, `[E]` restent dans ce registre comme connaissance qualitative ou
information à vérifier, pas comme hypothèse (même principe que la
knowledge base existante).

### `trading-ai/hypotheses/registry.json` (existant, étendu — pas recréé)

Le schéma actuel (`hypotheses/schema.md`) reste valide pour les champs
`conditions`/`entree`/`sortie`/`no_trade`/`timeframe`/`donnees_necessaires`.
Trois ajouts additifs (rétrocompatibles, les entrées H001-H010 ne sont pas
modifiées) pour supporter le multi-source :

```json
{
  "...": "... champs existants inchangés ...",
  "sources": [
    { "source_id": "S004", "claim_id": "C012", "accord": "confirme" }
  ],
  "nb_sources": 1,
  "nb_sources_independantes": 1,
  "mecanisme": "Explication causale proposée (pas juste la corrélation observée).",
  "complexite": "faible | moyenne | elevee",
  "biais_potentiel": "Ex: biais de survie, biais de confirmation du formateur, etc.",
  "statut_en": "UNTESTED"
}
```

`sources` remplace à terme le champ unique `source` (objet) pour les
nouvelles hypothèses multi-sources ; les hypothèses H001-H010 existantes
gardent leur champ `source` simple tel quel (une seule source = pas besoin
de migrer rétroactivement, cf. "ne pas recommencer ce qui est fait").
**Deux sources qui disent la même chose ne sont jamais traitées comme une
preuve statistique plus forte** — `nb_sources_independantes` est une
métadonnée de traçabilité, pas un critère de promotion de statut (les
critères de promotion restent purement statistiques, section 4).

## 4. Taxonomie de statut (anglais, telle que demandée)

Le registre existant utilise des statuts français (`non_testee`,
`en_test`, `validee`, `rejetee`, `non_testable`). La consigne du 2026-10
demande une taxonomie anglaise plus fine pour les nouvelles hypothèses
issues de ce pipeline. Les deux coexistent : `statut` (français, champ
historique, inchangé pour H001-H010) et `statut_en` (anglais, nouveau
champ, utilisé pour toute hypothèse créée à partir de maintenant).

| Statut EN | Équivalent FR le plus proche | Sens précis |
|---|---|---|
| `UNTESTED` | `non_testee` | Formalisée, aucun test lancé. |
| `TESTABLE` | — (nouveau) | Formalisée ET vérifiée faisable (données identifiées comme accessibles) mais pas encore testée — distingue explicitement "on pourrait tester" de "on n'a pas encore regardé". |
| `TESTING` | `en_test` | Test en cours / premiers résultats partiels, pas encore de verdict de robustesse complet. |
| `REJECTED` | `rejetee` | Le test contredit franchement l'hypothèse. |
| `INCONCLUSIVE` | — (nouveau) | Testée mais résultat ni significatif ni clairement négatif, OU sources contradictoires non encore arbitrées par backtest. Remplace l'ambiguïté qu'il y avait à forcer `en_test` pour ce cas. |
| `PROMISING` | — (nouveau, intermédiaire) | Significatif sur le test initial (étape A de `04_protocols.md`) mais n'a pas encore passé toute l'étape B (robustesse) — équivalent de l'état actuel réel de H003. |
| `ROBUST` | `validee`, critères resserrés | **Tous** les critères de `04_protocols.md` étape D réunis : p<0.05 sur observations indépendantes, ≥20 occurrences indépendantes, stable ≥2 sous-périodes, survit perturbation de paramètres, survit coûts réels. Jamais atteint parce qu'"une formation l'affirme" — uniquement par le backtest. |
| `RETIRED` | — (nouveau) | Hypothèse abandonnée sans avoir été réfutée statistiquement (ex: données définitivement indisponibles, devenue hors-sujet après choix de marché) — distinct de `REJECTED` qui implique un test négatif réel. |

Règle non négociable (rappel explicite de la consigne utilisateur) :
**aucune hypothèse ne peut atteindre `PROMISING` ou `ROBUST` uniquement
parce qu'une ou plusieurs sources l'affirment** — ces deux statuts ne sont
accessibles qu'après passage réel par `trading-ai/backtest/`.

## 5. Règle de déduplication et de préservation des contradictions

1. Avant de créer un nouveau claim : chercher dans `CLAIMS_REGISTRY.md` un
   claim déjà formulé sur le même mécanisme/domaine.
2. Si un claim équivalent existe et **pointe dans le même sens** (même
   prédiction) : ne pas créer de nouvelle hypothèse — ajouter la source à
   la liste `sources` de l'hypothèse existante, incrémenter
   `nb_sources`/`nb_sources_independantes` (si auteur/organisation
   réellement différents — deux vidéos du même formateur ne comptent pas
   comme deux sources indépendantes).
3. Si un claim équivalent existe mais **contredit** la prédiction (Source A
   dit X, Source B dit non-X sur les mêmes conditions) : créer une
   **deuxième hypothèse distincte**, avec un champ croisé
   `contredit_hypothese: "HXXX"` des deux côtés. Ne jamais trancher à la
   lecture — seul un backtest comparant les deux prédictions sur les mêmes
   données tranche, et seulement après l'étape de priorisation (section 6).
4. Documenter dans le registre de claims, pas dans le registre
   d'hypothèses, la raison de la fusion ou de la non-fusion (traçabilité
   de la décision éditoriale).

## 6. Garde-fou explicite : ne pas tout backtester immédiatement

Rappel de la consigne, déjà cohérent avec `04_protocols.md` section
"Protocole de recherche" (étape 5 : "aucune opinion sur la qualité d'une
méthode à ce stade") : l'ordre est collecter → dédupliquer → formaliser →
vérifier la testabilité → **filtrer/prioriser** → seulement ensuite tester.
L'étape de priorisation (choisir 2-3 hypothèses à tester en premier parmi
toutes celles formalisées) suit les mêmes critères que
`05_roadmap.md` ("données les plus simples d'accès en premier") — à
documenter explicitement au moment de cette sélection, pas avant.

## 7. Ce que ce document ne fait pas

Il ne crée aucune hypothèse, ne lance aucun backtest, ne choisit aucun
marché. Il ne fait que poser la structure pour que la collecte de sources
(tâche suivante) range immédiatement son résultat au bon endroit.
