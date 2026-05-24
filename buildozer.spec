[app]
title = My First App
package.name = myfirstapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp3
version = 0.1
requirements = python3,kivy==2.3.1,kivymd==1.2.0
icon = mira.png
orientation = portrait
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25.1.8937393

[buildozer]
log_level = 2
warn_on_root = 1
