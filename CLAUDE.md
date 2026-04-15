# CLAUDE.md — arkive.ninja (VDO.Ninja)

This file provides context for AI assistants working in this repository.

## Project Overview

**arkive.ninja** is a deployment/fork of [VDO.Ninja](https://vdo.ninja) (formerly OBS.Ninja), a peer-to-peer WebRTC video streaming platform. It enables content creators to pull remote cameras into OBS Studio or other broadcast software with low latency, no video server required in ~95% of cases.

This repository contains **only the browser-side web client** — HTML, CSS, and JavaScript. There is no build step; all files are served directly as static assets over HTTPS.

## Repository Structure

```
/
├── index.html             # Main landing page / director interface
├── room.html              # Primary video room (guest view)
├── meet.html              # Google Meet-style multi-party room (~65KB)
├── mixer.html             # Audio/video mixer interface (~146KB)
├── comms.html             # Communications/chat interface (~77KB)
├── iframe.html            # IFRAME API host page
├── whip.html              # WHIP ingest protocol page
├── whep.html              # WHEP egress protocol page
├── electron.html          # Electron Capture integration
├── dock.html              # OBS dock widget
├── speedtest.html         # Network speed test
├── monitor.html           # Connection monitor
├── midi.html              # MIDI control interface
├── remotemidi.html        # Remote MIDI interface
├── teleprompter.html      # Teleprompter tool
├── convert.html           # Stream conversion tool
├── colorspace.html        # Color space testing
├── codecs.html            # Codec support checker
├── supports.html          # Browser feature support checker
├── check.html             # WebRTC connectivity checker
├── icetest.html           # ICE server test
├── mictest.html           # Microphone test
├── devices.html           # Device enumeration
├── cloudflare.html        # Cloudflare Stream integration
├── esports.html           # Esports overlay integration
├── zoom.html              # Zoom integration page
├── results.html           # Results / stats display
├── publish.html           # Publishing interface
├── popout.html            # Popout video window
├── 360.html               # 360-degree video viewer
│
├── main.js                # Main application logic (~247KB)
├── webrtc.js              # WebRTC peer connection management (~481KB)
├── lib.js                 # Bundled third-party libraries (~1.4MB)
├── insertableStreamWorker.js  # Web Worker for Insertable Streams (E2E encryption)
├── iframe-examples.js     # IFRAME API usage examples
├── serviceWorker.js       # PWA service worker
│
├── main.css               # Primary stylesheet (~112KB)
├── iframe.css             # IFRAME-specific styles
├── stats.css              # Stats overlay styles
├── speedtest.css          # Speed test styles
├── supports.css           # Browser support page styles
├── devices.css            # Devices page styles
├── minidirector.css       # Mini director view styles
│
├── translations/          # i18n JSON translation files
│   ├── en.json            # English (source of truth)
│   ├── blank.json         # Template for new translations
│   ├── cn.json, de.json, es.json, fr.json, ...
│   ├── translate.js       # Translation helper script
│   └── makepig.js         # Pig Latin generator (for testing)
│
├── design-system/         # UI design assets
│   ├── arkive.ninja/      # Current design specs
│   └── arkive.ninja-(vdo.ninja)/  # VDO.Ninja branded design specs
│
├── thirdparty/            # Third-party libraries (served locally)
├── filters/               # Video filter assets
├── media/                 # Static media assets
├── examples/              # Example integration code
├── lineawesome/           # Line Awesome icon font
│
├── .claude/               # Claude Code configuration
│   ├── settings.json      # Claude Code tool permissions
│   └── hooks/             # Claude Code lifecycle hooks
├── .agents/               # AI agent configuration
├── .github/
│   ├── workflows/
│   │   ├── update_translations.yml        # Auto-generate translation files
│   │   └── update-advanced-settings-toc.yml  # Update settings table of contents
│   ├── ci-generateTranslations.js         # Translation generation script
│   └── FUNDING.yml        # GitHub Sponsors config
│
├── turnserver.conf        # Sample coturn TURN server config
├── turnserver.md          # TURN server setup guide
├── install.md             # Self-hosting deployment guide
├── IFRAME.md              # IFRAME API documentation
├── CONTRIBUTING.md        # Contribution policy and CLA info
├── LICENCE.md             # Custom "mostly open-source" license
└── AGPLv3.md              # AGPLv3 license text
```

## Technology Stack

- **Pure static web**: HTML5, CSS3, Vanilla JavaScript (ES modules/modern JS)
- **WebRTC**: Native browser WebRTC APIs for peer-to-peer video/audio
- **No build system**: No webpack, no npm, no compilation — files are served as-is
- **Signaling**: WebSocket-based handshake server (external, see install.md)
- **TURN**: Optional coturn server for NAT traversal (~5% of users need it)
- **STUN**: Public STUN servers for peer discovery

## Development Workflow

### Serving Locally

Because WebRTC requires HTTPS (or localhost), you need a local HTTPS server:

```bash
# Python simple server (HTTP only, works on localhost)
python3 -m http.server 8080

# For HTTPS (required for camera/mic on non-localhost):
# Use a local proxy like caddy, nginx, or ngrok
```

Alternatively, open files directly via `https://vdo.ninja` and point to your local version via URL parameters for testing.

### No Build Step

- Edit HTML/CSS/JS files directly — no compilation needed
- Changes are immediately reflected on browser refresh
- `node_modules/` is gitignored; there are no npm dependencies to install for the client

### Branch Strategy

- **`develop`** — active development branch; aligns with `vdo.ninja/beta/` or `/alpha/`
- **Release branches** — each release version gets its own branch (e.g., `v23`, `v24`)
- **Feature branches** — prefix with `claude/` for AI-generated changes
- The production deployment at `vdo.ninja` is updated infrequently to avoid disrupting live productions

### CI / Automation

- **Translation updates**: When `translations/en.json` changes, the workflow `update_translations.yml` uses `.github/ci-generateTranslations.js` to propagate new keys to all other language files (filling missing keys with English fallback)
- **Settings TOC**: `update-advanced-settings-toc.yml` auto-updates the advanced settings table of contents when relevant files change

## Key Files to Understand

### `webrtc.js` (~481KB)
The core WebRTC engine. Handles:
- Peer connection lifecycle (offer/answer/ICE)
- Media stream acquisition (camera, screen, audio)
- Codec negotiation and bitrate control
- TURN/STUN configuration
- Insertable Streams (E2E encryption)
- Data channels for chat/control messages

### `main.js` (~247KB)
Application logic layer. Handles:
- URL parameter parsing (VDO.Ninja is heavily URL-param driven)
- UI state management
- Director controls (room management)
- Scene management for OBS integration
- Feature flags and session configuration

### `lib.js` (~1.4MB)
Bundled third-party dependencies (minified). Do not edit directly.

### `index.html` (~172KB)
The main app page. Contains significant inline JavaScript for initialization. This is the entry point for most users.

### `room.html` (~170KB)
The guest/publisher room. Used when joining a session as a camera source.

### `translations/en.json`
The **source of truth** for all UI strings. When adding new UI text:
1. Add the key/value to `en.json`
2. The CI workflow will propagate it to other language files
3. Never edit other language files directly for keys that should be translated — the CI handles it

## Conventions

### URL Parameters
VDO.Ninja is heavily driven by URL parameters (e.g., `?room=myroom&push=cameraID&quality=2`). When adding features, follow the existing pattern of reading params from `URLSearchParams` in `main.js`.

### No Frameworks
The codebase uses vanilla JavaScript. Do **not** introduce React, Vue, or other SPA frameworks. Keep additions consistent with the existing vanilla JS style.

### Global State
Much of the app state lives in module-level variables in `main.js` and `webrtc.js`. Be aware of global variable dependencies when making changes.

### CSS
Styles are organized per-page (e.g., `speedtest.css` for `speedtest.html`). Global styles live in `main.css`. Avoid inline styles except for dynamic values.

### i18n
All user-facing strings should use the translation system. Reference existing patterns in `translations/translate.js` for how strings are loaded and applied.

## Self-Hosting Notes

See `install.md` for full deployment instructions. Key requirements:
- HTTPS (mandatory for WebRTC camera/mic access in browsers)
- No server-side processing needed for the web client itself
- Optional: TURN server (`turnserver.md`) for users behind strict NAT/firewalls
- Optional: Custom signaling/handshake server (see linked websocket_server repo)

## Licensing & Contributions

- License: Custom "mostly open-source" — see `LICENCE.md`
- Contributors **must sign the CLA** before their PRs are merged (see `CONTRIBUTING.md`)
- A CLA Assistant bot will prompt contributors automatically on new PRs
- The CLA is perpetual once signed — no need to re-sign for future contributions
- Grant is to Steve Seguin (project creator)

## What NOT to Do

- Do not add a build system or npm dependencies to the main client
- Do not edit `lib.js` directly (it is a bundled artifact)
- Do not commit `turn-credentials.php` (gitignored — contains secrets)
- Do not commit `.vscode/` settings
- Do not break URL parameter backwards compatibility — existing links must keep working
- Do not update the production `vdo.ninja` hosted service without explicit permission
