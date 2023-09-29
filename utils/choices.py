from django.db import models

class VerificationChoices(models.TextChoices):
    NOT_VERIFIED = ("NOT VERIFIED", "Not verified")
    PENDING = ("PENDING", "Pending")
    VERIFIED = ("VERIFIED", "Verified")

class IdentityNumberChoices(models.TextChoices):
    ID_NUMBER = ("ID_NUMBER", "Not verified")
    PASSPORT = ("PASSPORT", "Passport")

class TitleChoices(models.TextChoices):
        MR = ("MR", "Mr")
        MRS = ("MRS", "Mrs")
        MS = ("MS", "Miss")
        DR = ("DR", "Doctor")
        PROF = ("PROF", "Professor")
        ADVOCATE = ("ADVOCATE", "Adv")
        CLLR = ("CLLR", "Cllr")
        OTHER = ("OTHER", "Other")

class RelationShip(models.TextChoices):
    OTHER = ("OTHER", "Other")
    WIFE = ("WIFE", "Wife")
    HUSBAND = ("HUSBAND", "Husband")
    DAUGHTER = ("DAUGHTER", "Daughter")
    SON = ("SON", "Son")
    MOTHER = ("MOTHER", "Mother")
    FATHER = ("FATHER", "Father")
    GRANDMOTHER = ("GRANDMOTHER", "Grandmother")
    GRANDFATHER = ("GRANDFATHER", "Grandfather")
    BROTHER = ("BROTHER", "Brother")
    SISTER = ("SISTER", "Sister")
    COUSIN = ("COUSIN", "Cousin")
    AUNT = ("AUNT", "Aunt")
    UNCLE = ("UNCLE", "Uncle")

class QualificationType(models.TextChoices):
    BACHELOR = ("BACHELOR", "Bachelor's Degree")
    MASTER = ("MASTER", "Master's Degree")
    DOCTORAL = ("DOCTORAL", "Doctoral Degree")
    POSTGRAD = ("POSTGRAD_CERT", "Postgraduate Certificate")
    HIGH_CERT = ("HIGH_CERTI", "Higher Certicate")
    ADVA_DIP = ("ADVANCE_DIP", "Advance Diploma")
    DIPLOMA = ("DIPLOMA", "Diploma")
    HONO = ("HONOURS", "Honour's Degree")
    MATRIC = ("MATRIC", "Grade 12 Matric")
    OTHER = ("OTHER", "Other")