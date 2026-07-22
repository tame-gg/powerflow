# Powerflow (macOS 27)

Fork of [lzt1008/powerflow](https://github.com/lzt1008/powerflow) with fixes for **macOS 27 beta** (Darwin 27).

Powerflow monitors Mac power usage and charging status from the menu bar / tray.

## macOS 27 changes

Upstream `v0.2.2` can flash-quit on launch under macOS 27 because IORegistry / `AppleSmartBattery` plists changed shape. A bad `Result` transmute then turned parse failures into a SIGSEGV while panicking.

This fork:

- Fixes the IORegistry `Result` transmute / panic path (no more launch SIGSEGV)
- Makes IORegistry serde resilient with `serde(default)`
- Falls back to SMC-only metrics when IORegistry parse fails
- Restores mAh capacity fields from nested `BatteryData` when top-level keys are missing on macOS 27

Upstream issue/PR context: [lzt1008/powerflow#17](https://github.com/lzt1008/powerflow/issues/17), [PR #21](https://github.com/lzt1008/powerflow/pull/21).

## Build

Requires Rust, Node, and pnpm:

```bash
pnpm install
SQLX_OFFLINE=true pnpm tauri build
```

Debug binary:

```bash
SQLX_OFFLINE=true cargo build -p powerflow
```

## Install / run

If a release asset is attached, download it from [Releases](https://github.com/tame-gg/powerflow/releases), clear quarantine if needed, and open:

```bash
xattr -cr /Applications/Powerflow.app
open /Applications/Powerflow.app
```

## License

MIT — see [LICENSE](LICENSE). Original project by [lzt1008](https://github.com/lzt1008/powerflow).
