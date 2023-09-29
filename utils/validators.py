from django.core.validators import RegexValidator

def verify_rsa_phone():
    PHONE_REGEX = RegexValidator(r'^(\+27|0)[6-8][0-9]{8}$', 'RSA phone number is required')
    return PHONE_REGEX