from cluster_purger.config import settings
from cluster_purger.proxy import ProxyRouter
from cluster_purger.utils import generate_urls
from fastapi import Response

import httpx


router = ProxyRouter()

USER_AGENT = settings.get("USER_AGENT", default="Swarm Purger")


async def _do_request(
    client: httpx.AsyncClient, http_verb: str, url: str, headers: dict
):
    headers["user-agent"] = USER_AGENT
    return await client.request(method=http_verb, url=url, headers=headers)


@router.purge("/{path:path}")
async def purge_remote_url(path: str, response: Response):
    """Given a path, purge the url."""
    info = generate_urls(f"/{path}")
    body = {}
    async with httpx.AsyncClient() as client:
        for item in info:
            headers = {}
            http_verb = item.http_verb
            url = item.url
            if host := item.host:
                headers["Host"] = host
            proxy = await _do_request(
                client=client, http_verb=http_verb, url=url, headers=headers
            )
            key = f"{host}|{url}"
            body[key] = {"status_code": proxy.status_code, "body": proxy.content}
    # Return only the last response
    response.status_code = proxy.status_code
    response.body = key
    return response
