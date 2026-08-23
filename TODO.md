# TODO

Tracked on the [kanban board](https://github.com/users/craigrouse/projects/3/views/1) — this file is the quick mirror; the board is the source of truth.

## Now
- [ ] Verify the 2026-08-23 free-session credit lands in the Octopus account (~15.1 kWh, cap guard fired at 15.0)
- [ ] Watch the first automated free session end-to-end (pre-dump → fill → cap guard → restore)
- [ ] Test the new window controls (lovelace/solar + Whole House → Energy) and the repaired manual force import
- [ ] Add the margin sensors (`sensor.grid_margin_today` + daily meters) to a dashboard
- [ ] Test "Upstairs: Auto-Off Left-On Lights" (Jade-leaves weekday rule + 30-min daylight rule)
- [ ] Delete "Holiday: Hot Water (25–29 Aug)" one-shot automation after returning

## Review queue (2026-08-23 automation audit)
- [ ] Delete broken automation "Kitchen: Turn Off Lights Warning on Off-Peak Start" (targets deleted dining spots, already disabled)
- [ ] Review "System: Update Sony TV State (2s Interval)" — heaviest automation in the house, likely obsolete
- [ ] Fix or delete "Notify Jade if Craig in Meeting on Arrival" — references dead MuteSync sensors
- [ ] Disable "Lounge: Christmas Tree Toggle" until December
- [ ] Review the Octopus timestamp-cache cluster for redundancy (automation_108, set_power_hour_start, saving_sessions_set_timestamps, store_3_minutes_before_slot_ends, set_octopus_end_time_from_sensor)
- [ ] Tesla Sunday 100% charge automation is OFF — deliberate? (LFP calibration reminder)
- [ ] Check wall switches: Ava's and Mya's ceiling lights show unavailable in HA
- [ ] Remove the lounge_ceiling YAML group block from config + restart, then rename light.lounge_ceiling_2

## Next
- [ ] First paid Saving Session of the season: verify the new calendar-triggered controller + paid-session gate end-to-end
- [ ] Margin tracker: sanity-check `sensor.grid_margin_today` against the Octopus bill after a full week
- [ ] Update rate constants (6.9p/30.4p/12p) in the margin sensor whenever the tariff changes

## September — Heating Scheduler (the big one)
- [ ] Design "Heating Scheduler" for the Altherma mirroring the Daily Scheduler pattern (single writer, window template, same freeze-flag guards)
- [ ] Preheat house + DHW in the 23:30–05:30 window and dispatch slots; never run the heat pump at day rate
- [ ] Use the existing COP tracking helpers to decide heat-pump vs immersion and preheat depth
- [ ] Retire/replace the old disabled seasonal on/off automations (heat pump at off-peak, Altherma morning, off-above-55)

## Watching / someday
- [ ] Renault 5 V2G — Mobilize UK launch (structural upgrade: ~tripled cycleable capacity); revisit charger investment when available
- [ ] Monthly true-zero battery drain for BMS calibration (evening dump buffer 0 once a month)
- [ ] Decide fate of Solar Arbitrage Mode (EV-neutral with DC-coupled solar; kept for now)

## Decided / not doing
- Agile Outgoing export — not interested; prefer the fixed 12p margin at any time of day
- Pre-filling the battery at peak rate before paid Saving Sessions — rarely worth it; dump whatever is in the battery
- Holiday mode gating energy automations — removed 2026-08-23; arbitrage runs on holiday by design
