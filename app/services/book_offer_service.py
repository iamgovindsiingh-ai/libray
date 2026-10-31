from app import db
from app.models.request import BookOffer
from app.models.member import Member


class BookOfferService:
    @staticmethod
    def create_offer(data, member_id=None):
        """Submit a book to give/lend/exchange/sell."""
        title = (data.get("title") or "").strip()
        author = (data.get("author") or "").strip()
        category = (data.get("category") or "General").strip()
        condition = (data.get("condition") or "Good").strip()
        offer_type = (data.get("offer_type") or "free_giveaway").strip()
        price = float(data.get("price") or 0.0)
        image_url = (data.get("image_url") or "").strip()
        donor_name = (data.get("donor_name") or "").strip()
        contact_phone = (data.get("contact_phone") or "").strip()
        contact_whatsapp = (data.get("contact_whatsapp") or "").strip()
        contact_email = (data.get("contact_email") or "").strip()
        pickup_location = (data.get("pickup_location") or "").strip()
        description = (data.get("description") or "").strip()

        if not title or not author:
            raise ValueError("Book title and author are required.")

        # If donor/seller info not provided, try to populate from member
        if member_id and not donor_name:
            member = Member.query.get(member_id)
            if member:
                donor_name = member.user.full_name if member.user else "Student"
                if not contact_email:
                    contact_email = member.email
                if not contact_phone:
                    contact_phone = member.phone or ""

        if not donor_name:
            raise ValueError("Your name is required to list a book.")
        if not contact_email and not contact_phone and not contact_whatsapp:
            raise ValueError("At least one contact method (phone, WhatsApp, or email) is required.")

        if not contact_email:
            if contact_phone:
                contact_email = f"{contact_phone}@nexshelf.edu"
            elif contact_whatsapp:
                contact_email = f"{contact_whatsapp}@nexshelf.edu"
            else:
                contact_email = "student@nexshelf.edu"

        offer = BookOffer(
            member_id=member_id,
            title=title,
            author=author,
            category=category,
            condition=condition,
            offer_type=offer_type,
            price=price,
            image_url=image_url if image_url else None,
            donor_name=donor_name,
            contact_phone=contact_phone if contact_phone else None,
            contact_whatsapp=contact_whatsapp if contact_whatsapp else None,
            contact_email=contact_email,
            pickup_location=pickup_location if pickup_location else None,
            description=description if description else None,
            status="available",
        )
        db.session.add(offer)
        db.session.commit()
        return offer

    @staticmethod
    def get_offers(status="available", category=None, offer_type=None):
        """Get all book offers matching status, category, and offer_type."""
        query = BookOffer.query
        if status and status != "all":
            query = query.filter_by(status=status)
        if offer_type:
            if offer_type == "sell":
                query = query.filter_by(offer_type="sell")
            elif offer_type == "donate":
                query = query.filter(BookOffer.offer_type.in_(["free_giveaway", "free_donation", "lend", "exchange"]))
            else:
                query = query.filter_by(offer_type=offer_type)
        if category:
            query = query.filter(BookOffer.category.ilike(f"%{category}%"))

        offers = query.order_by(BookOffer.created_at.desc()).all()
        return [
            {
                "id": o.id,
                "title": o.title,
                "author": o.author,
                "category": o.category or "General",
                "condition": o.condition,
                "offer_type": o.offer_type,
                "price": float(o.price or 0.0),
                "image_url": o.image_url or "",
                "donor_name": o.donor_name,
                "donor_dept": o.member.department if o.member else "Campus Reader",
                "contact_phone": o.contact_phone or "",
                "contact_whatsapp": o.contact_whatsapp or "",
                "contact_email": o.contact_email or "",
                "pickup_location": o.pickup_location or "Campus / Library",
                "description": o.description or "",
                "status": o.status,
                "created_at": o.created_at.strftime("%b %d, %Y"),
            }
            for o in offers
        ]

    @staticmethod
    def update_offer_status(offer_id, new_status):
        """Update offer status (available, sold, claimed, archived)."""
        offer = BookOffer.query.get(offer_id)
        if not offer:
            raise ValueError("Book offer not found.")
        offer.status = new_status
        db.session.commit()
        return offer

    @staticmethod
    def delete_offer(offer_id):
        """Delete a book offer."""
        offer = BookOffer.query.get(offer_id)
        if not offer:
            raise ValueError("Book offer not found.")
        db.session.delete(offer)
        db.session.commit()
