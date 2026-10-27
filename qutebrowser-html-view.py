# Isoliertes qutebrowser-Profil nur für die HTML-Mail-Ansicht (siehe
# mailcap, html-view.rc) - JS aus und immer Private Browsing, damit weder
# Tracking-/Exploit-Skripte aus einer Mail laufen noch Cookies/Verlauf
# über mehrere Mails hinweg landen. Bilder bleiben an, sonst sehen die
# meisten HTML-Mails (Newsletter etc.) kaputt aus - Tracking-Pixel sind
# der bewusst in Kauf genommene Rest-Trade-off.
config.load_autoconfig(False)

c.content.javascript.enabled = False
c.content.private_browsing = True
c.content.notifications.enabled = False
c.content.geolocation = False
c.content.desktop_capture = False
c.content.autoplay = False
c.content.plugins = False

# Kiosk-artig wie qutebrowser-webapps: pro Mail immer nur ein Fenster/Tab.
c.tabs.show = "never"
c.statusbar.show = "in-mode"
