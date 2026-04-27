import hashlib
from dataclasses import dataclass


@dataclass
class GuardSketch:
    uid: str
    name: str
    biodome: str
    kit: str
    helmet: str
    cape: str
    beard: str
    emblem: str
    tint: int
    weapon_variant: int
    helmet_finish: str
    tabard: str
    skin_r: int
    skin_g: int
    skin_b: int
    shield_r: int
    shield_g: int
    shield_b: int
    boot_r: int
    boot_g: int
    boot_b: int
    sash: int
    clothing_armor_r: int
    clothing_armor_g: int
    clothing_armor_b: int
    clothing_plate_r: int
    clothing_plate_g: int
    clothing_plate_b: int
    clothing_trim_r: int
    clothing_trim_g: int
    clothing_trim_b: int
    location: str

    @property
    def skin_tone(self):
        return (self.skin_r, self.skin_g, self.skin_b)

    @property
    def shield_color(self):
        return (self.shield_r, self.shield_g, self.shield_b)

    @property
    def boots(self):
        return (self.boot_r, self.boot_g, self.boot_b)

    @property
    def clothing(self):
        return {
            "armor": (self.clothing_armor_r, self.clothing_armor_g, self.clothing_armor_b),
            "plate": (self.clothing_plate_r, self.clothing_plate_g, self.clothing_plate_b),
            "trim":  (self.clothing_trim_r,  self.clothing_trim_g,  self.clothing_trim_b),
        }


def sketch_from_npc(npc, location="Unknown"):
    """Create a GuardSketch from a live GuardNPC."""
    identity = getattr(npc, "identity", None) or {}
    first  = identity.get("first_name", "Guard")
    family = identity.get("family_name", "")
    name   = f"{first} {family}".strip()
    seed_str = f"sketch_{name}_{location}_{getattr(npc, 'kit', '')}_{id(npc)}"
    uid = hashlib.md5(seed_str.encode()).hexdigest()[:12]
    clothing = getattr(npc, "clothing", {})
    armor = clothing.get("armor", (55, 55, 75))
    plate = clothing.get("plate", (155, 160, 165))
    trim  = clothing.get("trim",  (140, 35, 35))
    skin  = getattr(npc, "skin_tone", (230, 195, 155))
    shield = getattr(npc, "shield_color", (140, 35, 35))
    boots  = getattr(npc, "boots", (60, 45, 30))
    return GuardSketch(
        uid=uid,
        name=name,
        biodome=getattr(npc, "biodome", "temperate"),
        kit=getattr(npc, "kit", "spearman"),
        helmet=getattr(npc, "helmet", "pot"),
        cape=getattr(npc, "cape", "none"),
        beard=getattr(npc, "beard", "none"),
        emblem=getattr(npc, "emblem", "none"),
        tint=getattr(npc, "tint", 0),
        weapon_variant=getattr(npc, "weapon_variant", 0),
        helmet_finish=getattr(npc, "helmet_finish", "steel"),
        tabard=getattr(npc, "tabard", "solid"),
        skin_r=skin[0], skin_g=skin[1], skin_b=skin[2],
        shield_r=shield[0], shield_g=shield[1], shield_b=shield[2],
        boot_r=boots[0], boot_g=boots[1], boot_b=boots[2],
        sash=int(getattr(npc, "sash", False)),
        clothing_armor_r=armor[0], clothing_armor_g=armor[1], clothing_armor_b=armor[2],
        clothing_plate_r=plate[0], clothing_plate_g=plate[1], clothing_plate_b=plate[2],
        clothing_trim_r=trim[0],  clothing_trim_g=trim[1],  clothing_trim_b=trim[2],
        location=location,
    )
