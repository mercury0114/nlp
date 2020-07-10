import predictor
import re

class AlwaysHamPredictor(predictor.Interface):
    name = "Always-ham-predictor"

    def predict_one(self, sms):
        return predictor.HAM

_SPAM_KEYWORDS = [
    "!", "click", "visit", "reply", "subscribe", "free", "price", "offer",
    "claim code", "charge", "stop", "unlimited", "expires", "£",
    "new voicemail", "cash prize", "special-call"
]
_WEB_KEYWORDS = ["http", "www.", ".com", ".uk"]

def _make_vector(original_sms):
    sms = original_sms.lower()
    vector = [keyword in sms for keyword in _SPAM_KEYWORDS]
    # Checking for website in sms
    vector.append(any(web_keyword in sms for web_keyword in _WEB_KEYWORDS))
    # Checking for phone number in sms
    vector.append(bool(re.compile(".*[0-9]{5}.*").match(sms)))
    return vector

class SimplePredictor(predictor.Interface):
    name = "Simple-predictor"

    def predict_one(self, sms):
        vector = _make_vector(sms)
        return predictor.SPAM if sum(vector) >= 2 else predictor.HAM
