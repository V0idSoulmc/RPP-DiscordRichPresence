# 🎮 Discord Rich Presence Manager

Customize your Discord status from the terminal — with presets, images, and clickable buttons.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Discord](https://img.shields.io/badge/Discord-Rich%20Presence-5865F2)

🇫🇷 [Version française](../README.md)

---

## 📋 Requirements

- **Python 3.10+** — [python.org](https://www.python.org/downloads/)
- **Discord** running on your PC
- An account on [Discord Developer Portal](https://discord.com/developers/applications)

---

## ⚙️ Installation

**1. Install the dependency:**
```
pip install pypresence
```

**2. Run the script:**
```
python discord_presence.py
```

---

## 🚀 First-time Setup

### Step 1 — Create a Discord Application

1. Go to [discord.com/developers/applications](https://discord.com/developers/applications)
2. Click **New Application**
3. Give it the name that will show on Discord (e.g. `ERLC | QCFR`)
4. Copy the **Application ID** — you'll need it in the script

### Step 2 — Add an Image (optional)

1. In your application → **Rich Presence** → **Art Assets**
2. Click **Add Images**
3. Upload your image (PNG/JPG, 512x512 minimum recommended)
4. Give it a simple name (e.g. `erlc`) — remember this name!

> ⚠️ Asset names cannot be changed after saving. If you want to rename one, delete the asset and re-upload it.

### Step 3 — Configure the Script

In the main menu:

1. **⚙ Change Discord Client ID** → paste your Application ID
2. **☰ Manage presets** → **+ Create a new preset**
3. Fill in the fields and activate your Rich Presence!

---

## 🗂️ Preset System

You can create as many presets as you want, each with its own settings.

| Field | Description |
|---|---|
| Preset name | Internal name to find the preset in the list |
| Display name | *(ignored by Discord — change the name in the Developer Portal)* |
| Details | 1st line below the title |
| State | 2nd line below the title |
| Timer | Stopwatch displayed since launch |
| Large image | Discord asset key name (e.g. `erlc`) |
| Small image | Icon in the bottom-right corner (2nd Discord asset) |
| Buttons | Up to 2 buttons with label + URL |

**Example presets:**
```
1. ERLC   → "Playing ER:LC" | image: erlc | button: Discord
2. AFK    → "I'm AFK"       | no image    | no buttons
3. Stream → "Live now!"     | image: logo  | button: Twitch
```

---

## 🖼️ Preview on Discord

```
┌─────────────────────────────────────┐
│  Playing                            │
│  ┌──────┐  ERLC | QCFR             │
│  │      │  Playing ER:LC           │
│  │ img  │  On the QCFR server      │
│  └──────┘  🎮 0:42                 │
│  [ Join ]  [ My Discord ]           │
└─────────────────────────────────────┘
```

---

## ❓ Common Issues

**My image shows a `?`**
→ Discord takes 5 to 15 minutes to activate a new asset. Wait a bit and try again.

**The title shows the wrong name**
→ The title comes from your **app name** on Discord Developer, not from the script. Change it there, then close and reopen Discord.

**Buttons are not showing**
→ That's normal! Discord hides your own buttons from yourself. Other people see them just fine.

**Connection error**
→ Make sure Discord is open. The script needs the app running in the background.

**RuntimeWarning coroutine**
→ Fixed in v3.0, this warning is suppressed automatically.

---

## 📁 Files

| File | Description |
|---|---|
| `discord_presence.py` | Main script |
| `~/.discord_presence_config.json` | Config & presets saved automatically |

---

## 🔖 Changelog

| Version | What's new |
|---|---|
| v1.0 | Basic Rich Presence |
| v2.0 | Images via Discord asset keys |
| v3.0 | Preset system, small image, warning fix |

---

*Made with ❤️ — By V0idSoul*
