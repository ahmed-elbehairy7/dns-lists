from .group import Group, MAX_TTL
from dnslib import QTYPE
from redis import Redis

TYPE_LOOKUP = {
    "A": QTYPE.A,
    "AAAA": QTYPE.AAAA,
    "CAA": QTYPE.CAA,
    "CNAME": QTYPE.CNAME,
    "DNSKEY": QTYPE.DNSKEY,
    "MX": QTYPE.MX,
    "NAPTR": QTYPE.NAPTR,
    "NS": QTYPE.NS,
    "PTR": QTYPE.PTR,
    "RRSIG": QTYPE.RRSIG,
    "SOA": QTYPE.SOA,
    "SRV": QTYPE.SRV,
    "TXT": QTYPE.TXT,
    "SPF": QTYPE.TXT,
}


class Zones(Group):

    table_name = "zoneslist"

    def __init__(self):
        self.name = "zones"
        super().__init__()
        self.list = self.low_raw
        self.merge_high()
    
    @Group.merge_high_decorator
    def merge_high(self):
        self.list += self.high_raw

    def to_redis(self, r : Redis, json : dict):
        for answer in json["answers"]:
            r.setex(f"{json["host"]}:{TYPE_LOOKUP[answer["type"]]}", MAX_TTL, answer["answer"])
