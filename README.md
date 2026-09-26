# ora-etl-log

Analyze timestamped ETL/batch logs and turn them into a compact execution summary.

> **Oracle compatibility**
>
> | Oracle version | Support |
> |---|---|
> | Oracle Database 19c | ✅ Oracle-independent log analysis |
> | Oracle Database 23ai | ✅ Oracle-independent log analysis |
> | Oracle AI Database 26ai | ✅ Oracle-independent log analysis |
>
> The current parser is database-version independent. Oracle error codes found in log messages are preserved, but this tool does not depend on Oracle server metadata.

## What it extracts

- total batch duration;
- stage start/end timestamps;
- stage duration;
- failed stages;
- longest completed stage;
- ORA errors present in messages;
- JSON output for automation.

## Expected log format

The default parser understands lines such as:

```text
2026-09-26T08:00:00 START BATCH nightly_dwh
2026-09-26T08:00:02 START LOAD_CUSTOMERS
2026-09-26T08:03:15 END LOAD_CUSTOMERS
2026-09-26T08:03:16 START LOAD_ORDERS
2026-09-26T08:10:04 ERROR LOAD_ORDERS ORA-01722 invalid number
2026-09-26T08:10:05 END BATCH nightly_dwh
```

## Usage

```bash
python -m pip install "git+https://github.com/raoulmunet/ora-etl-log.git"

ora-etl-log examples/nightly.log
ora-etl-log examples/nightly.log --format json
```

Example summary:

```text
Batch duration: 0:10:05
Completed stages: 1
Failed stages: LOAD_ORDERS
Longest completed stage: LOAD_CUSTOMERS (0:03:13)
Oracle errors: ORA-01722
```

## Scope

Real ETL tools produce many log formats. This first release intentionally supports a tiny readable event format; later adapters can map ODI, SQL*Loader, scheduler or custom logs into the same event model.

## License

MIT.
