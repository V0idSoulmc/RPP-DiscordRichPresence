; ============================================================
;  Discord Rich Presence Manager — Inno Setup Script
;  Génère un installateur .exe propre pour Windows
;
;  Pré-requis :
;    1. Lance build.py pour générer dist\DiscordPresenceManager.exe
;    2. Installe Inno Setup : https://jrsoftware.org/isinfo.php
;    3. Ouvre ce fichier dans Inno Setup Compiler et clique "Build"
;
;  L'installateur final sera dans le dossier Output\
; ============================================================

#define AppName      "Discord Rich Presence Manager"
#define AppVersion   "3.0"
#define AppPublisher "V0idSoul"
#define AppExeName   "DiscordPresenceManager.exe"

[Setup]
; Infos de base
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisherURL=https://github.com/
AppSupportURL=https://github.com/
AppUpdatesURL=https://github.com/
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
OutputDir=Output
OutputBaseFilename=DiscordPresenceManager_Setup_v{#AppVersion}
; Icône de l'installateur (optionnel — retire la ligne si tu n'as pas de .ico)
; SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
; Pas besoin de droits admin si tu veux installer dans AppData
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "startmenuicon"; Description: "Créer un raccourci dans le menu Démarrer"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
; L'exe principal généré par PyInstaller — chemin relatif à ce .iss
Source: "dist\{#AppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{group}\Désinstaller {#AppName}"; Filename: "{uninstallexe}"
Name: "{userdesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon
Name: "{userstartmenu}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: startmenuicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(AppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Nettoie le dossier d'installation à la désinstallation
Type: filesandordirs; Name: "{app}"
