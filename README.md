# Home Assistant Config — Rouse House Energy System

Snapshot of the important Home Assistant configuration for the home energy setup, exported from the live instance. Automations live in [`automations/`](automations/) as YAML (converted from the HA config API's JSON; the `alias` matches the automation in HA). Helpers are documented in [`docs/helpers.md`](docs/helpers.md). Resume point after the Sept 2026 gateway-stall week: [`docs/handoff-2026-09-04.md`](docs/handoff-2026-09-04.md). Open work is tracked on the [kanban board](https://github.com/users/craigrouse/projects/3/views/1) and mirrored in [`TODO.md`](TODO.md).

## The setup

- 2× Tesla Powerwall 3 — 27 kWh usable, DC-coupled 4.74 kWp solar (solar→battery is effectively lossless; conversion cost only on AC import/export). Combined grid-charge limit 10 kW, export ~14 kW, site limit ~22 kW (100A).
- Octopus Intelligent Go — 6.9p off-peak 23:30–05:30 (whole house also 6.9p during any car dispatch), ~30.4p day rate, 12p flat export.
- Tesla Model Y + Renault 5, sharing one Tesla Wall Connector.
- Daikin Altherma heat pump (space + DHW with immersion booster).
- Control plane: Teslemetry (`teslemetry.time_of_use` fake-tariff pushes are how the Powerwall is steered), local Powerwall gateway integration (fast sensors), BottlecapDave Octopus Energy integration (rates, dispatches, Octoplus events/calendars).

## Architecture

One writer, event controllers that delegate, independent watchdogs.

```
                    binary_sensor.octopus_paid_saving_session_active   (calendar on AND octopoints/kWh > 0)
                    binary_sensor.octopus_free_session_active          (joined event window with octopoints/kWh == 0)
                                     │ gates everything
        ┌────────────────────────────┼──────────────────────────────┐
        ▼                            ▼                              ▼
Daily Scheduler (single      Saving Session Controller       Power Hour Controller
TOU writer; evening dump,    (PAID sessions: export           (FREE sessions: pre-dump via
night dump 01:30→empty,      spike TOU, kickstart             Free Session Pre-Dump, fill at
refill, day mode, car        nudge, soc_low guard)            reserve 100, immersion boost,
slot handling)                                                dynamic free-window TOU,
        ▲                                                     smart-charge pause/resume)
        │ automation.trigger with skip_condition: false
        ├── Intelligent Slot delegate (cancels manual export, re-runs scheduler)
        ├── Grid Charge Watchdog (battery charging >2 kW AND grid import >1 kW at peak)
        ├── Grid Export Watchdog (export configured but stuck at 0 kW → gateway nudge)
        ├── Grid Fill Watchdog (fill posture pushed but battery not charging >3 min → mode toggle + re-run)
        └── Solar Arbitrage (SoC 97↔80 hysteresis, 10:00–16:00)

Manual layer: Manual Export/Import Controllers (dashboard buttons + duration sliders,
0.25h steps) + Manual Window Scheduler ("export/import between" times, one-shot arm).

Guards: input_boolean.power_hour_active freezes the scheduler and watchdogs during any
session or manual TOU work. Free Session Import Cap Guard sheds all load at 15 kWh
imported (16 kWh fair-use cap). Kill switch for auto pre-dump:
input_boolean.free_session_auto_dump.

Verification: daily utility meters (grid import split cheap/peak by live rate, grid
export) + sensor.grid_margin_today (export×12p − cheap×6.9p − peak×30.4p).
```

## Conventions / hard-won rules

- **Tariff first, mode last, then verify.** Every TOU writer pushes the tariff, waits 15 s, then sets grid switch → reserve → export → operation mode. Since gateway firmware 26.2 the Powerwall checks the tariff before honouring reserve/mode changes (2026-09-02: three stalls in one evening with the old tariff-last order). Never trust a pushed posture: the Export/Fill watchdogs and the controllers' kickstarts test GRID power (export) or BATTERY power (fill) after 3 min and toggle `self_consumption → 45 s → autonomous` to make the gateway re-plan. Battery-power alone is NOT an export test (house load hides a stalled export). Stuck tests read the LOCAL gateway sensors (`sensor.powerwall_192_168_1_182_site_power` / `_battery_power`, 30 s) - the Teslemetry grid/battery sensors are cloud-polled and lag ~1 min (2026-09-03: a stale reading toggled the mode against an export that had already started). Paid sessions start 5 min early (calendar offset -5m, TOU spike opens at T-5) so the gateway's ~3-4 min reaction time lands before the session.
- **Never call `automation.trigger` on the Daily Scheduler without `skip_condition: false`** — the default bypasses its session/manual guards (this class of bug clobbered session tariffs for months before being fixed on 2026-08-23).
- **Only the Daily Scheduler and the session/manual controllers push TOU tariffs** — one writer per situation, gated so exactly one is in charge at a time.
- **Session type is decided by `octopoints_per_kwh`** on the joined event (0 = free electricity, >0 = paid saving session). Never by calendar message text — free and paid sessions both appear on both Octoplus calendars with the message "Octopus Energy Saving Session".
- **`water_heater.altherma` does not support `set_temperature`** (operation-mode + on/off only). Use `water_heater.set_operation_mode` (`performance` engages the immersion booster), always with `continue_on_error: true` and ordered after the money-path actions.
- **Never export while a car dispatch is active** — the meter nets instantaneously, so the export silently fills the car from the battery instead.
- `sensor.rouse_house_pw3_grid_power` is positive on import. `sensor.powerwall_192_168_1_182_site_import` (local gateway, kWh, ~30s updates) is the fast import meter used for the cap guard.
- Free-session billing: the tariff feed never shows 0p — the free hour arrives afterwards as an Octoplus account credit. Verify credits against the cap-guard notification totals.

## Regenerating this export

Configs were pulled via the HA config API (each file is the exact automation config). To refresh, pull the automation config from HA and re-run `tools/json2yaml.py` on the JSON, or just paste updated YAML directly.
