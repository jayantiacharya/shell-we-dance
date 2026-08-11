# Data Schema — Interface Contract

CS 3030 - Project 7: Final Capstone

This is the shared contract between Eric's collector, Jayanti's aggregator,
and Omar's dashboard. Proposed by Jayanti — react/adjust as a team, then once
agreed, everyone can build against this independently.

## 1. Bash collector output (raw_metrics.txt)

One `key=value` pair per line:

```
disk_usage_percent=42
cpu_load_1min=0.35
process_count=187
log_size_kb=1024
docker_available=true
docker_container_count=3
```

Notes:
- Flat key=value format — no nesting, since Bash can't easily produce structured output
- `docker_available` is a separate flag so the dashboard can show "Docker not running"
  instead of a broken number if Docker isn't installed on the test machine
- Keys use snake_case to match Python variable names directly

## 2. Aggregator output (health.json)

```json
{
  "timestamp": "2026-07-25T18:42:00Z",
  "metrics": {
    "disk_usage_percent": 42,
    "cpu_load_1min": 0.35,
    "process_count": 187,
    "log_size_kb": 1024,
    "docker_available": true,
    "docker_container_count": 3
  },
  "alerts": [
    "disk_usage_percent (92) exceeded threshold (85)"
  ]
}
```

Notes:
- `timestamp` is ISO 8601 UTC, at the top level
- `metrics` is a flat dict, same keys as the raw input but typed correctly
  (numbers as numbers/booleans, not strings)
- `alerts` is a list of plain human-readable strings — dashboard just loops
  over these and displays them, no parsing needed



 This document defines how our three components talk to each other, so we can all build our own pieces independently without guessing at each other's formats. Eric's Bash script needs to output metrics in the exact key=value format shown above — Jayanti's Python script depends on parsing that exact format. Jayanti's script then needs to produce the health.json file in the exact structure shown above — Omar's dashboard depends on reading that exact structure. Please review both formats and either confirm they work for your part, or flag anything you'd want changed before we lock this in and start building.

## Status

- [ ] Reviewed and approved by Eric
- [ ] Reviewed and approved by Omar
- [ ] Reviewed and approved by Jayanti