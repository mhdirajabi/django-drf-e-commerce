import random
import string

from django.utils.crypto import get_random_string


def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slug + "-" + get_random_string(length=4)
    return unique_slug


def generate_totp():
    rand = random.SystemRandom()
    digits = rand.choices(string.digits, k=4)
    return "".join(digits)
