#!/usr/bin/env python3
"""Befehlspalette für NeoMutt: Leertaste → fuzzel-Menü mit deutschen
Einträgen, Auswahl → NeoMutt führt den Befehl aus.

Aufruf aus palette.rc:  source '~/.config/neomutt/palette.py index|'
NeoMutt übernimmt, was das Skript ausgibt, als Konfigurationsbefehl
(„exec <funktion>“ bzw. „push <tasten>“). Abbrechen gibt nichts aus.

Hinter jedem Eintrag steht die Taste, falls es eine gibt – zum Lernen
nebenbei. Neue Einträge: Zeile in BEFEHLE ergänzen (Bezeichnung, Taste,
NeoMutt-Befehl).
"""

import subprocess
import sys

# Gmail archivieren = in den Ordner Archive verschieben, ohne Rückfrage
# „anhängen?“ (confirm_append gilt nur für diesen einen Befehl)
ARCHIVIEREN = ('push "<enter-command>set confirm_append=no<enter><save-message>+Archive<enter>'
               '<enter-command>set confirm_append=yes<enter>"')
# Erst eigene Änderungen (Löschen, Archivieren) übernehmen, dann holen
ABRUFEN = 'push "<sync-mailbox><shell-escape>systemctl --user start mbsync.service<enter>"'

LESEN = [
    ("Antworten", "r", "exec reply"),
    ("Allen antworten", "", "exec group-reply"),
    ("Weiterleiten", "f", "exec forward-message"),
    ("Neue Mail schreiben", "m", "exec mail"),
    ("Archivieren", "", ARCHIVIEREN),
    ("In den Papierkorb", "dd", "exec delete-message"),
    ("Papierkorb rückgängig", "u", "exec undelete-message"),
    ("Gelesen / ungelesen", "", "exec toggle-new"),
    ("Stern setzen / entfernen", "F", "exec flag-message"),
    ("Mehr mit dieser Mail (Links, Bilder, Einladung)", "$mod+i", 'push "<f12>"'),
    ("Links öffnen", "gu", 'push "gu"'),
    ("Anhänge / HTML-Ansicht", "v", "exec view-attachments"),
    ("Suchen (geführt)", "gs", 'push "gs"'),
    ("Mails vom selben Absender", "gf", 'push "gf"'),
    ("Suchen (notmuch-Abfrage)", "gm", 'push "gm"'),
    ("Ungelesene Mails", "", 'push "<change-vfolder>Ungelesen<enter>"'),
    ("Mails von heute", "", 'push "<change-vfolder>Heute<enter>"'),
    ("Zur Inbox", "gi", 'push "gi"'),
    ("Ordner wechseln", "c", 'push "<change-folder>?"'),
    ("Jetzt abrufen", "", ABRUFEN),
    ("Änderungen jetzt übernehmen", "$", "exec sync-mailbox"),
]

BEFEHLE = {
    "index": LESEN + [
        ("Mail öffnen", "Enter", "exec display-message"),
        ("Unterhaltung ein-/ausklappen", "za", "exec collapse-thread"),
        ("Alle Tasten anzeigen", "?", "exec help"),
        ("NeoMutt beenden", "q", "exec quit"),
    ],
    "pager": LESEN + [
        ("Nächste Mail", "", "exec next-entry"),
        ("Vorige Mail", "", "exec previous-entry"),
        ("Zurück zur Liste", "q", "exec exit"),
        ("Alle Tasten anzeigen", "?", "exec help"),
    ],
    "compose": [
        ("Senden", "y", "exec send-message"),
        ("Anhang hinzufügen", "a", "exec attach-file"),
        ("Empfänger (An) ändern", "t", "exec edit-to"),
        ("Kopie (Cc) ändern", "c", "exec edit-cc"),
        ("Betreff ändern", "s", "exec edit-subject"),
        ("Text bearbeiten", "e", "exec edit-message"),
        ("Als Entwurf speichern", "P", "exec postpone-message"),
        ("Verwerfen", "q", "exec exit"),
        ("Alle Tasten anzeigen", "?", "exec help"),
    ],
    "attach": [
        ("Öffnen", "Enter", "exec view-attach"),
        ("Speichern", "s", "exec save-entry"),
        ("Kalendereinladung in Google Kalender", "Strg+G", 'push "\\cg"'),
        ("Zurück", "q", "exec exit"),
        ("Alle Tasten anzeigen", "?", "exec help"),
    ],
}


def zeile(bezeichnung: str, taste: str) -> str:
    return f"{bezeichnung}   ·   {taste}" if taste else bezeichnung


def main() -> int:
    befehle = BEFEHLE.get(sys.argv[1] if len(sys.argv) > 1 else "", BEFEHLE["index"])
    zeilen = {zeile(b, t): c for b, t, c in befehle}
    try:
        p = subprocess.run(["fuzzel", "--dmenu", "--prompt", "Mail › ", "--width", "45",
                            "--lines", str(min(len(zeilen), 20))],
                           input="\n".join(zeilen) + "\n", capture_output=True, text=True, timeout=300)
    except (OSError, subprocess.TimeoutExpired):
        return 0
    befehl = zeilen.get(p.stdout.strip("\n"))
    if befehl:
        print(befehl)
    return 0


if __name__ == "__main__":
    sys.exit(main())
