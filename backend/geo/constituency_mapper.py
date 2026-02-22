# backend/geo/constituency_mapper.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SAMPLE_CONSTITUENCIES


class ConstituencyMapper:
    def __init__(self):
        self.constituencies = SAMPLE_CONSTITUENCIES

        # Expanded keyword mapping — more words = better matching
        self.keyword_map = {
            # Varanasi
            "varanasi": "Varanasi", "banaras": "Varanasi", "kashi": "Varanasi",
            "काशी": "Varanasi", "वाराणसी": "Varanasi", "बनारस": "Varanasi",
            "ganga ghat": "Varanasi", "bhu": "Varanasi",

            # Delhi
            "delhi": "New Delhi", "new delhi": "New Delhi", "दिल्ली": "New Delhi",
            "नई दिल्ली": "New Delhi", "ncr": "New Delhi", "delhi ncr": "New Delhi",
            "parliament": "New Delhi", "lok sabha": "New Delhi",
            "rajya sabha": "New Delhi", "संसद": "New Delhi",

            # Mumbai
            "mumbai": "Mumbai North", "bombay": "Mumbai North", "मुंबई": "Mumbai North",
            "bandra": "Mumbai North", "andheri": "Mumbai North",
            "borivali": "Mumbai North", "malad": "Mumbai North",

            # Chennai
            "chennai": "Chennai South", "madras": "Chennai South", "चेन्नई": "Chennai South",
            "tamil nadu": "Chennai South", "तमिलनाडु": "Chennai South",

            # Kolkata
            "kolkata": "Kolkata North", "calcutta": "Kolkata North", "कोलकाता": "Kolkata North",
            "bengal": "Kolkata North", "बंगाल": "Kolkata North",

            # Lucknow
            "lucknow": "Lucknow", "लखनऊ": "Lucknow",

            # Patna
            "patna": "Patna Sahib", "पटना": "Patna Sahib",
            "bihar": "Patna Sahib", "बिहार": "Patna Sahib",

            # Gandhinagar
            "gandhinagar": "Gandhinagar", "गांधीनगर": "Gandhinagar",
            "gujarat": "Gandhinagar", "गुजरात": "Gandhinagar",
            "ahmedabad": "Gandhinagar",

            # Bangalore
            "bangalore": "Bangalore South", "bengaluru": "Bangalore South",
            "बैंगलोर": "Bangalore South", "karnataka": "Bangalore South",

            # Hyderabad
            "hyderabad": "Hyderabad", "हैदराबाद": "Hyderabad",
            "telangana": "Hyderabad", "तेलंगाना": "Hyderabad",

            # General political keywords → map to Delhi (national politics)
            "modi": "New Delhi", "pm modi": "New Delhi",
            "prime minister": "New Delhi", "प्रधानमंत्री": "New Delhi",
            "bjp headquarters": "New Delhi", "congress headquarters": "New Delhi",

            # State-level mapping
            "uttar pradesh": "Lucknow", "up": "Lucknow",
            "उत्तर प्रदेश": "Lucknow",
            "maharashtra": "Mumbai North", "महाराष्ट्र": "Mumbai North",
            "rajasthan": "New Delhi", "madhya pradesh": "New Delhi",
            "punjab": "New Delhi", "haryana": "New Delhi",
        }

        print("✅ Constituency mapper initialized")

    def map_text_to_constituency(self, text, location=""):
        """Map text to constituency — improved matching"""
        if not text and not location:
            return "unknown"

        combined = f"{text} {location}".lower()

        # Check for exact keyword matches
        for keyword, constituency in self.keyword_map.items():
            if keyword in combined:
                return constituency

        # Check for partial state/city matches
        # If text mentions "india" or "government" in general, map to Delhi
        general_national = ["india", "bharat", "भारत", "national", "country",
                           "desh", "देश", "sarkar", "सरकार", "government"]
        for word in general_national:
            if word in combined:
                return "New Delhi"

        return "unknown"

    def map_batch(self, items):
        """Map multiple items to constituencies"""
        for item in items:
            text = item.get("text", "")
            location = item.get("location", "")
            item["constituency"] = self.map_text_to_constituency(text, location)
        return items

    def get_constituency_info(self, name):
        for c in self.constituencies:
            if c["name"].lower() == name.lower():
                return c
        return None

    def get_all_constituencies(self):
        return self.constituencies

    def get_constituency_coordinates(self):
        return {
            c["name"]: {"lat": c["lat"], "lng": c["lng"], "state": c["state"]}
            for c in self.constituencies
        }


if __name__ == "__main__":
    mapper = ConstituencyMapper()

    tests = [
        "Water supply is terrible in Varanasi",
        "Modi government doing great work",
        "Mumbai floods are devastating",
        "Bihar elections are coming soon",
        "मोदी जी ने बहुत अच्छा काम किया",
        "सरकार बिल्कुल बेकार है",
        "Gujarat development model is working",
        "Random comment about nothing specific",
    ]

    print("\n📍 Constituency Mapping Tests:\n")
    for text in tests:
        result = mapper.map_text_to_constituency(text)
        emoji = "✅" if result != "unknown" else "❌"
        print(f"  {emoji} \"{text[:50]}...\"")
        print(f"     → {result}")
        print()