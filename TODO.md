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
- [ ] Teslemetry PINNED at v6.0.3 (v6.0.15 needs a newer core than 2026.8.3 and broke every TOU push on 2026-08-23) - unpin after the next core update or a fixed release; the broken version is skipped in HA updates
- [x] First paid Saving Session of the season (2026-09-02 20:00): gate + triggers fired correctly; the gateway ignored the plan and the battery-power stuck test missed it → fixed (grid-power test, 45 s toggle, tariff-first ordering). Still to verify: the new re-assert loop against a real stall
- [ ] Powerwall firmware: HA shows 26.18.3 (Teslemetry device record, may be stale); 26.26.4 rolled to ~50% of PW3s from 2026-09-01. Check the version in the Tesla app - if it is 26.26.x, tonight's command stalls (2026-09-02) are probably the new major, same pattern as 26.2 in Feb
- [ ] Tesla app checks after the site re-creation: Powerwall → Vehicle Charging → Wall Connector Schedule (Rate Plan Charging) must be OFF, and no linked energy provider tariff (conflicts with API-pushed tariffs, alandtse/tesla#1171)
- [ ] Evening planner is now slot-aware (2026-09-04): verify the first evening Octopus inserts a mid-evening dispatch - expect dump / 6.9p refill during the slot / dump again, finishing by 23:30; check the netting rule held (no export while the car drew)
- [ ] Grid Fill Watchdog (new 2026-09-02): watch the first few nights for false nudges during the 23:30-05:00 refill (gateway may legitimately defer parts of the window); loosen the trigger if it fights the gateway
- [ ] Margin tracker: sanity-check `sensor.grid_margin_today` against the Octopus bill after a full week
- [ ] Update rate constants (6.9p/30.4p/12p) in the margin sensor whenever the tariff changes

## September — Cold-day battery strategy (re-scoped 2026-08-23)
The heat pump deliberately runs at a constant low temp all winter — no scheduling wanted. The winter lever is battery strategy: the pump draws up to 30 kWh on the coldest days, and morning slot-farming is what keeps the batteries topped.
- [ ] Forecast-driven cold-day handling: skip/shrink the 01:30 night dump and refill deeper when tomorrow is forecast cold
- [ ] Decide whether the old disabled seasonal on/off automations (heat pump at off-peak, Altherma morning) get deleted or kept as manual tools
- [x] Salt tracking BUILT 2026-08-23 as software check-in instead of hardware (owner call: too time-poor for the sensor build): weekly actionable push (Sun 10:00 home / arrival catch-up) -> estimate 100/75/50/25/0; handler learns litres-per-percent from the Aquaro meter (EMA, seeded 230 L/%); sensor.salt_level_live interpolates between check-ins; low alerts at 15%/5% with Refilled button
- [ ] Cancel the AliExpress sensor parts order if not wanted for tinkering (XIAO C3 + Grove bits, ~£20)

## Watching / someday
- [ ] Renault 5 V2G — Mobilize UK launch (structural upgrade: ~tripled cycleable capacity); revisit charger investment when available
- [ ] Monthly true-zero battery drain for BMS calibration (evening dump buffer 0 once a month)
- [ ] Decide fate of Solar Arbitrage Mode (EV-neutral with DC-coupled solar; kept for now)

## Decided / not doing
- Agile Outgoing export — not interested; prefer the fixed 12p margin at any time of day
- Pre-filling the battery at peak rate before paid Saving Sessions — rarely worth it; dump whatever is in the battery
- Holiday mode gating energy automations — removed 2026-08-23; arbitrage runs on holiday by design
