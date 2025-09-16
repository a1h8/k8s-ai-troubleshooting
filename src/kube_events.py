"""
Module to extract Kubernetes logs and events
"""
from kubernetes import client, config

def get_kube_events(namespace=None):
    """
    Retrieve Kubernetes events for a given namespace or all namespaces.
    """
    config.load_kube_config()
    v1 = client.CoreV1Api()
    if namespace:
        events = v1.list_namespaced_event(namespace)
    else:
        events = v1.list_event_for_all_namespaces()
    return events.items

def get_kube_logs(pod_name, namespace):
    """
    Retrieve logs for a specific pod in a namespace.
    """
    config.load_kube_config()
    v1 = client.CoreV1Api()
    return v1.read_namespaced_pod_log(pod_name, namespace)
