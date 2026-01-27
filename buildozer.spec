[app]
title = Deal Exchange Pro
package.name = dealexchangepro
package.domain = org.rizwan
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# Requirements
requirements = python3, flet, requests

# Permissions (Adding everything you need)
android.permissions = INTERNET, CAMERA, RECORD_AUDIO, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, ACCESS_NETWORK_STATE

# Flet Specific Settings (Very Important)
android.entrypoint = main
p4a.bootstrap = webview
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b

# Orientation and Fullscreen
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
