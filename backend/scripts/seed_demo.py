from __future__ import annotations

from app.auth.password import get_password_hash
from app.core.enums import ClothingStatus, Formality, OutfitItemRole, Season
from app.db.session import SessionLocal
from app.models.clothing_item import ClothingItem
from app.models.outfit import Outfit
from app.models.outfit_item import OutfitItem
from app.models.user import User


def seed_demo() -> None:
    db = SessionLocal()

    try:
        user = db.query(User).filter(User.email == "demo@virtualcloset.dev").first()
        if user is None:
            user = User(
                email="demo@virtualcloset.dev",
                display_name="Demo Stylist",
                hashed_password=get_password_hash("demo12345"),
                is_active=True,
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        existing_items = db.query(ClothingItem).filter(ClothingItem.user_id == user.id).count()
        if existing_items == 0:
            items = [
                ClothingItem(
                    user_id=user.id,
                    name="Blue Oxford Shirt",
                    category="tops",
                    subcategory="shirt",
                    primary_color="blue",
                    season=Season.SPRING,
                    formality=Formality.SMART_CASUAL,
                    status=ClothingStatus.CLEAN,
                ),
                ClothingItem(
                    user_id=user.id,
                    name="Stone Chinos",
                    category="bottoms",
                    subcategory="pants",
                    primary_color="beige",
                    season=Season.SPRING,
                    formality=Formality.SMART_CASUAL,
                    status=ClothingStatus.CLEAN,
                ),
                ClothingItem(
                    user_id=user.id,
                    name="White Sneakers",
                    category="shoes",
                    subcategory="sneakers",
                    primary_color="white",
                    season=Season.ALL_SEASON,
                    formality=Formality.CASUAL,
                    status=ClothingStatus.CLEAN,
                ),
                ClothingItem(
                    user_id=user.id,
                    name="Navy Overshirt",
                    category="outerwear",
                    subcategory="jacket",
                    primary_color="navy",
                    season=Season.FALL,
                    formality=Formality.SMART_CASUAL,
                    status=ClothingStatus.CLEAN,
                ),
            ]
            db.add_all(items)
            db.commit()

        existing_outfits = db.query(Outfit).filter(Outfit.user_id == user.id).count()
        if existing_outfits == 0:
            top = db.query(ClothingItem).filter_by(user_id=user.id, category="tops").first()
            bottom = db.query(ClothingItem).filter_by(user_id=user.id, category="bottoms").first()
            shoes = db.query(ClothingItem).filter_by(user_id=user.id, category="shoes").first()

            if top and bottom and shoes:
                outfit = Outfit(
                    user_id=user.id,
                    name="Demo Smart Casual",
                    notes="A seeded look for quick exploration.",
                )
                outfit.items = [
                    OutfitItem(clothing_item_id=top.id, role=OutfitItemRole.TOP, position=0),
                    OutfitItem(clothing_item_id=bottom.id, role=OutfitItemRole.BOTTOM, position=1),
                    OutfitItem(clothing_item_id=shoes.id, role=OutfitItemRole.SHOES, position=2),
                ]
                db.add(outfit)
                db.commit()

        print("Demo data ready.")
        print("Email: demo@virtualcloset.dev")
        print("Password: demo12345")
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo()
