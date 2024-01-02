from pydantic import constr, validator
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

# from .models.utils import StrEnum
from enum import StrEnum
import dns.resolver

states = {
    "AK": "ALASKA",
    "AL": "ALABAMA",
    "AR": "ARKANSAS",
    "AZ": "ARIZONA",
    "CA": "CALIFORNIA",
    "CO": "COLORADO",
    "CT": "CONNECTICUT",
    "DC": "DISTRICT OF COLUMBIA",
    "DE": "DELAWARE",
    "FL": "FLORIDA",
    "GA": "GEORGIA",
    "HI": "HAWAII",
    "IA": "IOWA",
    "ID": "IDAHO",
    "IL": "ILLINOIS",
    "IN": "INDIANA",
    "KS": "KANSAS",
    "KY": "KENTUCKY",
    "LA": "LOUISIANA",
    "MA": "MASSACHUSETTS",
    "MD": "MARYLAND",
    "ME": "MAINE",
    "MI": "MICHIGAN",
    "MN": "MINNESOTA",
    "MO": "MISSOURI",
    "MS": "MISSISSIPPI",
    "MT": "MONTANA",
    "NC": "NORTH CAROLINA",
    "ND": "NORTH DAKOTA",
    "NE": "NEBRASKA",
    "NH": "NEW HAMPSHIRE",
    "NJ": "NEW JERSEY",
    "NM": "NEW MEXICO",
    "NV": "NEVADA",
    "NY": "NEW YORK",
    "OH": "OHIO",
    "OK": "OKLAHOMA",
    "OR": "OREGON",
    "PA": "PENNSYLVANIA",
    "RI": "RHODE ISLAND",
    "SC": "SOUTH CAROLINA",
    "SD": "SOUTH DAKOTA",
    "TN": "TENNESSEE",
    "TX": "TEXAS",
    "UT": "UTAH",
    "VA": "VIRGINIA",
    "VT": "VERMONT",
    "WA": "WASHINGTON",
    "WI": "WISCONSIN",
    "WV": "WEST VIRGINIA",
    "WY": "WYOMING",
}


class Address(SQLModel):
    street: str
    city: str
    state: str
    state_abbr: Optional[str]
    zip_code: str

    @validator("zip_code")
    def must_be_valid_zip_code(cls, v):
        if not v.isnumeric() or len(v) != 5:
            raise ValueError("Zip code must be a 5-digit number")
        return v

    @validator("state")
    def must_be_valid_state(cls, v):
        if v not in cls.states.values():
            raise ValueError("Invalid state")
        return v

    @validator("state_abbr")
    def must_be_valid_state_abbr(cls, v):
        if v not in cls.states.keys():
            raise ValueError("Invalid state abbreviation")
        return v

    @validator("state_abbr", always=True)
    def set_state_abbr(cls, v, values):
        if "state" in values:
            return cls.states[values["state"]]
        return v


class Role(StrEnum):
    OWNER = "Owner"
    MANAGER = "Manager"
    TRAINER = "Trainer"
    STAFF = "Staff"
    MEMBER = "Member"
    GUEST = "Guest"
    VENDOR = "Vendor"


# class UserBase(SQLModel):
#     name: constr(min_length=3, max_length=100)
#     email: str
#     role: Optional[Role] = None
#     created_at: datetime = Field(default_factory=datetime.now)

#     @validator("name")
#     def validate_name(cls, v):
#         if not v.replace(" ", "").isalpha():
#             raise ValueError("Name must only contain alphabetic characters")
#         return v.title()

#     @validator("email")
#     def validate_email(cls, v):
#         # Verify's that the email's domain has valid MX (Mail Exchange) records, indicating that it is capable of receiving emails.
#         domain = v.split("@")[1]
#         try:
#             dns.resolver.resolve(domain, "MX")
#         except dns.resolver.NoAnswer:
#             raise ValueError("Email domain has no MX records")

#         # TODO: Email verification logic should be handled by a separate service

#         return v.lower()
