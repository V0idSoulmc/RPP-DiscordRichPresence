# 🎮 Discord Rich Presence Manager

Personnalise ton statut Discord depuis le terminal — avec présets, images et boutons cliquables.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Discord](https://img.shields.io/badge/Discord-Rich%20Presence-5865F2)

---

## 📋 Prérequis

- **Python 3.10+** — [python.org](https://www.python.org/downloads/)
- **Discord** ouvert sur ton PC
- Un compte sur [Discord Developer Portal](https://discord.com/developers/applications)

---

## ⚙️ Installation

**1. Installe la dépendance :**
```
pip install pypresence
```

**2. Lance le script :**
```
python discord_presence.py
```

---

## 🚀 Première utilisation

### Étape 1 — Créer une application Discord

1. Va sur [discord.com/developers/applications](https://discord.com/developers/applications)
2. Clique **New Application**
3. Donne-lui le nom qui s'affichera sur Discord (ex: `ERLC | QCFR`)
4. Copie l'**Application ID** (tu en auras besoin dans le script)

### Étape 2 — Ajouter une image (optionnel)

1. Dans ton application → **Rich Presence** → **Art Assets**
2. Clique **Ajouter des images**
3. Upload ton image (PNG/JPG, 512x512 minimum recommandé)
4. Donne-lui un nom simple (ex: `erlc`) — retiens ce nom !

> ⚠️ Les noms d'assets ne sont pas modifiables après enregistrement. Si tu veux changer le nom, supprime l'asset et re-uploade.

### Étape 3 — Configurer le script

Dans le menu principal :

1. **⚙ Changer le Client ID Discord** → colle ton Application ID
2. **☰ Gérer les présets** → **+ Créer un nouveau préset**
3. Remplis les champs et active ta Rich Presence !

---

## 🗂️ Système de présets

Tu peux créer autant de présets que tu veux, chacun avec ses propres paramètres.

| Champ | Description |
|---|---|
| Nom du préset | Nom interne pour retrouver le préset dans la liste |
| Nom affiché | *(ignoré par Discord — change le nom dans le Developer Portal)* |
| Détails | 1re ligne sous le titre |
| État | 2e ligne sous le titre |
| Timer | Chrono qui s'affiche depuis le lancement |
| Image principale | Nom de la clé d'asset Discord (ex: `erlc`) |
| Petite image | Icône en coin bas-droit (2e asset Discord) |
| Boutons | Jusqu'à 2 boutons avec label + URL |

**Exemple de présets :**
```
1. ERLC   → "Joue a ER:LC" | image: erlc | bouton: Discord
2. AFK    → "Je suis AFK"  | pas d'image | pas de boutons
3. Stream → "En live !"    | image: logo  | bouton: Twitch
```

---

## 🖼️ Aperçu du résultat sur Discord

```
┌─────────────────────────────────────┐
│  Joue à                             │
│  ┌──────┐  ERLC | QCFR             │
│  │      │  Joue a ER:LC            │
│  │ img  │  Sur le serveur QC FR    │
│  └──────┘  🎮 0:42                 │
│  [ Rejoindre ]  [ Mon Discord ]     │
└─────────────────────────────────────┘
```

---

## ❓ Problèmes fréquents

**Mon image s'affiche avec un `?`**
→ Discord met 5 à 15 minutes pour activer un nouvel asset. Attends puis réessaie.

**Le titre affiche le mauvais nom**
→ Le titre vient du **nom de ton app** sur Discord Developer, pas du script. Change-le là-bas, puis ferme/réouvre Discord.

**Les boutons ne s'affichent pas**
→ C'est normal ! Discord cache tes propres boutons. Les autres personnes les voient parfaitement.

**Erreur de connexion**
→ Assure-toi que Discord est bien ouvert. Le script a besoin que l'app tourne en arrière-plan.

**RuntimeWarning coroutine**
→ Mis à jour dans la v3.0, ce warning est supprimé automatiquement.

---

## 📁 Fichiers

| Fichier | Description |
|---|---|
| `discord_presence.py` | Script principal |
| `~/.discord_presence_config.json` | Config & présets sauvegardés automatiquement |

---

## 🔖 Versions

| Version | Nouveautés |
|---|---|
| v1.0 | Rich Presence de base |
| v2.0 | Images via clés d'assets Discord |
| v3.0 | Système de présets, petite image, fix warnings |

---

*Made — By V0idSoul*
