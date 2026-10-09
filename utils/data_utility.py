"""Text utilities for AskScience post data.

Helpers for cleaning and featurizing Reddit post titles and bodies before
embedding and modeling. All functions are pure string transforms and make
no network or model calls.
"""

from unidecode import unidecode
import re


class DataUtil():
    """Text cleaning and feature extraction utilities for AskScience posts."""

    def __init__(self):
        pass

    def replace_chars(self, text):
        """Replace punctuation and special characters in a text.

        Maps common punctuation to spaces or underscores, collapses
        repeated separators, and drops tokens that are pure digits or
        longer than 25 characters.

        Args:
            text: Raw text (title, body, or tag).

        Returns:
            The cleaned text as a single whitespace-separated string.
        """
        chars = {'?':' ',',':' ','/':'_','!':' ','"':'_','-':'_','{':' ','}':' ','(':' ',')':' ','[':' ',']':' ','{':' ','}':' ','<':' ','>':' ','$':' ','%':' ',':':' ','&':'and','|':' ','+':'_','=':'_','*':'_',';':'_','^':'_','\\':' ','~':' ','\'':'','http':' ','nan':' ','#':' ','\n':' '}
        for k, v in chars.items():
            text = text.replace(k, v)

        text = ' '.join(text.replace(' _ ', ' ').replace('_ ', ' ').replace(' _', ' ').replace('__', '_').split())
        new_text = []
        for w in text.split():
            if not w.isdigit() and len(w) < 25:
                new_text.append(w)
        new_text = ' '.join(new_text)

        return new_text

    def split_sentence(self, text):
        """Split text into sentences on '. '.

        Args:
            text: Raw text.

        Returns:
            List of sentence strings.
        """
        return text.split('. ')

    def cleaning_text(self, text):
        """Lowercase text, strip accents, and collapse whitespace.

        Args:
            text: Raw text (coerced to str).

        Returns:
            Lowercased, ASCII, single-spaced text.
        """
        text = unidecode(str(text))
        return ' '.join(str(text).lower().split())

    def count_qs(self, text):
        """Count the number of question marks (questions) in a text.

        Args:
            text: Raw text.

        Returns:
            Number of '?' segments in the text.
        """
        pattern = r"[?]"
        sentences = [sentence for sentence in re.split(pattern, text) if sentence]
        return len(sentences)

    def count_links_cited(self, text):
        """Count URL-like citations in a text.

        Uses a broad URL/IP pattern, so a match is an approximate
        citation count, not a validated link.

        Args:
            text: Raw text.

        Returns:
            Number of regex matches, or 0 for empty text.
        """
        # Broad URL/IP/host regex. Note: matches are approximate; the
        # intent is citation counting, not link validation.
        regex = r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"

        if len(text):
            links = re.findall(regex, text)
            return len(links)
        else:
            return 0
