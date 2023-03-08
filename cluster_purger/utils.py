from .config import settings
from dataclasses import dataclass
from itertools import product

import dns.resolver


@dataclass
class PurgeInfo:
    host: str
    url: str
    http_verb: str


def name_for_resolution(service_name: str) -> str:
    """Name to be used for internal resolution."""
    mode = settings.get_fresh("MODE", "swarm")
    match mode:
        case "swarm":
            prefix = "tasks."
        case "compose":
            prefix = ""
        case other:
            # Should log
            prefix = ""
    return f"{prefix}{service_name}"


def resolve_service_name(service_name: str, scheme: str = "http") -> list[str]:
    """Resolve all the ip addresses of a service."""
    urls = []
    port = settings.get_fresh("SERVICE_PORT")
    port_suffix = f":{port}" if port else ""
    hostname = name_for_resolution(service_name)
    try:
        answers = dns.resolver.resolve(hostname)
    except dns.resolver.NoAnswer:
        answers = []
    for answer in answers:
        urls.append(f"{scheme}://{answer.address}{port_suffix}")
    return urls


def generate_urls(path: str, http_verb: str = "PURGE") -> list[PurgeInfo]:
    """Generate a list of urls to be purged."""
    service_name = settings.get("SERVICE_NAME")
    hostnames = settings.get_fresh("PUBLIC_SITES", default=[])
    if not hostnames:
        # Empty hostname will not add
        # the HOST header to the call
        hostnames = [""]
    urls = [f"{url}{path}" for url in resolve_service_name(service_name)]
    if not urls:
        # Error in name resolution
        return []
    verbs = [
        http_verb,
    ]
    info = [PurgeInfo(*info) for info in product(hostnames, urls, verbs)]
    return info
