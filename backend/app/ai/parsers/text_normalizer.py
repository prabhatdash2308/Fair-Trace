import re
import unicodedata

class TextNormalizer:
    """
    Standardizes text extracted from various document formats.
    """
    
    # Matches multiple spaces or tabs
    _duplicate_spaces_re = re.compile(r'[ \t]+')
    
    # Matches multiple newlines (more than 2)
    _multiple_newlines_re = re.compile(r'\n{3,}')
    
    # Matches control characters (excluding tab and newline)
    _control_chars_re = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]')

    @classmethod
    def normalize(cls, text: str) -> str:
        if not text:
            return ""

        # 1. Unicode Normalization (NFC)
        # Converts decomposed characters into precomposed characters
        text = unicodedata.normalize('NFC', text)
        
        # 2. Normalize line endings to standard Unix (\n)
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # 3. Remove control characters
        text = cls._control_chars_re.sub('', text)
        
        # 4. Remove duplicate spaces and tabs
        text = cls._duplicate_spaces_re.sub(' ', text)
        
        # 5. Cap consecutive newlines to maximum of 2
        text = cls._multiple_newlines_re.sub('\n\n', text)
        
        # 6. Trim leading/trailing whitespace
        return text.strip()
