from datetime import datetime
class JoinApplier:
    def __init__(self, data: dict):
        self.mail_addr = data["mail_address"]
        _applied_at = datetime.strptime(data["applied_at"], "%Y-%m-%d %H:%M:%S %z") # ex) 2024-01-01 01:11:11 +0900
        self.applied_at = str(_applied_at)
        self.name = data["name"]
        self.univ = data["university"]
        self.dep = data["department"]
        self.grade = data["grade"]
        self.reason = data["reason"]
        self.opportunity = data.get("opportunity", None)  # opportunityのみNULL許容
        self.possible_dates = data["possible_dates"]

    def to_dict(self):
        return {
            "mail_address": self.mail_addr,
            "applied_at": self.applied_at,
            "name": self.name,
            "university": self.univ,
            "department": self.dep,
            "grade": self.grade,
            "reason": self.reason,
            "opportunity": self.opportunity,
            "possible_dates": self.possible_dates
        }
