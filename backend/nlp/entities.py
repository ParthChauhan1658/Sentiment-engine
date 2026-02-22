# backend/nlp/entities.py
"""
Named Entity Recognition using spaCy.
Extracts person names, organizations, locations.
"""


class EntityExtractor:
    def __init__(self):
        try:
            import spacy
            self.nlp = spacy.load("en_core_web_sm")
            self.working = True
            print("✅ Entity extractor initialized (spaCy)")
        except Exception as e:
            print(f"⚠️ spaCy not available: {e}")
            print("   Run: python -m spacy download en_core_web_sm")
            self.working = False

    def extract_entities(self, text):
        """Extract named entities from text"""
        if not self.working or not text or len(text.strip()) < 5:
            return []

        try:
            doc = self.nlp(text[:1000])  # Limit text length

            entities = []
            for ent in doc.ents:
                if ent.label_ in ["PERSON", "ORG", "GPE", "LOC", "NORP"]:
                    entities.append({
                        "text": ent.text,
                        "type": ent.label_,
                        # PERSON=person, ORG=organization, 
                        # GPE=location, LOC=location, NORP=group
                    })

            # Remove duplicates
            seen = set()
            unique = []
            for e in entities:
                key = f"{e['text']}_{e['type']}"
                if key not in seen:
                    seen.add(key)
                    unique.append(e)

            return unique

        except Exception as e:
            return []

    def extract_entities_batch(self, texts):
        """Extract entities from multiple texts"""
        all_entities = []
        for text in texts:
            entities = self.extract_entities(text)
            all_entities.append(entities)
        return all_entities

    def get_entity_names(self, text):
        """Get just the entity name strings"""
        entities = self.extract_entities(text)
        return [e["text"] for e in entities]

    def get_locations(self, text):
        """Extract only location entities"""
        entities = self.extract_entities(text)
        return [e["text"] for e in entities if e["type"] in ["GPE", "LOC"]]

    def get_persons(self, text):
        """Extract only person names"""
        entities = self.extract_entities(text)
        return [e["text"] for e in entities if e["type"] == "PERSON"]


# Quick test
if __name__ == "__main__":
    extractor = EntityExtractor()

    test_texts = [
        "Prime Minister Modi visited Varanasi and met with BJP workers",
        "Congress leader Rahul Gandhi criticized the government in Parliament",
        "Chennai floods affected thousands, Tamil Nadu CM announced relief",
    ]

    print("\n🏷️ Entity Extraction Tests:\n")
    for text in test_texts:
        entities = extractor.extract_entities(text)
        locations = extractor.get_locations(text)
        print(f"  Text: {text[:60]}...")
        print(f"  Entities: {entities}")
        print(f"  Locations: {locations}")
        print()