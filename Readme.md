
[![PyPI Version][pypi-image]][pypi-project-url]
[![PyPI Version Image][pypi-version-image]][pypi-project-url]

# KubeGen

[kubegen][pypi-url] is an utility ```python``` library on [PyPI][pypi-url]. It is use in generating kubernetes policy files. The library generate policy based on the `kind` specified.
It provides way of generating k8s policy files on the fly during CI/CD process.

:rotating_light:
## Features

- Supports creation of deployment, ingress and svc policy file
- Pass json string as argument 
- Dynamically bind environment variables, volumes etc.

# Installation

Installation is done using the
[`pip install` command](https://pypi.org/project/pip/):
```
   $ pip install kubegen
   $ pip3 install kubegen
```

### Usage:

```
Usage: kubegen [OPTIONS]

Options:
  -k, --kind TEXT  what kind of k8s policy file are you trying to create.
                   support type includes deployment, ingress and svc.

  -d, --data TEXT  Supply payload for the policy file in jsonstring format e.g
                   {"name": "app-1", "version": "v1"}

  --help           Show this message and exit.
```

```
// Generate svc policy file

kubegen -k svc -d '{"name": "test-app", "environment": "staging", "port": 8080, "service_type": "ClusterIP", "protocol": "TCP"}'
```

```
// Generate ingress policy file

kubegen -k svc -d '{"name": "test-app", "host": "test-app.io", "port": 8080, "path": "/",  "tls_secret_name": "test-app-secret", "annotations": {"kubernetes.io/ingress.class": "nginx", "nginx.ingress.kubernetes.io/ssl-redirect": "true"}}'
```

```
// Generate deployment policy file

kubegen -k deployment -d '{"version": "apps/v1", "name": "test-app", "image": "test-app:1.0.0", "port": 8080, "environment": "staging", "image_pull_secret": "test-app-secret", "environment_variables": [{"name": "keyvault_id", "value": "12345"}], "replicas": 3, "volume_mounts": [{"name": "test-volume", "mountPath": "/app/test-volume"}], "volumes": [{"name": "test-volume", "configMap": {"name": "app-configmap"}}]}'
```

[pypi-image]: https://img.shields.io/pypi/v/kubegen.svg
[pypi-project-url]: https://pypi.org/project/kubegen
[pypi-version-image]: https://img.shields.io/pypi/pyversions/kubegen.svg
[pypi-url]: https://pypi.org

