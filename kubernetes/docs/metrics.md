# Kubernetes Metrics API Support

This document describes how to use the metrics utilities in the Kubernetes Python client to access resource usage data from the metrics-server.

## Overview

The metrics utilities provide easy access to pod and node resource consumption data (CPU and memory) through the `metrics.k8s.io/v1beta1` API. This enables monitoring and autoscaling workflows directly from Python applications.

## Prerequisites

- A running Kubernetes cluster with [metrics-server](https://github.com/kubernetes-sigs/metrics-server) installed
- Kubernetes Python client library installed
- Appropriate RBAC permissions to access metrics API endpoints

## Installation

The metrics utilities are included in the `kubernetes.utils` module:

```python
from kubernetes import client, config, utils
```

## Quick Start

```python
from kubernetes import client, config, utils

# Load kubernetes configuration
config.load_kube_config()

# Create API client
api_client = client.ApiClient()

# Get node metrics
node_metrics = utils.get_nodes_metrics(api_client)
for node in node_metrics['items']:
    print(f"{node['metadata']['name']}: {node['usage']}")

# Get pod metrics in a namespace
pod_metrics = utils.get_pods_metrics(api_client, 'default')
for pod in pod_metrics['items']:
    print(f"Pod: {pod['metadata']['name']}")
    for container in pod['containers']:
        print(f"  {container['name']}: {container['usage']}")
```

## API Reference

### `get_nodes_metrics(api_client)`

Fetches current resource usage for all nodes in the cluster.

**Parameters:**
- `api_client` (kubernetes.client.ApiClient): Configured API client instance

**Returns:**
- dict: Response containing node metrics with structure:
  ```python
  {
      'kind': 'NodeMetricsList',
      'apiVersion': 'metrics.k8s.io/v1beta1',
      'items': [
          {
              'metadata': {'name': 'node-name', ...},
              'timestamp': '2024-01-01T00:00:00Z',
              'window': '30s',
              'usage': {'cpu': '100m', 'memory': '1Gi'}
          }
      ]
  }
  ```

**Raises:**
- `ApiException`: When the metrics server is unavailable or request fails

**Example:**
```python
metrics = utils.get_nodes_metrics(api_client)
for node in metrics['items']:
    name = node['metadata']['name']
    cpu = node['usage']['cpu']
    memory = node['usage']['memory']
    print(f"Node {name}: CPU={cpu}, Memory={memory}")
```

### `get_pods_metrics(api_client, namespace, label_selector=None)`

Fetches current resource usage for pods in a specific namespace.

**Parameters:**
- `api_client` (kubernetes.client.ApiClient): Configured API client instance
- `namespace` (str): Kubernetes namespace to query (required)
- `label_selector` (str, optional): Label selector to filter pods (e.g., `'app=nginx,env=prod'`)

**Returns:**
- dict: Response containing pod metrics with structure:
  ```python
  {
      'kind': 'PodMetricsList',
      'apiVersion': 'metrics.k8s.io/v1beta1',
      'items': [
          {
              'metadata': {'name': 'pod-name', 'namespace': 'default', ...},
              'timestamp': '2024-01-01T00:00:00Z',
              'window': '30s',
              'containers': [
                  {
                      'name': 'container-name',
                      'usage': {'cpu': '50m', 'memory': '512Mi'}
                  }
              ]
          }
      ]
  }
  ```

**Raises:**
- `ValueError`: When namespace is None or empty
- `ApiException`: When the metrics server is unavailable or request fails

**Examples:**
```python
# Get all pod metrics in namespace
metrics = utils.get_pods_metrics(api_client, 'default')

# Get pods matching labels
metrics = utils.get_pods_metrics(api_client, 'production', 'app=nginx')
metrics = utils.get_pods_metrics(api_client, 'prod', 'tier=frontend,env=staging')

# Process the results
for pod in metrics['items']:
    pod_name = pod['metadata']['name']
    for container in pod['containers']:
        container_name = container['name']
        cpu = container['usage']['cpu']
        memory = container['usage']['memory']
        print(f"{pod_name}/{container_name}: CPU={cpu}, Memory={memory}")
```

### `get_pods_metrics_in_all_namespaces(api_client, namespaces, label_selector=None)`

Fetches pod metrics across multiple namespaces.

**Parameters:**
- `api_client` (kubernetes.client.ApiClient): Configured API client instance
- `namespaces` (list of str): List of namespace names to query
- `label_selector` (str, optional): Label selector applied to all namespaces

**Returns:**
- dict: Maps namespace names to their metrics or error information:
  ```python
  {
      'namespace-1': {
          'kind': 'PodMetricsList',
          'items': [...]
      },
      'namespace-2': {
          'kind': 'Error',
          'error': 'error message'
      }
  }
  ```

**Example:**
```python
namespaces = ['default', 'kube-system', 'production']
all_metrics = utils.get_pods_metrics_in_all_namespaces(api_client, namespaces)

for ns, result in all_metrics.items():
    if 'error' in result:
        print(f"{ns}: ERROR - {result['error']}")
    else:
        pod_count = len(result.get('items', []))
        print(f"{ns}: {pod_count} pods")
```

## Complete Example

See [examples/metrics_example.py](../examples/metrics_example.py) for a complete working example that demonstrates:
- Fetching node metrics
- Fetching pod metrics in specific namespaces
- Using label selectors to filter pods
- Querying multiple namespaces
- Error handling

## Parsing Resource Values

The metrics API returns resource values as Kubernetes quantity strings (e.g., `"100m"` for CPU, `"1Gi"` for memory). You can parse these using the existing `parse_quantity` utility:

```python
from kubernetes import utils

cpu_value = utils.parse_quantity("100m")  # Returns Decimal('0.1')
memory_value = utils.parse_quantity("1Gi")  # Returns Decimal('1073741824')
```

## Common Use Cases

### Monitoring Resource Usage

```python
def monitor_namespace_resources(api_client, namespace):
    """Monitor total resource usage in a namespace."""
    metrics = utils.get_pods_metrics(api_client, namespace)
    
    total_cpu = 0
    total_memory = 0
    
    for pod in metrics['items']:
        for container in pod['containers']:
            cpu = utils.parse_quantity(container['usage']['cpu'])
            memory = utils.parse_quantity(container['usage']['memory'])
            total_cpu += cpu
            total_memory += memory
    
    print(f"Namespace {namespace}:")
    print(f"  Total CPU: {total_cpu} cores")
    print(f"  Total Memory: {total_memory / (1024**3):.2f} GiB")
```

### Finding Resource-Intensive Pods

```python
def find_high_cpu_pods(api_client, namespace, threshold_millicores=500):
    """Find pods using more than threshold CPU."""
    metrics = utils.get_pods_metrics(api_client, namespace)
    high_cpu_pods = []
    
    for pod in metrics['items']:
        pod_name = pod['metadata']['name']
        for container in pod['containers']:
            cpu_str = container['usage']['cpu']
            cpu_millicores = utils.parse_quantity(cpu_str) * 1000
            
            if cpu_millicores > threshold_millicores:
                high_cpu_pods.append({
                    'pod': pod_name,
                    'container': container['name'],
                    'cpu': cpu_str
                })
    
    return high_cpu_pods
```

### Comparing Usage Across Namespaces

```python
def compare_namespace_usage(api_client, namespaces):
    """Compare resource usage across namespaces."""
    all_metrics = utils.get_pods_metrics_in_all_namespaces(api_client, namespaces)
    
    for ns, result in all_metrics.items():
        if 'error' not in result:
            pod_count = len(result['items'])
            container_count = sum(len(pod['containers']) for pod in result['items'])
            print(f"{ns}: {pod_count} pods, {container_count} containers")
```

## Troubleshooting

### Metrics Server Not Available

If you get an error about metrics not being available:

```
ApiException: (404)
Reason: Not Found
```

This means metrics-server is not installed or not running. Install it using:

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

### Permission Denied

If you get a 403 Forbidden error, ensure your service account has permissions to access the metrics API:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: metrics-reader
rules:
- apiGroups: ["metrics.k8s.io"]
  resources: ["pods", "nodes"]
  verbs: ["get", "list"]
```

### Empty Results

If metrics return empty results, check that:
1. Pods/nodes are actually running in the namespace
2. Metrics-server has had time to collect data (usually 15-60 seconds after pod start)
3. Label selectors are correct if using filtering

## Additional Resources

- [Kubernetes Metrics Server Documentation](https://github.com/kubernetes-sigs/metrics-server)
- [Metrics API Design](https://github.com/kubernetes/design-proposals-archive/blob/main/instrumentation/resource-metrics-api.md)
- [HorizontalPodAutoscaler using metrics](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
