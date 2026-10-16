def format_etag(version: int) -> str:
    return f'"{version}"'


def parse_etag_version(if_match: str) -> int:
    etag = if_match.strip()
    if etag.startswith("W/"):
        etag = etag[2:].strip()
    if len(etag) >= 2 and etag.startswith('"') and etag.endswith('"'):
        etag = etag[1:-1]
    return int(etag)
