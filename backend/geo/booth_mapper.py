# backend/geo/booth_mapper.py
"""
Maps data to booth-level granularity.
For hackathon demo: uses simulated booth data.
"""
import random


class BoothMapper:
    def __init__(self):
        # Sample booths for demo
        self.booths = {
            "Varanasi": [
                {"id": "VNS-001", "name": "Dashashwamedh Ward", "area": "Dashashwamedh Ghat"},
                {"id": "VNS-002", "name": "Assi Ward", "area": "Assi Ghat"},
                {"id": "VNS-003", "name": "Sigra Ward", "area": "Sigra"},
                {"id": "VNS-004", "name": "Lanka Ward", "area": "Lanka BHU"},
                {"id": "VNS-005", "name": "Cantt Ward", "area": "Cantonment"},
            ],
            "New Delhi": [
                {"id": "DLH-001", "name": "Connaught Place", "area": "CP"},
                {"id": "DLH-002", "name": "Karol Bagh", "area": "Karol Bagh"},
                {"id": "DLH-003", "name": "Chandni Chowk", "area": "Old Delhi"},
                {"id": "DLH-004", "name": "Sarojini Nagar", "area": "South Delhi"},
                {"id": "DLH-005", "name": "Lajpat Nagar", "area": "South East"},
            ],
            "Mumbai North": [
                {"id": "MUM-001", "name": "Borivali", "area": "Borivali West"},
                {"id": "MUM-002", "name": "Kandivali", "area": "Kandivali East"},
                {"id": "MUM-003", "name": "Malad", "area": "Malad West"},
                {"id": "MUM-004", "name": "Goregaon", "area": "Goregaon East"},
                {"id": "MUM-005", "name": "Dahisar", "area": "Dahisar"},
            ],
        }
        print("✅ Booth mapper initialized")

    def assign_booth(self, constituency, text=""):
        """Assign a booth to data within a constituency"""
        if constituency in self.booths:
            # For demo: random booth assignment
            # In production: use address/location parsing
            booth = random.choice(self.booths[constituency])
            return booth["id"]

        return "unknown"

    def get_booths(self, constituency):
        """Get all booths for a constituency"""
        return self.booths.get(constituency, [])

    def get_booth_info(self, booth_id):
        """Get booth details by ID"""
        for constituency, booths in self.booths.items():
            for booth in booths:
                if booth["id"] == booth_id:
                    booth["constituency"] = constituency
                    return booth
        return None


# Quick test
if __name__ == "__main__":
    mapper = BoothMapper()

    print("\n🗳️ Booth Mapper Tests:\n")

    booths = mapper.get_booths("Varanasi")
    print(f"  Varanasi booths: {len(booths)}")
    for b in booths:
        print(f"    {b['id']} — {b['name']} ({b['area']})")

    print(f"\n  Random assignment: {mapper.assign_booth('Varanasi')}")
    print(f"  Random assignment: {mapper.assign_booth('New Delhi')}")
    print(f"  Unknown: {mapper.assign_booth('RandomPlace')}")