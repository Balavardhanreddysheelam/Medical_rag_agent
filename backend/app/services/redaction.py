import re
import structlog

logger = structlog.get_logger()

class RedactionService:
    def __init__(self):
        # Regex patterns for common PHI
        self.patterns = {
            "EMAIL": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "PHONE": r'\b(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})\b',
            "DATE": r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            # Simple SSN pattern
            "SSN": r'\b\d{3}-\d{2}-\d{4}\b',
        }
        logger.info("Initialized Regex-based RedactionService")

    def redact(self, text: str) -> str:
        redacted_text = text
        
        for label, pattern in self.patterns.items():
            redacted_text = re.sub(pattern, f"[{label}]", redacted_text)
            
        return redacted_text

redaction_service = RedactionService()
