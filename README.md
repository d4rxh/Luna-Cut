<p align="center">
  <img src="assets/luna-cut-logo.png" alt="Luna-Cut Logo" width="160" style="border-radius: 28px;" />
</p>

<h1 align="center">Luna-Cut</h1>

<p align="center">
  <strong>The Free, Open-Source, GPU-Accelerated Video & Motion Editor</strong><br>
  <em>Local-first • Keyframe Bezier Curves • Multi-Track Timeline • Zero Watermark • 100% Private</em>
</p>

<p align="center">
  <a href="https://github.com/d4rxh/Luna-Cut/releases"><img src="https://img.shields.io/github/v/release/d4rxh/Luna-Cut?style=flat&color=D71920" alt="Release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-AGPL%20v3-red.svg" alt="License: AGPL-3.0"></a>
  <a href="https://github.com/d4rxh/Luna-Cut"><img src="https://img.shields.io/badge/Platform-Android%20%7C%20Linux%20%7C%20Windows%20%7C%20macOS-blue.svg" alt="Platforms"></a>
</p>

---

## 🌟 What is Luna-Cut?

**Luna-Cut** is a next-generation, local-first motion and video editor built with a native Rust GPU engine (Vulkan / OpenGL / Skia) and a modern OLED-optimized mobile interface inspired by professional motion design workflows.

Designed as a privacy-friendly, pro-grade alternative to subscription-based editors (like CapCut & Alight Motion), **Luna-Cut** runs entirely on your device with no cloud uploads, no watermarks, and no mandatory accounts.

---

### ✨ Core Features

- 🎞️ **Multi-Track Timeline**: Layer video, audio, text, and shape elements with millisecond precision and smooth 60/120 FPS scrubbing.
- ◆ **Keyframe Motion Graphics**: Animate Position, Scale, Rotation, and Opacity with diamond keyframe markers.
- 📈 **Interactive Bezier Curve Editor**: Speed and value curves with draggable tangent handles (Easy Ease, Ease In, Ease Out, Custom velocity).
- ⚡ **GPU Compositor Engine**: Hardware-accelerated real-time playback powered by Vulkan, OpenGL ES, and Skia.
- 🗣️ **Local AI Auto-Captions**: Offline Whisper model integration for automatic subtitles without sending footage to any cloud server.
- 🧍 **Offline Background Cutout**: Remove backgrounds and isolate subjects locally.
- 🚫 **Zero Watermarks & Zero Paywalls**: 100% free and open-source under AGPLv3.

---

## 📱 Mobile Architecture

Luna-Cut provides two frontends:
1. **Jetpack Compose Native Android**: Pure Kotlin + Jetpack Compose with Material 3 OLED Dark styling, interacting with the Rust engine through UniFFI.
2. **Slint Cross-Platform UI**: Reactive, GPU-accelerated declarative UI (`ui/phone/`) for high-performance rendering.

---

## 🏗️ Building Luna-Cut

### Android Native Build:
```bash
cd android-native
./gradlew assembleRelease
```

### Desktop Build (Rust + Cargo):
```bash
cd src
cargo build --release
```

---

## 📜 License
Licensed under the [GNU Affero General Public License v3.0 (AGPL-3.0)](LICENSE).
