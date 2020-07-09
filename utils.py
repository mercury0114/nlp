from re import compile, findall
from decimal import Decimal, InvalidOperation

def long_number(token):
    try:
        d = Decimal(token)
        return d > 99 or d < -99 or d.as_tuple().exponent < 0
    except InvalidOperation:
        return False

def extract_tokens(original_sms):
    sms = original_sms.lower()
    tokens = findall(r'[+-]*[\d]*\.*[\d]+|[a-z]+(?:[-\'][a-z]+)+|[a-z]+|[!$£]', sms)
    return ["_start_"] + [
        "_number_" if long_number(token) else token for token in tokens
    ] + ["_stop_"]

spam_keywords = [
    "!", "click", "visit", "reply", "subscribe", "free", "price", "offer",
    "claim code", "charge", "stop", "unlimited", "expires", "£",
    "new voicemail", "cash prize", "special-call"
]
website_keywords = ["http", "www.", ".com", ".uk"]

def make_vector(original_sms):
    sms = original_sms.lower()
    vector = [keyword in sms for keyword in spam_keywords]
    # Checking for website in sms
    vector.append(any(k in sms for k in website_keywords))
    # Checking for phone number in sms
    vector.append(bool(compile(".*[0-9]{5}.*").match(sms)))
    return vector

def display(sms, outcome, vector):
    print(sms)
    print(outcome)
    d = {spam_keywords[i] for i in range(len(spam_keywords)) if vector[i]}
    if (vector[len(vector) - 2]):
        d.add("website")
    if (vector[len(vector) - 1]):
        d.add("number")
    print(d)
    print()
