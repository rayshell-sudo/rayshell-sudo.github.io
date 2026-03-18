"""Helper utility for validating email addresses."""

import re


# Practical email validation pattern (not fully RFC 5322 exhaustive).
EMAIL_PATTERN = re.compile(
    r"^(?=.{1,254}$)(?=.{1,64}@)"
    r"[A-Za-z0-9](?:[A-Za-z0-9._%+-]{0,62}[A-Za-z0-9])?"
    r"@"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+"
    r"[A-Za-z]{2,63}$"
)


def is_valid_email(email: str) -> bool:
    """Return whether a string appears to be a valid email address.

    Args:
        email: The email address string to validate.

    Returns:
        bool: True if the email has a valid format, otherwise False.

    Example:
        >>> is_valid_email("user@example.com")
        True
    """
    if not isinstance(email, str):
        return False

    candidate = email.strip()
    if not candidate:
        return False

    local_part, separator, domain_part = candidate.rpartition("@")
    if separator != "@" or not local_part or not domain_part:
        return False

    # Extra local-part checks to reject obvious invalid forms.
    if local_part.startswith(".") or local_part.endswith(".") or ".." in local_part:
        return False

    return EMAIL_PATTERN.fullmatch(candidate) is not None


if __name__ == "__main__":
    test_emails = [
        "user@example.com",
        "first.last+tag@sub.domain.org",
        "invalid-email",
        "no_at_symbol.com",
        "user@domain",
        "user..name@example.com",
    ]

    for value in test_emails:
        print(f"{value}: {is_valid_email(value)}")