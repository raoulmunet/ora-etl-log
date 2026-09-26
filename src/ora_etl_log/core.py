from __future__ import annotations
from dataclasses import dataclass,asdict
from datetime import datetime
import re

@dataclass(frozen=True)
class Stage:
    name:str
    started_at:datetime
    ended_at:datetime|None
    status:str
    message:str|None=None
    @property
    def duration(self):
        return None if self.ended_at is None else self.ended_at-self.started_at
    def to_dict(self):
        d=asdict(self)
        d["started_at"]=self.started_at.isoformat()
        d["ended_at"]=self.ended_at.isoformat() if self.ended_at else None
        d["duration_seconds"]=self.duration.total_seconds() if self.duration else None
        return d

@dataclass(frozen=True)
class LogSummary:
    started_at:datetime|None
    ended_at:datetime|None
    stages:list[Stage]
    oracle_errors:list[str]

def parse_log(text:str)->LogSummary:
    starts={}
    stages=[]
    batch_start=batch_end=None
    errors=set()
    for line in text.splitlines():
        m=re.match(r"^(\S+)\s+(START|END|ERROR)\s+([^\s]+)(?:\s+(.*))?$",line.strip(),re.I)
        if not m: continue
        try: ts=datetime.fromisoformat(m.group(1))
        except ValueError: continue
        event=m.group(2).upper(); name=m.group(3); msg=m.group(4) or ""
        errors.update(re.findall(r"ORA-\d{5}",msg,re.I))
        if name.upper()=="BATCH":
            if event=="START": batch_start=ts
            elif event=="END": batch_end=ts
            continue
        if event=="START":
            starts[name]=(ts,None)
        elif event=="END" and name in starts:
            st,_=starts.pop(name)
            stages.append(Stage(name,st,ts,"OK"))
        elif event=="ERROR":
            st=starts.pop(name,(ts,None))[0]
            stages.append(Stage(name,st,ts,"ERROR",msg))
    for name,(st,_) in starts.items():
        stages.append(Stage(name,st,None,"RUNNING"))
    stages.sort(key=lambda s:s.started_at)
    return LogSummary(batch_start,batch_end,stages,sorted(x.upper() for x in errors))
