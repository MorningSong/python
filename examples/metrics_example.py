#!/usr/bin/env python
# Copyright 2024 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Example demonstrating how to fetch and display metrics from the Kubernetes
metrics-server using the Python client.

This example shows:
1. Fetching node metrics
2. Fetching pod metrics in a namespace
3. Fetching pod metrics across multiple namespaces
4. Filtering pod metrics by labels

Prerequisites:
- A running Kubernetes cluster with metrics-server installed
- kubectl configured to access the cluster
- The kubernetes Python client library installed
"""

from kubernetes import client, config, utils


def print_node_metrics(api_client):
    """Fetch and display node metrics."""
    print("\n" + "="*60)
    print("NODE METRICS")
    print("="*60)
    
    try:
        metrics = utils.get_nodes_metrics(api_client)
        
        print(f"Found {len(metrics.get('items', []))} nodes\n")
        
        for node in metrics.get('items', []):
            node_name = node['metadata']['name']
            timestamp = node.get('timestamp', 'N/A')
            window = node.get('window', 'N/A')
            usage = node.get('usage', {})
            
            print(f"Node: {node_name}")
            print(f"  Timestamp: {timestamp}")
            print(f"  Window: {window}")
            print(f"  CPU Usage: {usage.get('cpu', 'N/A')}")
            print(f"  Memory Usage: {usage.get('memory', 'N/A')}")
            print()
            
    except Exception as e:
        print(f"Error fetching node metrics: {e}")


def print_pod_metrics(api_client, namespace):
    """Fetch and display pod metrics for a namespace."""
    print("\n" + "="*60)
    print(f"POD METRICS IN NAMESPACE: {namespace}")
    print("="*60)
    
    try:
        metrics = utils.get_pods_metrics(api_client, namespace)
        
        print(f"Found {len(metrics.get('items', []))} pods\n")
        
        for pod in metrics.get('items', []):
            pod_name = pod['metadata']['name']
            timestamp = pod.get('timestamp', 'N/A')
            window = pod.get('window', 'N/A')
            
            print(f"Pod: {pod_name}")
            print(f"  Timestamp: {timestamp}")
            print(f"  Window: {window}")
            print(f"  Containers:")
            
            for container in pod.get('containers', []):
                container_name = container['name']
                usage = container.get('usage', {})
                print(f"    - {container_name}:")
                print(f"        CPU: {usage.get('cpu', 'N/A')}")
                print(f"        Memory: {usage.get('memory', 'N/A')}")
            print()
            
    except Exception as e:
        print(f"Error fetching pod metrics: {e}")


def print_filtered_pod_metrics(api_client, namespace, labels):
    """Fetch and display pod metrics filtered by labels."""
    print("\n" + "="*60)
    print(f"POD METRICS IN NAMESPACE: {namespace}")
    print(f"FILTERED BY LABELS: {labels}")
    print("="*60)
    
    try:
        metrics = utils.get_pods_metrics(api_client, namespace, labels)
        
        pods = metrics.get('items', [])
        print(f"Found {len(pods)} pods matching labels\n")
        
        for pod in pods:
            pod_name = pod['metadata']['name']
            print(f"Pod: {pod_name}")
            
            for container in pod.get('containers', []):
                container_name = container['name']
                usage = container.get('usage', {})
                print(f"  {container_name}: CPU={usage.get('cpu')}, Memory={usage.get('memory')}")
            print()
            
    except Exception as e:
        print(f"Error fetching filtered pod metrics: {e}")


def print_multi_namespace_metrics(api_client, namespaces):
    """Fetch and display pod metrics across multiple namespaces."""
    print("\n" + "="*60)
    print(f"POD METRICS ACROSS MULTIPLE NAMESPACES")
    print("="*60)
    
    try:
        all_metrics = utils.get_pods_metrics_in_all_namespaces(api_client, namespaces)
        
        for ns, result in all_metrics.items():
            print(f"\nNamespace: {ns}")
            
            if 'error' in result:
                print(f"  Error: {result['error']}")
            else:
                pod_count = len(result.get('items', []))
                print(f"  Pods: {pod_count}")
                
                # Calculate total resource usage for namespace
                total_containers = 0
                for pod in result.get('items', []):
                    total_containers += len(pod.get('containers', []))
                
                print(f"  Total containers: {total_containers}")
        
    except Exception as e:
        print(f"Error fetching multi-namespace metrics: {e}")


def main():
    """Main function to demonstrate metrics API usage."""
    # Load kubernetes configuration
    # This will use your current kubectl context
    config.load_kube_config()
    
    # Create API client
    api_client = client.ApiClient()
    
    print("\nKubernetes Metrics API Example")
    print("================================")
    print("\nThis example demonstrates fetching resource usage metrics")
    print("from the Kubernetes metrics-server.")
    print("\nNote: metrics-server must be installed in your cluster for this to work.")
    
    # Example 1: Fetch node metrics
    print_node_metrics(api_client)
    
    # Example 2: Fetch pod metrics in default namespace
    print_pod_metrics(api_client, 'default')
    
    # Example 3: Fetch pod metrics in kube-system namespace
    print_pod_metrics(api_client, 'kube-system')
    
    # Example 4: Fetch pod metrics with label filter
    # Uncomment and modify the label selector to match your pods
    # print_filtered_pod_metrics(api_client, 'default', 'app=nginx')
    
    # Example 5: Fetch metrics across multiple namespaces
    namespaces_to_query = ['default', 'kube-system']
    print_multi_namespace_metrics(api_client, namespaces_to_query)
    
    print("\n" + "="*60)
    print("Example completed successfully!")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
