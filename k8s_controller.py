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


def get_cpu_limit():

    deployment = apps.read_namespaced_deployment(
        DEPLOYMENT_NAME,
        NAMESPACE
    )

    cpu_limit = deployment.spec.template.spec.containers[
        0
    ].resources.limits["cpu"]

    if cpu_limit.endswith("m"):
        return int(cpu_limit.replace("m", "")) / 1000

    return float(cpu_limit)


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

    current_limit = container.resources.limits["cpu"]

    if current_limit.endswith("m"):
        current_limit = int(
            current_limit.replace("m", "")
        )

        new_limit = current_limit + 200

        container.resources.limits["cpu"] = (
            f"{new_limit}m"
        )

    apps.patch_namespaced_deployment(
        DEPLOYMENT_NAME,
        NAMESPACE,
        deployment
    )

    print(
        f"🔥 CPU limit increased to {new_limit}m"
    )