#!/usr/bin/env python3
"""
Discord Rich Presence Manager v3.0
Avec système de présets.
"""

import os
import sys
import time
import json
import threading
import re
import ctypes
import warnings
from pathlib import Path
from datetime import datetime

warnings.filterwarnings("ignore", category=RuntimeWarning)

# ── Dépendances ───────────────────────────────────────────────────────────────
try:
    from pypresence import Presence, InvalidID, InvalidPipe
except ImportError:
    print("\n[!] Module manquant : pypresence")
    print("    Lance : pip install pypresence\n")
    sys.exit(1)

# ── Couleurs ANSI ─────────────────────────────────────────────────────────────
RESET = "\033[0m";  BOLD = "\033[1m";  DIM = "\033[2m"
B = "\033[94m";     G = "\033[92m";    Y = "\033[93m"
R = "\033[91m";     C = "\033[96m";    M = "\033[95m"
W = "\033[97m"

def enable_ansi():
    if sys.platform == "win32":
        try:
            k = ctypes.windll.kernel32
            k.SetConsoleMode(k.GetStdHandle(-11), 7)
        except Exception:
            pass

enable_ansi()

# ── Constantes ────────────────────────────────────────────────────────────────
CONFIG_FILE = Path.home() / ".discord_presence_config.json"
WIDTH = 60

# ── Helpers UI ────────────────────────────────────────────────────────────────
def clear():
    os.system("cls" if sys.platform == "win32" else "clear")

def strip_ansi(s):
    return re.sub(r'\033\[[0-9;]*m', '', s)

def box(lines, color=B, title=""):
    w = WIDTH
    if title:
        pad = w - 4 - len(title)
        top = f"{color}╔══{RESET}{BOLD}{W} {title} {RESET}{color}{'═'*(pad//2)}{'═'*(pad-pad//2)}╗{RESET}"
    else:
        top = f"{color}╔{'═'*(w-2)}╗{RESET}"
    print(top)
    for l in lines:
        pad = w - 4 - len(strip_ansi(l))
        print(f"{color}║{RESET} {l}{' '*max(0,pad)} {color}║{RESET}")
    print(f"{color}╚{'═'*(w-2)}╝{RESET}")

def header(subtitle=""):
    clear()
    art = [
        f"{M}╔{'═'*56}╗{RESET}",
        f"{M}║{RESET}  {B}{BOLD}  ██████╗ ██████╗ ██████╗{RESET}                       {M}║{RESET}",
        f"{M}║{RESET}  {B}{BOLD} ██╔══██╗██╔══██╗██╔══██╗{RESET}  {C}Discord{RESET}              {M}║{RESET}",
        f"{M}║{RESET}  {B}{BOLD} ██████╔╝██████╔╝██████╔╝{RESET}  {C}Rich Presence{RESET}        {M}║{RESET}",
        f"{M}║{RESET}  {B}{BOLD} ██╔══██╗██╔═══╝ ██╔═══╝{RESET}   {DIM}Manager v3.0{RESET}         {M}║{RESET}",
        f"{M}║{RESET}  {B}{BOLD} ██║  ██║██║     ██║{RESET}                           {M}║{RESET}",
        f"{M}║{RESET}  {B}{BOLD} ╚═╝  ╚═╝╚═╝     ╚═╝{RESET}                           {M}║{RESET}",
        f"{M}╚{'═'*56}╝{RESET}",
    ]
    for l in art:
        print(l)
    if subtitle:
        print(f"\n  {DIM}{subtitle}{RESET}")
    print()

def prompt(label, default="", color=C):
    d = f" {DIM}[{default}]{RESET}" if default else ""
    val = input(f"  {color}▶{RESET} {label}{d} : ").strip()
    return val if val else default

def choose(label, options, color=Y, allow_back=False):
    print(f"\n  {color}{BOLD}{label}{RESET}")
    for i, o in enumerate(options, 1):
        print(f"    {DIM}{i}.{RESET} {o}")
    if allow_back:
        print(f"    {DIM}0.{RESET} {DIM}← Retour{RESET}")
    while True:
        try:
            raw = input(f"  {color}▶{RESET} Choix : ").strip()
            v = int(raw)
            if allow_back and v == 0:
                return -1
            if 1 <= v <= len(options):
                return v - 1
        except (ValueError, KeyboardInterrupt):
            pass
        print(f"  {R}Entrée invalide.{RESET}")

def status_line(text, color=G, icon="●"):
    print(f"\n  {color}{icon}{RESET} {text}")

def divider(label=""):
    if label:
        pad = 54 - len(label) - 2
        print(f"  {DIM}─── {RESET}{label}{DIM} {'─'*max(0,pad)}{RESET}")
    else:
        print(f"  {DIM}{'─'*54}{RESET}")

# ── Config & présets ──────────────────────────────────────────────────────────
def load_data() -> dict:
    """Charge le fichier de config complet."""
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"client_id": "", "presets": {}, "last_preset": ""}

def save_data(data: dict):
    CONFIG_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def preset_summary(p: dict) -> str:
    name    = p.get("name", "?")
    details = p.get("details", "")
    img     = p.get("image_key", "")
    btns    = len(p.get("buttons", []))
    parts   = [f"{W}{name}{RESET}"]
    if details:
        parts.append(f"{DIM}{details}{RESET}")
    if img:
        parts.append(f"{C}[img:{img}]{RESET}")
    if btns:
        parts.append(f"{G}[{btns} btn]{RESET}")
    return "  ".join(parts)

# ── Formulaire préset ─────────────────────────────────────────────────────────
def form_preset(existing: dict | None = None) -> dict:
    """Formulaire pour créer/modifier un préset."""
    e = existing or {}
    header("Nouveau préset" if not existing else "Modifier le préset")
    box(["Entrée = garder la valeur actuelle."], title="ÉDITEUR DE PRÉSET")
    print()

    divider("① NOM DU PRÉSET")
    preset_name = prompt("Nom du préset (ex: ERLC, Minecraft…)", e.get("preset_name", ""))

    divider("② JEU / APPLICATION")
    name    = prompt("Nom affiché (ligne principale)", e.get("name", "Mon Jeu"))
    details = prompt("Détails (2e ligne)", e.get("details", ""))
    state   = prompt("État (3e ligne)", e.get("state", ""))

    divider("③ TIMER")
    use_timer = prompt("Afficher un timer ? (o/n)", "o" if e.get("use_timer", True) else "n").lower() == "o"

    divider("④ IMAGE PRINCIPALE")
    print(f"  {DIM}Entre le nom de la clé uploadée dans Discord Developer → Rich Presence → Art Assets{RESET}")
    image_key  = prompt("Clé d'asset (ex: erlc)", e.get("image_key", ""))
    image_text = prompt("Texte au survol", e.get("image_text", name)) if image_key else ""

    divider("⑤ PETITE IMAGE (coin bas-droit, optionnel)")
    small_key  = prompt("Clé d'asset petite image", e.get("small_key", ""))
    small_text = prompt("Texte au survol petite image", e.get("small_text", "")) if small_key else ""

    divider("⑥ BOUTONS (max 2)")
    print(f"  {DIM}Laisser le label vide = pas de bouton{RESET}")
    buttons    = []
    saved_btns = e.get("buttons", [])
    for i in range(2):
        print(f"\n  {C}— Bouton {i+1} —{RESET}")
        sb    = saved_btns[i] if i < len(saved_btns) else {}
        label = prompt("  Label", sb.get("label", ""))
        if not label:
            continue
        url_b = prompt("  URL (https://…)", sb.get("url", "https://"))
        if url_b.startswith("http"):
            buttons.append({"label": label, "url": url_b})

    return {
        "preset_name": preset_name or name,
        "name":        name,
        "details":     details,
        "state":       state,
        "use_timer":   use_timer,
        "image_key":   image_key,
        "image_text":  image_text,
        "small_key":   small_key,
        "small_text":  small_text,
        "buttons":     buttons,
    }

# ── Menu présets ──────────────────────────────────────────────────────────────
def menu_presets(data: dict) -> dict:
    """Gestion des présets : créer, modifier, supprimer."""
    while True:
        header("Gestion des présets")
        presets = data.get("presets", {})

        if presets:
            box([f"  {i+1}. {preset_summary(p)}" for i, p in enumerate(presets.values())],
                title=f"PRÉSETS ({len(presets)})", color=C)
        else:
            box([f"  {Y}Aucun préset pour l'instant.{RESET}"], color=Y)

        print()
        idx = choose("QUE VEUX-TU FAIRE ?", [
            f"{G}+  Créer un nouveau préset{RESET}",
            f"{C}✎  Modifier un préset existant{RESET}",
            f"{R}✕  Supprimer un préset{RESET}",
            f"{DIM}←  Retour au menu principal{RESET}",
        ])

        keys = list(presets.keys())

        # ── Créer ──
        if idx == 0:
            p = form_preset()
            key = p["preset_name"].lower().replace(" ", "_")
            # éviter les doublons de clé
            base, n = key, 1
            while key in presets:
                key = f"{base}_{n}"; n += 1
            presets[key] = p
            data["presets"] = presets
            save_data(data)
            status_line(f"Préset {W}{p['preset_name']}{RESET}{G} créé !", G, "✓")
            time.sleep(1.5)

        # ── Modifier ──
        elif idx == 1:
            if not keys:
                status_line("Aucun préset à modifier.", Y, "!")
                time.sleep(1.5)
                continue
            header("Modifier un préset")
            pi = choose("Quel préset modifier ?",
                        [preset_summary(presets[k]) for k in keys], allow_back=True)
            if pi == -1:
                continue
            key = keys[pi]
            p   = form_preset(presets[key])
            new_key = p["preset_name"].lower().replace(" ", "_")
            if new_key != key:
                del presets[key]
            presets[new_key] = p
            data["presets"]  = presets
            save_data(data)
            status_line(f"Préset {W}{p['preset_name']}{RESET}{G} mis à jour !", G, "✓")
            time.sleep(1.5)

        # ── Supprimer ──
        elif idx == 2:
            if not keys:
                status_line("Aucun préset à supprimer.", Y, "!")
                time.sleep(1.5)
                continue
            header("Supprimer un préset")
            pi = choose("Quel préset supprimer ?",
                        [preset_summary(presets[k]) for k in keys], allow_back=True)
            if pi == -1:
                continue
            key  = keys[pi]
            name = presets[key].get("preset_name", key)
            confirm = prompt(f"Supprimer {W}{name}{RESET} ? (o/n)", "n", color=R).lower()
            if confirm == "o":
                del presets[key]
                data["presets"] = presets
                if data.get("last_preset") == key:
                    data["last_preset"] = ""
                save_data(data)
                status_line(f"Préset {W}{name}{RESET}{G} supprimé.", G, "✓")
            else:
                status_line("Annulé.", DIM, "○")
            time.sleep(1.5)

        # ── Retour ──
        else:
            return data

# ── Activation ────────────────────────────────────────────────────────────────
def start_presence(cfg: dict, client_id: str):
    header("Rich Presence active")
    img_status = f"{G}✓ {cfg['image_key']}{RESET}" if cfg.get("image_key") else f"{DIM}✗ aucune{RESET}"
    box([
        f"  Préset  : {M}{cfg.get('preset_name','?')}{RESET}",
        f"  Jeu     : {W}{cfg.get('name','?')}{RESET}",
        f"  Détails : {DIM}{cfg.get('details','—')}{RESET}",
        f"  État    : {DIM}{cfg.get('state','—')}{RESET}",
        f"  Image   : {img_status}",
        f"  Boutons : {G}{len(cfg.get('buttons',[]))}/2{RESET}",
        f"  Timer   : {''+G+'activé'+RESET if cfg.get('use_timer') else DIM+'désactivé'+RESET}",
    ], title="RÉSUMÉ", color=G)

    status_line("Connexion à Discord…", Y, "⟳")
    try:
        rpc = Presence(client_id)
        rpc.connect()
    except (InvalidID, InvalidPipe, Exception) as e:
        status_line(f"Impossible de se connecter : {e}", R, "✗")
        print(f"\n  {DIM}Assure-toi que Discord est ouvert et que le Client ID est correct.{RESET}")
        input("\n  Appuie sur Entrée pour revenir au menu…")
        return

    start_ts = int(datetime.now().timestamp()) if cfg.get("use_timer") else None

    def update():
        while True:
            try:
                rpc.update(
                    details     = cfg.get("details") or None,
                    state       = cfg.get("state") or None,
                    start       = start_ts,
                    large_image = cfg.get("image_key") or None,
                    large_text  = cfg.get("image_text") or None,
                    small_image = cfg.get("small_key") or None,
                    small_text  = cfg.get("small_text") or None,
                    buttons     = cfg.get("buttons") or None,
                )
            except Exception:
                try:
                    rpc.connect()
                except Exception:
                    pass
            time.sleep(15)

    threading.Thread(target=update, daemon=True).start()

    status_line(f"Rich Presence active — {W}{cfg['preset_name']}{RESET}{G} !", G, "✓")
    print()
    divider()
    print(f"  {DIM}Appuie sur {W}Ctrl+C{RESET}{DIM} pour arrêter.{RESET}")
    divider()

    try:
        while True:
            elapsed = int(time.time()) - (start_ts or int(time.time()))
            h, m, s = elapsed // 3600, (elapsed % 3600) // 60, elapsed % 60
            sys.stdout.write(f"\r  {G}●{RESET} En cours [{M}{cfg['preset_name']}{RESET}] — {W}{h:02d}:{m:02d}:{s:02d}{RESET}  ")
            sys.stdout.flush()
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n\n  {Y}Arrêt…{RESET}")
        try:
            rpc.clear(); rpc.close()
        except Exception:
            pass
        status_line("Rich Presence désactivée.", DIM, "○")
        time.sleep(1)

# ── Menu principal ─────────────────────────────────────────────────────────────
def main():
    data = load_data()

    while True:
        header()
        presets   = data.get("presets", {})
        client_id = data.get("client_id", "")
        last      = data.get("last_preset", "")

        # Infos client ID
        cid_status = f"{G}✓ configuré{RESET}" if client_id else f"{R}✗ manquant{RESET}"
        last_name  = presets[last].get("preset_name", last) if last in presets else "—"

        box([
            f"  Client ID : {cid_status}",
            f"  Présets   : {C}{len(presets)}{RESET} enregistré(s)",
            f"  Dernier   : {M}{last_name}{RESET}",
        ], title="ÉTAT", color=C)

        print()
        idx = choose("QUE VEUX-TU FAIRE ?", [
            f"{G}▶  Activer un préset{RESET}",
            f"{M}☰  Gérer les présets{RESET}  {DIM}(créer, modifier, supprimer){RESET}",
            f"{Y}⚙  Changer le Client ID Discord{RESET}",
            f"{R}✕  Quitter{RESET}",
        ])

        # ── Activer un préset ──
        if idx == 0:
            if not client_id:
                status_line("Client ID manquant ! Configure-le d'abord (option 3).", R, "✗")
                time.sleep(2); continue
            if not presets:
                status_line("Aucun préset ! Crée-en un d'abord (option 2).", Y, "!")
                time.sleep(2); continue

            header("Choisir un préset")
            keys = list(presets.keys())
            pi   = choose("Quel préset activer ?",
                          [preset_summary(presets[k]) for k in keys], allow_back=True)
            if pi == -1:
                continue
            key  = keys[pi]
            data["last_preset"] = key
            save_data(data)
            start_presence(presets[key], client_id)

        # ── Gérer présets ──
        elif idx == 1:
            data = menu_presets(data)

        # ── Client ID ──
        elif idx == 2:
            header("Client ID Discord")
            box([
                f"  {DIM}Va sur {C}discord.com/developers/applications{RESET}",
                f"  {DIM}→ ton app → General Information{RESET}",
                f"  {DIM}Copie l'«Application ID»{RESET}",
            ], color=Y)
            print()
            data["client_id"] = prompt("Client ID", client_id)
            save_data(data)
            status_line("Client ID sauvegardé !", G, "✓")
            time.sleep(1.5)

        # ── Quitter ──
        else:
            header()
            status_line("À bientôt !", M, "✦")
            print()
            sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {DIM}Interruption. Bye!{RESET}\n")
        sys.exit(0)
