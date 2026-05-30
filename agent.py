import time

from config import CHECK_INTERVAL

from llm_client import ask_llm

from prometheus_client import get_cpu_usage

from k8s_controller import (
    get_replicas,
    scale_deployment,
    increase_cpu_limit
)

with open(
    "prompts/cpu_healing_prompt.txt"
) as f:

    PROMPT = f.read()


def controller():

    print(
        "\n🚀 AI CPU Healing Controller Started\n"
    )

    while True:

        try:

            print(
                "\n===================================="
            )

            print(
                "📊 Checking Deployment CPU Health"
            )

            print(
                "===================================="
            )

            cpu = get_cpu_usage()

            replicas = get_replicas()

            print(
                f"\n🔥 CPU Usage : {cpu}"
            )

            print(
                f"📦 Replicas : {replicas}"
            )

            prompt = f"""
Current CPU Usage: {cpu}

Current Replicas: {replicas}

{PROMPT}
"""

            print(
                "\n🧠 Consulting AI..."
            )

            decision = ask_llm(
                prompt
            )

            print(
                "\n🤖 AI Decision"
            )

            print(
                decision
            )

            if "SCALE_DEPLOYMENT" in decision:

                scale_deployment(
                    replicas + 1
                )

            elif "INCREASE_CPU_LIMIT" in decision:

                increase_cpu_limit()

            else:

                print(
                    "\n✅ Cluster healthy"
                )

        except Exception as e:

            print(
                f"\n❌ Error: {e}"
            )

        print(
            f"\n⏳ Waiting {CHECK_INTERVAL} seconds..."
        )

        time.sleep(
            CHECK_INTERVAL
        )


if __name__ == "__main__":
    controller()