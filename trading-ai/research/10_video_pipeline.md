# Pipeline vidéo (démarré le 2026-10-03/04)

Suite de `09_written_corpus_synthesis.md` §7. Même ordre que le corpus
écrit : **collecter → dédupliquer → formaliser → vérifier la testabilité →
filtrer → prioriser → tester**. Aucune vidéo n'est une preuve ; une vidéo ne
peut produire que des claims tagués [A]-[E] et des candidats [C].

## 1. Objectif de la collecte

Combler les lacunes laissées par le corpus écrit, par ordre de pertinence :

| Priorité | Lacune | Pourquoi une vidéo |
|---|---|---|
| 1 | Market Profile (#13, MISSING) | Domaine de praticiens, livres de référence inaccessibles (S006) ; l'auteur de référence (J. Dalton) publie lui-même des webinaires |
| 2 | COT / positioning (#17-18, PARTIAL) | Corpus écrit au niveau résumé seulement (S017, S018) ; usage pratique du rapport COT très documenté en vidéo |
| 3 | Sentiment (#16), régimes (#15) | Seulement si une vidéo apporte une méthode précise non couverte |
| — | Mécanique des options (#19) | Non prioritaire tant qu'aucune stratégie options n'est envisagée |

## 2. Critères de sélection

Retenir une vidéo seulement si :
1. **Auteur identifié** et lien direct avec le domaine (auteur de la
   méthode, institution, praticien nommé) ;
2. **Contenu substantiel** (≥ ~10 min, explications de règles ou de
   données) — exclus : shorts, teasers, compilations ;
3. **Mise en ligne par l'ayant droit** (chaîne de l'auteur, de l'éditeur,
   de la bourse, du courtier) — exclus : réuploads de livres audio,
   copies de formations payantes ;
4. **Non redondante** avec une vidéo déjà traitée du même auteur (deux
   vidéos d'un même formateur ne sont **pas** deux sources indépendantes —
   `07_knowledge_pipeline.md` §5) ;
5. Sous-titres récupérables par un client officiel, ou audio transcriptible
   localement à coût nul.

Les webinaires commerciaux sont acceptés quand l'auteur est la référence du
domaine, avec **signalement explicite du contenu promotionnel** et de
l'intérêt commercial dans le fichier de claims.

## 3. Méthode d'accès et de transcription

- `yt-dlp` avec clients officiels uniquement : `mweb` (métadonnées),
  `web_embedded` (sous-titres). **Aucun cookie, aucun miroir (Invidious),
  aucune API non documentée** — même principe que pour le corpus écrit.
- Requêtes espacées (une piste de sous-titres à la fois, pause entre les
  vidéos) : un HTTP 429 a été reçu lors d'une deuxième requête rapprochée.
- Nettoyage : `parse_vtt` + `_dedupe` du skill `watch`, puis suppression
  des chevauchements des sous-titres glissants (script local), découpage en
  blocs de 20 minutes avec horodatage `[hh:mm:ss]`.
- Repli si pas de sous-titres : transcription locale gratuite (Whisper CPU)
  seulement si nécessaire ; jamais de service payant.
- Textes bruts conservés **hors dépôt** (scratchpad), seuls les claims
  horodatés sont commités.

## 4. Vidéos candidates et statut

| ID | Vidéo | Auteur / chaîne | Durée | Domaine | Statut |
|---|---|---|---|---|---|
| V001 | The Market Profile: Trading Value versus Price (LgIPFsIjyLs, 2014) | James Dalton (chaîne officielle) | 1:25:48 | #13 | **Traitée** — `claims/V001.md`, 25 claims |
| V002 | Commitment of Traders COT Report – What You Need to Know (W3jOAyaM6q4, 2022) | Barchart | 1:01:54 | #17-18 | **Traitée** — `claims/V002.md`, 15 claims |
| — | Futures Open Interest and Commitments of Traders Data (FZIxzsY14b0) | TradeStation | 43:19 | #17-18 | À traiter |
| — | Profiling for Profits with Jim Dalton (_UvLP87BEs4) | Topstep | 58:11 | #13 | Candidat — même auteur que V001 : retenu seulement si contenu non redondant (non indépendant) |
| — | Confessions of a Market Maker Ep. 91 (0WC54SmNrd0) | — | 53:13 | #13 | Candidat secondaire (même auteur) |
| — | Anthony Crudele podcast avec J. Dalton (yNaLtSHi9AI) | Anthony Crudele | 1:25:35 | #13 | Candidat secondaire (même auteur) |
| — | Barchart COT court (7sT03ShSxQs) | Barchart | 9:40 | #17-18 | Probablement redondant avec la vidéo longue de la même chaîne |
| — | Andy Waldock / MoneyShow (KKxtOZOBpH4) | MoneyShow | 4:36 | #17-18 | Trop court — candidat de dernier recours |
| — | VSA (3YghcVbsab4) | ERA | 12:41 | #11 | Faible qualité attendue — non prioritaire |
| — | Conférence française 2012 (fx8x7LdaNIw) | — | — | #13 | Métadonnées non récupérables — écarté |
| — | Livre audio de Dalton réuploadé (naCG2eUtLg0) | tiers | — | #13 | **Exclu** : copie non autorisée d'une œuvre sous droit d'auteur |

## 5. Ce que le pipeline vidéo ne fait pas

- Aucun backtest pendant la collecte ; aucune entrée dans
  `hypotheses/registry.json` avant la phase de dédoublonnage/formalisation
  commune au corpus écrit et vidéo.
- Aucun chiffre d'une vidéo (ex. "65 % of the time", C-V001-16) n'est
  repris comme fait : il devient au mieux un candidat [E] à mesurer.
