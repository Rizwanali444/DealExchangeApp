[app]
title = Deal Exchange Pro

package.name = dealexchangepro
package.domain = org.rizwan

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0


# ---------------- REQUIREMENTS ----------------
requirements = python,flet,requests

# ---------------- ANDROID ----------------
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 23b

android.permissions = INTERNET, CAMERA, RECORD_AUDIO, ACCESS_NETWORK_STATE

# Flet / Python settings
android.entrypoint = org.kivy.android.PythonActivity
p4a.bootstrap = sdl2

# ---------------- UI ----------------
orientation = portrait
fullscreen = 0


[buildozer]
log_level = 2
warn_on_root = 1
