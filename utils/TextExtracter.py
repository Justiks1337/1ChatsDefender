import easyocr

from utils.patterns.singleton import Singleton


class TextExtracter(Singleton):

    def __init(self):
        self.reader = easyocr.Reader(['ru'])

    def extract_text(self, image: bytes):
        return " ".join(self.reader.readtext(image, detail=0))
