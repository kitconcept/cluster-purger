# Varnish Cluster Purger

Tool to replicate a Purge request to all instances of Varnish in a cluster.

## Supported Clusters

* Docker Compose

* Docker Swarm


## Usage

### Docker Compose

Add a new service to a Docker Compose:

```yaml
  purger:
    image: ghcr.io/kitconcept/cluster-purger:latest
    ports:
      - "8000:80"
    environment:
      PURGER_MODE: "compose"
      PURGER_SERVICE_NAME: varnish
      PURGER_SERVICE_PORT: 80
      PURGER_PUBLIC_SITES: "['site.example.com', 'cms.example.com']"
```

This service exposes port `8000` on the local host (only for debugging purposes), and relies on the existence of another service called `varnish`.

To purge the `/de` path on Varnish, from another service in the same compose:

```python
import httpx

response = httpx.request(method="PURGE", url="http://purger/de")
```

To purge the `/de` path on Varnish, from the host, use:

```python
import httpx

response = httpx.request(method="PURGE", url="http://localhost:8000/de")
```

### Environment Variables

| Variable | Description | Example | Default |
| --- | --- | --- | --- |
|PURGER_MODE| Which type of cluster. Could be `compose` or `swarm` | `swarm` | `swarm` |
|PURGER_SERVICE_NAME| Varnish service name in the cluster | `varnish` |  |
|PURGER_SERVICE_PORT| Service port | `8080` | `80` |
|PURGER_PUBLIC_SITES| List of public hostnames to send in the Host header | `"['site.example.com', 'cms.example.com']"` |  |
