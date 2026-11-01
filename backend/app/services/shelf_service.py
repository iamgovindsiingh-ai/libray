from app.models import Book


ZONES_MAP = {
    "Zone A": {
        "name": "Turing Wing (Computing & AI)",
        "color": "#3b82f6",
        "racks": ["Rack 01", "Rack 02", "Rack 03"],
        "categories": ["Computer Science", "Artificial Intelligence", "Programming", "Data Science"],
    },
    "Zone B": {
        "name": "Ramanujan Wing (Math & Theory)",
        "color": "#10b981",
        "racks": ["Rack 04", "Rack 05"],
        "categories": ["Mathematics", "Algorithms", "Discrete Mathematics", "Physics"],
    },
    "Zone C": {
        "name": "Tesla Wing (Hardware & Electronics)",
        "color": "#f59e0b",
        "racks": ["Rack 06", "Rack 07"],
        "categories": ["Electronics", "Robotics", "Engineering", "Digital Logic"],
    },
    "Zone D": {
        "name": "Hypatia Wing (Humanities & Reference)",
        "color": "#8b5cf6",
        "racks": ["Rack 08"],
        "categories": ["General", "Literature", "Management", "Reference"],
    },
}


class ShelfService:
    @staticmethod
    def get_library_map_layout():
        """Returns the floor layout, zones, racks, and books positioned on each shelf."""
        all_books = Book.query.all()
        
        # Build rack occupancy
        zones_data = {}
        for zone_id, zone_info in ZONES_MAP.items():
            zones_data[zone_id] = {
                "name": zone_info["name"],
                "color": zone_info["color"],
                "racks": {},
            }
            for rack in zone_info["racks"]:
                zones_data[zone_id]["racks"][rack] = {
                    "shelves": {1: [], 2: [], 3: [], 4: []}
                }

        # Populate books into their shelf positions
        for book in all_books:
            loc = book.shelf_location or "Zone A · Rack 01 · Shelf 1"
            parts = [p.strip() for p in loc.split("·")]
            
            zone = parts[0] if len(parts) > 0 and parts[0] in zones_data else "Zone A"
            rack = parts[1] if len(parts) > 1 and parts[1] in zones_data[zone]["racks"] else "Rack 01"
            shelf_num = 1
            if len(parts) > 2:
                try:
                    shelf_num = int("".join(filter(str.isdigit, parts[2])) or 1)
                    if shelf_num not in [1, 2, 3, 4]:
                        shelf_num = 1
                except Exception:
                    shelf_num = 1

            zones_data[zone]["racks"][rack]["shelves"][shelf_num].append({
                "id": book.id,
                "title": book.title,
                "author": book.author.name if book.author else "Unknown",
                "available": book.available_quantity,
                "accent_color": book.accent_color or "#3b82f6",
                "isbn": book.isbn,
            })

        return {
            "zones": zones_data,
            "total_books_shelved": len(all_books),
        }

    @staticmethod
    def locate_book_on_shelf(book_id):
        """Locates the exact zone, rack, shelf coordinates and navigation instructions for a book."""
        book = Book.query.get(book_id)
        if not book:
            return None

        loc = book.shelf_location or "Zone A · Rack 01 · Shelf 1"
        parts = [p.strip() for p in loc.split("·")]
        zone_key = parts[0] if len(parts) > 0 else "Zone A"
        rack_key = parts[1] if len(parts) > 1 else "Rack 01"
        shelf_str = parts[2] if len(parts) > 2 else "Shelf 1"

        zone_meta = ZONES_MAP.get(zone_key, ZONES_MAP["Zone A"])

        # Navigation steps
        nav_steps = [
            f"1. Enter the Library Main Hall and turn towards {zone_meta['name']} ({zone_key}).",
            f"2. Proceed along Aisle {zone_key[-1]} until you reach {rack_key}.",
            f"3. Look on {shelf_str} (eye-level numbered bay).",
            f"4. Match Book Spine / ISBN: '{book.isbn}'.",
        ]

        return {
            "book_id": book.id,
            "title": book.title,
            "author": book.author.name if book.author else None,
            "category": book.category.name if book.category else None,
            "available_quantity": book.available_quantity,
            "shelf_location": loc,
            "zone": zone_key,
            "zone_name": zone_meta["name"],
            "rack": rack_key,
            "shelf": shelf_str,
            "color": zone_meta["color"],
            "navigation_steps": nav_steps,
        }

