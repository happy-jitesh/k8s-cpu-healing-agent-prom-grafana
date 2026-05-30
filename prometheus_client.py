import requests

from config import PROMETHEUS_URL


def get_cpu_usage():

    query = """
sum(
rate(
container_cpu_usage_seconds_total{
namespace="prod",
pod=~"cpu-demo-app-.*"
}[1m]
))
"""

    response = requests.get(
        f"{PROMETHEUS_URL}/api/v1/query",
        params={"query": query}
    )

    result = response.json()["data"]["result"]

    if not result:
        return 0

    return float(result[0]["value"][1])