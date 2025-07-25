from datetime import datetime
from dateutil.parser import parse

def valid_date(base_date: datetime, candidate_date: str, base_older: bool):
    candidate_date_dt = parse(candidate_date)
    
    return (base_date.date() <= candidate_date_dt.date()) == base_older