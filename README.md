# NeoMutt-Konfiguration

Gemeinsame Konfiguration für Rumpelkiste und Schleppi (`~/.config/neomutt`).
Gmail per IMAP: Abgleich mit mbsync, Versand mit msmtp bzw. `smtp_url`,
Suche mit notmuch. Passwörter kommen aus pass, nie aus diesen Dateien.

- `neomuttrc` – Konto, Ordner, Ansicht, bindet die `*.rc` ein
- `palette.py` / `palette.rc` – Befehlspalette auf der Leertaste (fuzzel)
- `plumber.rc` – F12 bzw. `$mod+i`: Mail an den Chaos-Plumber
  (`chaos-plumber/actions/mail-kontext`: Links, Bilder, Einladungen)
- `gcalcli.rc` / `gcal-import.sh` – Einladungen (.ics) in den Google-Kalender
- `notmuch.rc`, `urlscan.rc`, `kontakte.rc` (Adressen aus khard), `html-view.rc`, `mailcap`,
  `qutebrowser-html-view.py`, `colors.rc`
