import spacy
import random
from difflib import SequenceMatcher
import re

class PIIMasker:
    def __init__(self, model="en_core_web_sm", max_tokens=512):
        self.nlp = spacy.load(model)
        self.fake_names = []
        self.fake_orgs = []
        self.fake_locations = []
        self.mapping = {"PERSON": {}, "ORG": {}, "GPE": {}}
        self.max_tokens = max_tokens

    def set_fake_names(self, names):
        self.fake_names = names

    def set_fake_orgs(self, orgs):
        self.fake_orgs = orgs

    def set_fake_locations(self, locations):
        self.fake_locations = locations

    def mask_pii(self, text):
        chunks = self._split_into_chunks(text)
        masked_chunks = []

        for chunk in chunks:
            try:
                doc = self.nlp(chunk)
                masked_chunk = chunk

                for ent in doc.ents:
                    if ent.label_ == "PERSON":
                        masked_chunk = self._mask_entity(masked_chunk, ent, self.fake_names, "PERSON")
                    # elif ent.label_ == "ORG":
                    #     masked_chunk = self._mask_entity(masked_chunk, ent, self.fake_orgs, "ORG")
                    elif ent.label_ == "GPE":
                        masked_chunk = self._mask_entity(masked_chunk, ent, self.fake_locations, "GPE")

                masked_chunks.append(masked_chunk)
            except Exception as e:
                print(f"An error occurred while processing a chunk: {e}")

        return ''.join(masked_chunks)
    
    def _normalize_entity(self, entity):
        # Example normalization: lowercasing and stripping common articles
        normalized = entity.lower().strip().replace('the ', '').replace('a ', '')
        return normalized

    def _mask_entity(self, text, entity, fake_list, entity_type):
        normalized_entity = self._normalize_entity(entity.text)
        
        # Find the best match in existing mappings
        best_match = None
        highest_similarity = 0.8  # A threshold to determine if it's a match

        for existing_entity in self.mapping[entity_type]:
            similarity = SequenceMatcher(None, normalized_entity, self._normalize_entity(existing_entity)).ratio()
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = existing_entity

        if best_match:
            # Use the existing fake value
            fake_value = self.mapping[entity_type][best_match]
        else:
            if fake_list:
                fake_value = random.choice(fake_list)
                self.mapping[entity_type][normalized_entity] = fake_value

        # Use regex to replace only whole words, preserving the original text casing
        pattern = r'\b' + re.escape(entity.text) + r'\b'
        text = re.sub(pattern, fake_value, text, flags=re.IGNORECASE)
        
        return text

    def _split_into_chunks(self, text):
        doc = self.nlp(text)
        chunks = []
        current_chunk = []
        current_length = 0

        for token in doc:
            current_chunk.append(token.text)
            current_length += 1
            if current_length >= self.max_tokens:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_length = 0

        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks
    
    def mask_phone_numbers(self, text):
        # Example regex for U.S. phone numbers
        phone_regex = r'\b(?:\+?(\d{1,3}))?[-. ]?(\d{3})[-. ]?(\d{3})[-. ]?(\d{4})\b'
        return re.sub(phone_regex, '[PHONE]', text)

    def mask_dates_of_birth(self, text):
        # Example regex for dates (simple version, can be made more complex)
        date_regex = r'\b\d{2}[/-]\d{2}[/-]\d{4}\b'
        return re.sub(date_regex, '[DOB]', text)

    def mask_credit_card_numbers(self, text):
        # Example regex for credit card numbers
        cc_regex = r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b'
        return re.sub(cc_regex, '[CREDIT_CARD]', text)

    def mask_ssns(self, text):
        # Example regex for SSNs
        ssn_regex = r'\b\d{3}[- ]?\d{2}[- ]?\d{4}\b'
        return re.sub(ssn_regex, '[SSN]', text)

    def mask_all_pii(self, text):
        text = self.mask_pii(text)
        text = self.mask_phone_numbers(text)
        text = self.mask_dates_of_birth(text)
        text = self.mask_credit_card_numbers(text)
        text = self.mask_ssns(text)
        return text

    def get_mapping(self):
        return self.mapping

# Usage
# masker = PIIMasker()
# masker.set_fake_names(["John Doe", "Jane Smith", "Alice Johnson"])
# masker.set_fake_orgs(["Acme Corp", "Globex Inc", "Soylent Company"])
# masker.set_fake_locations(["Metropolis", "Gotham", "Springfield"])

# input_text = "Your original text here..."
# masked_text = masker.mask_pii(input_text)
# print(masked_text)
# print("Mapping:", masker.get_mapping())
