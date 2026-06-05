import time

from config import CHECK_INTERVAL

from llm_client import ask_llm

from prometheus_client import (
    get_cpu_usage
)

from k8s_controller import (
    get_replicas,
    get_cpu_limit,
    scale_deployment,


    increase_cpu_limit
)

# Prevent repeated actions
LAST_ACTION = None

with open(
    "prompts/cpu_healing_prompt.txt"
) as f:

    PROMPT = f.read()


def controller():

    global LAST_ACTION

    print(
        "\n🚀 AI CPU Healing Controller Started\n"
    )

    while True:

        try:

            print(
                "\n================================================"
            )

            print(
                "📊 Checking Deployment CPU Health"
            )

            print(
                "================================================"
            )

            # Get CPU Usage
            cpu_used = get_cpu_usage()

            # Get Deployment CPU Limit
            cpu_limit = get_cpu_limit()

            # Get Current Replicas
            replicas = get_replicas()

            # Calculate Utilization %
            cpu_percent = (
                cpu_used / cpu_limit
            ) * 100

            print(
                f"\n🔥 CPU Utilization : {cpu_percent:.2f}%"
            )

            print(
                f"⚙️ CPU Limit       : {cpu_limit} cores"
            )

            print(
                f"📦 Replicas        : {replicas}"
            )

            print(
                f"📝 Last Action     : {LAST_ACTION}"
            )

            # Build Prompt
            prompt = f"""
Deployment Name: cpu-demo-app

CPU Utilization: {cpu_percent:.2f}%

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
                "--------------------------------"
            )

            print(
                decision
            )

            print(
                "--------------------------------"
            )

            # SCALE_DEPLOYMENT
            if "SCALE_DEPLOYMENT" in decision:

                if LAST_ACTION == "SCALE_DEPLOYMENT":

                    print(
                        "\n Deployment already scaled recently"
                    )

                else:

                    print(
                        "\n🚀 Scaling deployment..."
                    )

                    scale_deployment(
                        replicas + 1
                    )

                    LAST_ACTION = "SCALE_DEPLOYMENT"

            # INCREASE_CPU_LIMIT
            elif "INCREASE_CPU_LIMIT" in decision:

                if LAST_ACTION == "INCREASE_CPU_LIMIT":

                    print(
                        "\n CPU limit already increased recently"
                    )

                else:

                    print(
                        "\n🔥 Increasing CPU limit..."
                    )

                    increase_cpu_limit()

                    LAST_ACTION = "INCREASE_CPU_LIMIT"

            # DO_NOTHING
            else:

                LAST_ACTION = None

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