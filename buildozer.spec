[app]

# اسم التطبيق
title = Master Keyboard Pro

# اسم الحزمة
package.name = masterkeyboard

# اسم المجال
package.domain = dev.h40v

# الملف الرئيسي
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

# الإصدار
version = 2.0

# المتطلبات
requirements = python3,kivy==2.3.0

# الأيقونة (اختياري - ضع ملف icon.png)
#icon.filename = %(source.dir)s/icon.png

# التوجه: portrait أو landscape أو all
orientation = portrait

# الصلاحيات
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# الخدمات في الخلفية
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

# اسم التطبيق الكامل
fullscreen = 0

# معمارية المعالج
android.archs = arm64-v8a, armeabi-v7a

# Android API
android.api = 31
android.minapi = 21
android.ndk = 25b
android.sdk = 31

# التحقق من التوقيع
android.accept_sdk_license = True

# اللون الافتراضي
#android.presplash_color = #FFFFFF

# شاشة البداية (splash screen)
#presplash.filename = %(source.dir)s/presplash.png

# الثيم
#android.apptheme = @android:style/Theme.NoTitleBar

# قائمة البرامج المُنسّقة
android.add_jars = 

# إضافة مكتبات native
#android.add_libs_armeabi = libs/android/*.so
#android.add_libs_armeabi_v7a = libs/android-v7/*.so
#android.add_libs_arm64_v8a = libs/android-v8/*.so
#android.add_libs_x86 = libs/android-x86/*.so
#android.add_libs_mips = libs/android-mips/*.so

# تكوين التطبيق
#android.manifest.intent_filters = 

# نسخة OpenSSL
#android.gradle_dependencies = 

# وضع التطوير (للتصحيح)
#android.logcat_filters = *:S python:D

# نسخة Gradle
#android.gradle_version = 7.0

# استخدام androidx
android.enable_androidx = True

# Blacklist للملفات غير المطلوبة
android.blacklist_src = tests, bin, __pycache__

# Whitelist للملفات المطلوبة فقط
#android.whitelist = 

# تفعيل backup
android.allow_backup = True

# وضع الإطلاق (landscape/portrait/sensor)
#android.ouya.category = GAME
#android.ouya.icon.filename = %(source.dir)s/icon.png

# تعطيل تحسين bytecode
#android.no-byte-compile-python = 

[buildozer]

# ملف السجل
log_level = 2

# عدد المحاولات
warn_on_root = 1

# مجلد البناء
build_dir = ./.buildozer

# مجلد الحزمة
bin_dir = ./bin
