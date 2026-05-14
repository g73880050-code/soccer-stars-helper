# ============================================================================
# Soccer Stars Analyzer — buildozer.spec  (clean / bulletproof build)
# ============================================================================
#
# Pinned stack
# ------------
#   Android API       33   (Android 13)
#   Build-Tools       33.0.0  ← explicitly locked; blocks auto-upgrade to 37
#   NDK               r25b (25.1.8937393)
#   Min API           26   (Android 8.0 — TYPE_APPLICATION_OVERLAY minimum)
#   Kivy              2.3.0
#   Python            3.11
#
# Build commands
# --------------
#   buildozer android debug                  # debug APK
#   buildozer android debug deploy run       # build + install + launch
#   buildozer android release                # production APK (needs keystore)
#
# Clean build
# -----------
#   buildozer android clean
#   rm -rf .buildozer bin
# ============================================================================

[app]

# ----------------------------------------------------------------------------
# Identity
# ----------------------------------------------------------------------------
title          = Soccer Stars Analyzer
package.name   = soccerstarsanalyzer
package.domain = com.soccerstars

# ----------------------------------------------------------------------------
# Source
# ----------------------------------------------------------------------------
source.dir          = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,ttf
source.main         = main.py

# Background capture service (foreground type — required for MediaProjection)
services = SoccerStarsService:service/main.py:foreground

# ----------------------------------------------------------------------------
# Version
# ----------------------------------------------------------------------------
version = 1.2.0

# ----------------------------------------------------------------------------
# Assets  (uncomment once icon / presplash are ready)
# ----------------------------------------------------------------------------
#icon.filename      = %(source.dir)s/data/icon.png        # 512×512 px
#presplash.filename = %(source.dir)s/data/presplash.png   # 1080×1920 px

# ----------------------------------------------------------------------------
# Requirements
# ----------------------------------------------------------------------------
# python-for-android recipe names (NOT pip package names):
#   python3    — CPython 3.11 runtime
#   kivy       — UI framework
#   numpy      — array / matrix math
#   opencv     — computer vision (p4a recipe builds libopencv_java4.so)
#   pyjnius    — Python ↔ Java bridge
#   android    — python-for-android helpers (permissions, activity, service)
requirements = python3==3.11.9,kivy==2.3.0,numpy,opencv,pyjnius,android

# ----------------------------------------------------------------------------
# Orientation / display
# ----------------------------------------------------------------------------
orientation = portrait
fullscreen   = 0

# ----------------------------------------------------------------------------
# Android SDK / NDK  ← THE VERSION-LOCK SECTION
#
# android.build_tools_version is the critical pin.
# Without it, p4a / Gradle selects the highest installed version which is
# often 37.x on modern runners, causing the 'aidl not found' failure.
# ----------------------------------------------------------------------------
android.api               = 33
android.minapi            = 26
android.ndk_api           = 26
android.build_tools_version = 33.0.0

# Leave sdk_path / ndk_path blank for local builds — Buildozer downloads them.
# In GitHub Actions the CI workflow sets ANDROIDSDK / ANDROIDNDK env vars
# which override these blanks automatically.
android.sdk_path =
android.ndk_path =

# Architecture — arm64 covers Honor 400; add armeabi-v7a for older devices
android.archs = arm64-v8a

# ----------------------------------------------------------------------------
# Gradle / AndroidX
# ----------------------------------------------------------------------------
android.gradle_dependencies = androidx.core:core:1.13.1
android.enable_androidx      = True

# Prevent Gradle from silently upgrading SDK components during the build.
# This is the Gradle-side complement to the PATH/env pinning in the CI.
android.gradle_repositories = google(), mavenCentral()

# ----------------------------------------------------------------------------
# PERMISSIONS
# ----------------------------------------------------------------------------
android.permissions =
    android.permission.SYSTEM_ALERT_WINDOW,
    android.permission.FOREGROUND_SERVICE,
    android.permission.FOREGROUND_SERVICE_MEDIA_PROJECTION,
    android.permission.WAKE_LOCK,
    android.permission.INTERNET,
    android.permission.ACCESS_NETWORK_STATE,
    android.permission.VIBRATE

# ----------------------------------------------------------------------------
# AndroidManifest extras
# ----------------------------------------------------------------------------
# Required for HTTP on Android 9+
android.extra_manifest_application_arguments =
    android:usesCleartextTraffic="true"

android.manifest.intent_filters =
android.manifest.meta_data     =

# ----------------------------------------------------------------------------
# python-for-android
# ----------------------------------------------------------------------------
# Use 'develop' branch for Kivy 2.3 + OpenCV recipe compatibility
p4a.branch = develop

# Uncomment to use a local p4a clone (useful for recipe patching):
# p4a.source_dir = /path/to/python-for-android

# Uncomment to add local custom recipes (e.g. patched opencv):
# p4a.local_recipes = ./p4a_recipes

# ----------------------------------------------------------------------------
# Build directories
# ----------------------------------------------------------------------------
[buildozer]
build_dir = .buildozer
bin_dir   = ./bin
log_level = 2
