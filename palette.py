#!/usr/bin/env python3
"""Befehlspalette für NeoMutt: Leertaste bzw. Strg+I/Tab → fuzzel-Menü mit deutschen
Einträgen, Auswahl → NeoMutt führt den Befehl aus.

Aufruf aus palette.rc:  source '~/.config/neomutt/palette.py index|'
NeoMutt übernimmt, was das Skript ausgibt, als Konfigurationsbefehl
(„exec <funktion>“ bzw. „push <tasten>“). Abbrechen gibt nichts aus.

Hinter jedem Eintrag steht die Taste, falls es eine gibt – zum Lernen
nebenbei. Neue Einträge: Zeile in BEFEHLE ergänzen (Bezeichnung, Taste,
NeoMutt-Befehl).
"""

import os
import subprocess
import sys

# Gmail archivieren = in den Ordner Archive verschieben, ohne Rückfrage
# „anhängen?“ (confirm_append gilt nur für diesen einen Befehl)
ARCHIVIEREN = ('push "<enter-command>set confirm_append=no<enter><save-message>+Archive<enter>'
               '<enter-command>set confirm_append=yes<enter><sync-mailbox>"')
# Zurück in die Inbox (z. B. aus dem Papierkorb), ebenso sofort
IN_INBOX = ('push "<enter-command>set confirm_append=no<enter><save-message>+Inbox<enter>'
            '<enter-command>set confirm_append=yes<enter><sync-mailbox>"')
PAPIERKORB_OEFFNEN = 'push "<change-folder>+[Gmail]/Papierkorb<enter>"'
# Erst eigene Änderungen (Löschen, Archivieren) übernehmen, dann holen
ABRUFEN = 'push "<sync-mailbox><shell-escape>systemctl --user start mbsync.service<enter>"'

LESEN = [
    ("Antworten", "r", "exec reply"),
    ("Allen antworten", "", "exec group-reply"),
    ("Weiterleiten", "f", "exec forward-message"),
    ("HTML-Ansicht im Browser", "", 'push "<pipe-message>~/.config/neomutt/html-ansicht.py<enter>"'),
    ("Neue Mail schreiben", "m", "exec mail"),
    ("Archivieren", "", ARCHIVIEREN),
    ("In den Papierkorb", "dd", 'push "<delete-message><sync-mailbox>"'),
    ("Papierkorb öffnen (zurückholen)", "", PAPIERKORB_OEFFNEN),
    ("Zurück in die Inbox", "", IN_INBOX),
    ("Gelesen / ungelesen", "", "exec toggle-new"),
    ("Stern setzen / entfernen", "F", "exec flag-message"),
    ("Mehr mit dieser Mail (Links, Bilder, Einladung)", "$mod+i", 'push "<f12>"'),
    ("Links öffnen", "gu", 'push "gu"'),
    ("Anhänge ansehen / speichern", "v", "exec view-attachments"),
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
        # Mehrere Mails auf einmal (29.10.2026): auto_tag=yes in der neomuttrc –
        # sind Mails markiert, wirken Löschen/Archivieren/… auf alle markierten
        ("Diese Mail markieren / Markierung weg", "t", "exec tag-message"),
        ("Mehrere markieren (Muster: ~f Absender, ~s Betreff, ~d >30d, ~A alle)", "T", "exec tag-pattern"),
        ("Alle Markierungen aufheben", "Strg+T", 'push "<untag-pattern>~A<enter>"'),
        ("Unterhaltung ein-/ausklappen", "za", "exec collapse-thread"),
        ("Alle Tasten anzeigen", "?", "exec help"),
        ("NeoMutt beenden", "q", "exec quit"),
    ],
    "pager": LESEN + [
        ("Nächste Mail", "J", "exec next-entry"),
        ("Vorige Mail", "K", "exec previous-entry"),
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


PLUMB = os.path.expanduser("~/.local/bin/plumb")
# Die eigene Plumber-Regel für NeoMutt (öffnet diese Palette) nicht noch einmal
EIGENE = ("✉️ Mail-Menü",)


def plumber_angebote() -> list[str]:
    """Was der Chaos-Plumber für dieses Fenster anbietet ($mod+i), ohne die
    eigene Regel – z. B. „📋 Text an Schleppi: …“, „🔑 Anmelden (pass)“."""
    try:
        p = subprocess.run([PLUMB, "--angebote"], capture_output=True, text=True, timeout=4)
    except (OSError, subprocess.TimeoutExpired):
        return []
    return [z for z in p.stdout.splitlines() if z.strip() and z not in EIGENE]


def zeile(bezeichnung: str, taste: str) -> str:
    return f"{bezeichnung}   ·   {taste}" if taste else bezeichnung


def main() -> int:
    befehle = BEFEHLE.get(sys.argv[1] if len(sys.argv) > 1 else "", BEFEHLE["index"])
    zeilen = {zeile(b, t): c for b, t, c in befehle}
    # darunter die übrigen Plumber-Angebote (🔌), ausgeführt mit plumb -s --waehle
    plumber = {f"🔌 {name}": name for name in plumber_angebote()}
    try:
        p = subprocess.run(["fuzzel", "--dmenu", "--prompt", "Mail › ", "--width", "60",
                            "--lines", str(min(len(zeilen) + len(plumber), 22))],
                           input="\n".join([*zeilen, *plumber]) + "\n", capture_output=True, text=True, timeout=300)
    except (OSError, subprocess.TimeoutExpired):
        return 0
    wahl = p.stdout.strip("\n")
    if wahl in plumber:
        # Palette ist zu, NeoMutt wieder vorn: den Treffer wie bei $mod+i ausführen
        subprocess.Popen([PLUMB, "-s", "--waehle", plumber[wahl]], stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL, start_new_session=True)
        return 0
    befehl = zeilen.get(wahl)
    if befehl:
        print(befehl)
    return 0


if __name__ == "__main__":
    sys.exit(main())
