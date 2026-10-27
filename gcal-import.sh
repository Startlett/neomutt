#!/bin/bash
# Kalendereinladung (.ics, auf stdin) per gcalcli in den Google-Kalender
# (gcalcli.rc, Strg+G bei den Anhängen).
#
# gcalcli nutzt die gespeicherte Anmeldung (~/.local/share/gcalcli/oauth),
# das Client-Secret braucht es nur beim ersten Anmelden – und das bekommt
# es dann über stdin, nie als Argument (Prozessliste):
#   gcal-import.sh --anmelden
set -euo pipefail

OAUTH=~/.local/share/gcalcli/oauth
KALENDER=oettel.nico@gmail.com

if [[ ${1:-} == --anmelden ]]; then
    # gcalcli fragt „Client Secret:“ per input() ab – erste Zeile von stdin
    pass show google/oauth-client-secret | head -n 1 | gcalcli init
    chmod 600 "$OAUTH"
    exit
fi

if [[ ! -s $OAUTH ]]; then
    echo "gcalcli ist auf $(uname -n) nicht angemeldet – einmal im Terminal:" >&2
    echo "  ~/.config/neomutt/gcal-import.sh --anmelden" >&2
    exit 1
fi
exec gcalcli import --calendar "$KALENDER" --default-reminders
