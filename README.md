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

### OpenTelemetry support

This tool has OpenTelemetry support built-in. To use it, set the following environment variables on your service definition.

| Variable | Description | Example |
| --- | --- | --- |
|OTEL_EXPORTER_OTLP_ENDPOINT| OpenTelemetry endpoint | `http://192.168.1.1:4317` |
|OTEL_RESOURCE_ATTRIBUTES| Set attributes for OpenTelemetry, i.e. service name | `service.name=cluster-purger` |

## Credits

[![kitconcept GmbH](https://raw.githubusercontent.com/kitconcept/docker-stack-deploy/main/docs/kitconcept.png)](https://kitconcept.com)

## License

The project is licensed under [MIT License](./LICENSE)