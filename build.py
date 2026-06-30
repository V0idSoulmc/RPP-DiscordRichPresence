#!/usr/bin/env python3
"""
Build script — Discord Rich Presence Manager
Génère un .exe standalone avec PyInstaller.

Usage:
    python build.py

Pré-requis (installés automatiquement si absents) :
    pip install pyinstaller pypresence
"""

import subprocess
import sys
import os
from pathlib import Path

APP_NAME    = "DiscordPresenceManager"
SCRIPT      = "discord_presence.py"
ICON        = "icon.ico"           # Optionnel — place un .ico à côté de ce script
VERSION     = "3.0.0"

def install_if_missing(package):
    try:
        __import__(package.replace("-", "_"))
    except ImportError:
        print(f"[→] Installation de {package}…")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    # ── Dépendances build ─────────────────────────────────────────────────────
    install_if_missing("pyinstaller")
    install_if_missing("pypresence")

    script_path = Path(SCRIPT)
    if not script_path.exists():
        print(f"[✗] Fichier introuvable : {SCRIPT}")
        print(f"    Place ce build.py dans le même dossier que {SCRIPT}")
        sys.exit(1)

    # ── Commande PyInstaller ──────────────────────────────────────────────────
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                     # Tout dans un seul .exe
        "--console",                     # Garde la fenêtre console (app terminal)
        "--name", APP_NAME,
        "--clean",
    ]

    # Icône optionnelle
    if Path(ICON).exists():
        cmd += ["--icon", ICON]
    else:
        print(f"[!] Pas d'icône trouvée ({ICON}) — build sans icône.")

    cmd.append(SCRIPT)

    print("\n[→] Build en cours…\n")
    result = subprocess.run(cmd)

    if result.returncode == 0:
        exe = Path("dist") / f"{APP_NAME}.exe"
        print(f"\n[✓] Build réussi !")
        print(f"    Exe : {exe.resolve()}")
        print(f"\n    Ce fichier est 100% autonome — aucune installation Python requise.")
        print(f"    Tu peux maintenant l'utiliser avec Inno Setup pour créer l'installateur.")
    else:
        print("\n[✗] Build échoué. Consulte les messages ci-dessus.")
        sys.exit(1)

if __name__ == "__main__":
    main()
