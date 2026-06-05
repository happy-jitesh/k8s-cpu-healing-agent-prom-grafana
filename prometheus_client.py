import requests

from config import PROMETHEUS_URL


def get_cpu_utilization():

    query = """
100 *
avg(
  rate(
    container_cpu_usage_seconds_total{
      namespace="prod",
      pod=~"cpu-demo-app-.*",
      container!="POD"
    }[1m]
  )
)
/
avg(
  kube_pod_container_resource_limits{
    namespace="prod",
    pod=~"cpu-demo-app-.*",
    resource="cpu"
  }
)
"""

    response = requests.get(
        f"{PROMETHEUS_URL}/api/v1/query",
        params={"query": query}
    )

    response.raise_for_status()

    result = response.json()["data"]["result"]

    if not result:
        return 0

    return float(result[0]["value"][1])