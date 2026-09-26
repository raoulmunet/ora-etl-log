from __future__ import annotations
import argparse,json
from pathlib import Path
from .core import parse_log

def main(argv=None):
    p=argparse.ArgumentParser(description="Analyze ETL/batch logs.")
    p.add_argument("source")
    p.add_argument("--format",choices=("text","json"),default="text")
    a=p.parse_args(argv)
    s=parse_log(Path(a.source).read_text(encoding="utf-8"))
    if a.format=="json":
        print(json.dumps({
            "started_at":s.started_at.isoformat() if s.started_at else None,
            "ended_at":s.ended_at.isoformat() if s.ended_at else None,
            "duration_seconds":(s.ended_at-s.started_at).total_seconds() if s.started_at and s.ended_at else None,
            "stages":[x.to_dict() for x in s.stages],
            "oracle_errors":s.oracle_errors
        },indent=2))
    else:
        dur=s.ended_at-s.started_at if s.started_at and s.ended_at else None
        ok=[x for x in s.stages if x.status=="OK"]
        failed=[x.name for x in s.stages if x.status=="ERROR"]
        longest=max((x for x in ok if x.duration),key=lambda x:x.duration,default=None)
        print(f"Batch duration: {dur or 'unknown'}")
        print(f"Completed stages: {len(ok)}")
        print(f"Failed stages: {', '.join(failed) if failed else '-'}")
        print(f"Longest completed stage: {longest.name+' ('+str(longest.duration)+')' if longest else '-'}")
        print(f"Oracle errors: {', '.join(s.oracle_errors) if s.oracle_errors else '-'}")
    return 0
if __name__=="__main__": raise SystemExit(main())
