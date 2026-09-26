from ora_etl_log import parse_log

LOG="""2026-09-26T08:00:00 START BATCH nightly_dwh
2026-09-26T08:00:02 START LOAD_CUSTOMERS
2026-09-26T08:03:15 END LOAD_CUSTOMERS
2026-09-26T08:03:16 START LOAD_ORDERS
2026-09-26T08:10:04 ERROR LOAD_ORDERS ORA-01722 invalid number
2026-09-26T08:10:05 END BATCH nightly_dwh"""

def test_summary():
    s=parse_log(LOG)
    assert len(s.stages)==2
    assert s.stages[0].status=="OK"
    assert s.stages[1].status=="ERROR"
    assert s.oracle_errors==["ORA-01722"]
