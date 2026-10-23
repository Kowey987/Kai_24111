ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encode_base62(num: int) -> str:
    """Кодирует число в base62 — короткий код без коллизий."""
    if num == 0:
        return ALPHABET[0]
    base = len(ALPHABET)
    result = []
    while num > 0:
        num, rem = divmod(num, base)
        result.append(ALPHABET[rem])
    return "".join(reversed(result))