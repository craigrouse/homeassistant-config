# Helpers (energy system)

Created via the HA UI/config flow (not YAML). Grouped by role. All carry the `powerwall` label unless noted.

## Session detection (template binary sensors — the source of truth)
| Entity | Definition |
|---|---|
| `binary_sensor.octopus_paid_saving_session_active` | saving-sessions calendar is `on` AND the currently-active joined event has `octopoints_per_kwh > 0` |
| `binary_sensor.octopus_free_session_active` | the currently-active joined event has `octopoints_per_kwh == 0` |

Both iterate `joined_events` on `event.octopus_energy_a_dbae4963_octoplus_saving_session_events`.

## Free sessions
| Entity | Type | Purpose |
|---|---|---|
| `input_boolean.free_session_auto_dump` | toggle | Kill switch for the automatic pre-session dump |
| `input_boolean.power_hour_active` | toggle | Global freeze flag: blocks the Daily Scheduler, watchdogs, and slot delegate while any session/manual TOU is in charge |
| `input_number.free_session_import_baseline` | number (kWh) | Site-import meter reading stamped at session start (by Pre-Dump and Power Hour) |
| `input_number.free_session_import_cap` | number (5–16 kWh) | Shed threshold for the 16 kWh fair-use cap; 15.0 leaves ~1 kWh sensor-lag margin |
| `input_datetime.20th_oct_12pm` / `input_datetime.20th_oct_1pm` / `input_datetime.3_mins_before_power_hour_end` | datetime | Legacy names, kept because three dashboards display them. Auto-stamped by Power Hour at session start (start / end / end−3min); also act as manual-fire triggers |

## Saving sessions
| Entity | Type | Purpose |
|---|---|---|
| `input_datetime.octopus_saving_session_next_start` / `_end` | datetime | Next joined session window; maintained by the joiner + set-time automations; consumed by both session controllers' TOU templates |

## Manual control
| Entity | Type | Purpose |
|---|---|---|
| `input_boolean.manual_export_active` | toggle | The dashboard force-export button (drives Manual Export Controller) |
| `input_boolean.start_manual_force_import` | toggle | The dashboard force-import button (drives Manual Import Controller) |
| `input_number.manual_export_duration_hours` / `manual_import_duration_hours` | slider 0.25–6h, 0.25 steps | Duration for the manual controllers (import one created 2026-08-23 — it never existed; import always defaulted to 1h) |
| `timer.manual_export_countdown` / `manual_import_countdown` | timer | Auto-stop for manual runs |
| `input_datetime.manual_export_window_from` / `_until` (+ import pair) | time | "Export/import between" window times |
| `input_boolean.manual_export_window_armed` / `manual_import_window_armed` | toggle | One-shot arm for the window scheduler |

## Verification / margin
| Entity | Type | Purpose |
|---|---|---|
| `select.daily_grid_import` + `sensor.rouse_house_pw3_daily_grid_import_cheap` / `_peak` | utility_meter (daily, tariffs) | Grid import split by rate band; tariff flipped by the Tariff Switcher automation at the 10p threshold |
| `sensor.rouse_house_pw3_daily_grid_export` | utility_meter (daily) | Grid export today |
| `sensor.grid_margin_today` | template sensor (£) | export×0.12 − cheap×0.069 − peak×0.303714 — **rate constants; update when the tariff changes** |

## Powerwall health (pre-existing)
`input_number.powerwall_3_measured_full_capacity`, `input_number.powerwall_target_percentage`, plus the Powerwall A/B Health and degradation template sensors.

## Other pre-existing energy helpers
`input_datetime.time_to_start_exporting` (evening dump start, computed nightly at 20:40), `input_datetime.octopus_off_peak_start`, `input_boolean.holiday_mode`, `input_boolean.home_for_morning`, `input_datetime.tesla_shadow_ready_by`, `input_number.tesla_desired_soc`, COP tracking helpers (heating/DHW power in/out integrations + statistics).
