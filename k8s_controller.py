from kubernetes import client
from kubernetes import config

from config import (
    DEPLOYMENT_NAME,
    NAMESPACE
)

try:
    config.load_incluster_config()
except:
    config.load_kube_config()

apps = client.AppsV1Api()


def get_replicas():

    deployment = apps.read_namespaced_deployment(
        DEPLOYMENT_NAME,
        NAMESPACE
    )

    return deployment.spec.replicas


def scale_deployment(new_replicas):

    body = {
        "spec": {
            "replicas": new_replicas
        }
    }

    apps.patch_namespaced_deployment_scale(
        DEPLOYMENT_NAME,
        NAMESPACE,
        body
    )

    print(
        f"🚀 Deployment scaled to {new_replicas} replicas"
    )


def increase_cpu_limit():

    deployment = apps.read_namespaced_deployment(
        DEPLOYMENT_NAME,
        NAMESPACE
    )

    container = deployment.spec.template.spec.containers[0]

    container.resources = {
        "limits": {
            "cpu": "1000m"
        },
        "requests": {
            "cpu": "500m"
        }
    }

    apps.patch_namespaced_deployment(
        DEPLOYMENT_NAME,
        NAMESPACE,
        deployment
    )

    print(
        "🔥 CPU limits increased"
    )