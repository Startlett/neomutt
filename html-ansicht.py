#!/usr/bin/env python3
"""HTML-Fassung der aktuellen Mail im abgeschotteten Browser zeigen
(Palette: „HTML-Ansicht im Browser“, <pipe-message>; 27.10.2026).

Nimmt den text/html-Teil der Mail (stdin), bettet eingebettete Bilder
(cid:) als data:-Adressen ein und öffnet ihn wie mailcap im eigenen
qutebrowser-Profil (qutebrowser-html-view.py: JavaScript aus, privat).
Die Datei liegt nur für den eigenen Benutzer lesbar in $XDG_RUNTIME_DIR.
"""

import base64
import email
import email.policy
import os
import subprocess
import sys
import tempfile
from pathlib import Path

PROFIL = Path.home() / ".local/share/qutebrowser-mail-html"
KONFIG = Path.home() / ".config/neomutt/qutebrowser-html-view.py"


def melde(text: str) -> None:
    subprocess.run(["notify-send", "-a", "Mail", "HTML-Ansicht", text], check=False)


def main() -> int:
    nachricht = email.message_from_bytes(sys.stdin.buffer.read(), policy=email.policy.default)
    teil = nachricht.get_body(preferencelist=("html",))
    if teil is None:
        melde("Diese Mail hat keine HTML-Fassung.")
        return 0
    html = teil.get_content()
    for anhang in nachricht.walk():
        cid = (anhang.get("Content-ID") or "").strip("<>")
        if cid and anhang.get_content_maintype() == "image":
            daten = base64.b64encode(anhang.get_payload(decode=True) or b"").decode()
            html = html.replace(f"cid:{cid}", f"data:{anhang.get_content_type()};base64,{daten}")
    ordner = Path(os.environ.get("XDG_RUNTIME_DIR", tempfile.gettempdir())) / "neomutt-html"
    ordner.mkdir(mode=0o700, exist_ok=True)
    fd, pfad = tempfile.mkstemp(suffix=".html", dir=ordner)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(html)
    subprocess.Popen(["qutebrowser", "-B", str(PROFIL), "-C", str(KONFIG), "--desktop-file-name", "link-popup",
                      "--target", "window", pfad],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
