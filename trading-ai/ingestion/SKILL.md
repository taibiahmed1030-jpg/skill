---
name: ingest-trading-content
description: Traite une vidéo/formation de trading en sous-titres pour en extraire des hypothèses testables dans le registre, sans jamais juger si une méthode est rentable. Usage: /ingest-trading-content <url-youtube>
---

# Ingestion de contenu de trading

Ce process convertit une vidéo (ou tout contenu long) en entrées structurées
dans `hypotheses/registry.json`, **une seule fois** par source. Ensuite, plus
jamais besoin de retoucher la vidéo brute — c'est ce qui règle le problème de
consommation de tokens évoqué par l'utilisateur.

C'est la généralisation du traitement fait manuellement sur la formation
"Apprendre le Trading de A à Z" (Elliot, 11h46) — voir
`/home/user/skill/TRADING_KNOWLEDGE_BASE.md` pour un exemple complet de
sortie.

## Étape 0 — Vérifier avant de commencer

- La source est-elle déjà dans le registre (même `source.url`) ? Si oui, ne
  pas retraiter — proposer une mise à jour incrémentale seulement si le
  contenu a changé.
- Récupérer les sous-titres via le skill `watch` (yt-dlp) ou toute méthode
  disponible. Ne JAMAIS résumer depuis la mémoire/connaissances générales du
  modèle sur le sujet — seulement depuis le texte réel de la source.

## Étape 1 — Découpage en blocs

Découper le transcript en blocs de ~20 minutes (ou ~4000 mots), avec
déduplication des sous-titres qui se chevauchent (rolling captions). Ne
jamais traiter plus de 2-3 blocs par tour d'outil pour garder un contexte
gérable.

## Étape 2 — Extraction par bloc

Pour chaque bloc, extraire UNIQUEMENT :
1. Concepts importants (définitions, mécanismes)
2. Règles explicitement enseignées (conditions précises, pas des généralités)
3. Signaux, conditions d'entrée, conditions de sortie
4. Conditions explicites de non-trade
5. Gestion du risque
6. Timeframes
7. Données/indicateurs nécessaires
8. Hypothèses implicites non testées par le formateur
9. Limites/contradictions que le formateur lui-même reconnaît
10. Timestamp source

**Séparer systématiquement** : affirmation du formateur [A] / règle explicite
[B] / hypothèse testable [C] / opinion/interprétation [D] / info nécessitant
validation [E]. Ignorer le contenu promotionnel, les digressions
personnelles, les tutoriels de plateforme sans contenu de marché.

Ne jamais donner d'avis sur la qualité de la méthode enseignée.

## Étape 3 — Synthèse en connaissances compactes

Fusionner les extractions de blocs en un document structuré (principes,
lecture de marché, price action, indicateurs, setups, entrées, sorties,
no-trade, risk management, timeframes, erreurs à éviter — voir
`TRADING_KNOWLEDGE_BASE.md` comme gabarit). Ne pas répéter un concept déjà
capturé ailleurs dans le même document — une seule formulation canonique.

## Étape 4 — Claims tracés (PAS d'écriture directe dans le registre)

Mise à jour 2026-10-04 (pipeline `research/07_knowledge_pipeline.md`) :
l'ingestion s'arrête à l'étage **CLAIM**. Écrire un fichier
`research/claims/VXXX.md` (une ligne par claim : ID `C-VXXX-NN`, tag
[A]-[E], claim, timestamp, conditions/limites) et l'indexer dans
`research/CLAIMS_REGISTRY.md` (fusions, corroborations, conflits).
Signaler explicitement : contenu promotionnel, intérêt commercial,
exemples choisis a posteriori, chiffres sans méthodologie, backtests
montrés (et pourquoi ils sont recevables ou non).

La formalisation en hypothèses dans `hypotheses/registry.json` est une
étape **séparée et ultérieure**, commune à toutes les sources (écrites et
vidéo) : dédoublonnage → formalisation → vérification de testabilité →
filtrage → priorisation. Elle n'est jamais faite source par source.

Accès aux sous-titres : clients officiels `yt-dlp` uniquement (`mweb` pour
les métadonnées, `web_embedded` pour les sous-titres), sans cookies ni
miroirs, requêtes espacées (voir `research/10_video_pipeline.md`).

## Étape 5 — Rapport court

Ne jamais coller le contenu complet dans le chat. Donner uniquement :
- Durée traitée / parties manquantes
- Nombre de claims extraits, candidats [C], fusions/conflits signalés
- Fichier(s) mis à jour

## Ce que ce process NE fait PAS

- Il ne lance aucun backtest (ça, c'est `backtest/`).
- Il ne décide jamais qu'une méthode est "bonne" ou "rentable" — il formalise
  des affirmations en hypothèses testables, point.
- Il ne modifie jamais `backtest/` ni les statuts `validee`/`rejetee` d'une
  hypothèse déjà testée sans relancer explicitement le backtest correspondant.
