from enum import Enum


class ClothingStatus(str, Enum):
    CLEAN = "clean"
    DIRTY = "dirty"
    UNAVAILABLE = "unavailable"


class Season(str, Enum):
    SPRING = "spring"
    SUMMER = "summer"
    FALL = "fall"
    WINTER = "winter"
    ALL_SEASON = "all_season"


class Formality(str, Enum):
    CASUAL = "casual"
    SMART_CASUAL = "smart_casual"
    BUSINESS = "business"
    FORMAL = "formal"
    ATHLETIC = "athletic"
    LOUNGE = "lounge"


class OutfitItemRole(str, Enum):
    TOP = "top"
    BOTTOM = "bottom"
    SHOES = "shoes"
    OUTERWEAR = "outerwear"
    ACCESSORY = "accessory"
    ONE_PIECE = "one_piece"


class ClothingTagSource(str, Enum):
    MANUAL = "manual"
    GENERATED = "generated"
    SYSTEM = "system"


class ProvenanceSource(str, Enum):
    MANUAL = "manual"
    RULE_BASED = "rule_based"
    AI_GENERATED = "ai_generated"


class SuggestionStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
