import spacy
import structlog

logger = structlog.get_logger()

class RedactionService:
    def __init__(self, model: str = "en_core_web_sm"):
        try:
            self.nlp = spacy.load(model)
        except OSError:
            logger.warning(f"Model {model} not found. Downloading...")
            from spacy.cli import download
            download(model)
            self.nlp = spacy.load(model)
        
        self.phi_labels = {"PERSON", "DATE", "GPE", "ORG", "PHONE", "EMAIL"} # Basic set, can be expanded

    def redact(self, text: str) -> str:
        doc = self.nlp(text)
        redacted_text = text
        
        # We iterate in reverse to avoid messing up indices when replacing
        for ent in reversed(doc.ents):
            if ent.label_ in self.phi_labels:
                start = ent.start_char
                end = ent.end_char
                redacted_text = redacted_text[:start] + f"[{ent.label_}]" + redacted_text[end:]
        
        return redacted_text

redaction_service = RedactionService()
