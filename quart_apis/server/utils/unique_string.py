import secrets
import string


def unique_string(prefix:str,lenght=8) -> str:
    TOTAL_LEN = lenght
    SUFFIX_LEN = TOTAL_LEN - len(prefix)
    # base36-ish, lowercase
    ALPHABET = string.ascii_lowercase + string.digits  
    suffix = ''.join(secrets.choice(ALPHABET) for _ in range(SUFFIX_LEN))
    return prefix + suffix


if __name__ == "__main__":
    print(unique_string("usr",100))