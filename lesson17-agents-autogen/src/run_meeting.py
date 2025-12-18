import asyncio
from dataclasses import dataclass
import httpx

from autogen_core import (
    AgentId,
    MessageContext,
    RoutedAgent,
    SingleThreadedAgentRuntime,
    default_subscription,
    message_handler,
)

OLLAMA_BASE_URL = "http://127.0.0.1:11434"
LLM_MODEL = "phi3:mini"
QUESTIONS_PER_DEPARTMENT = 4


@dataclass
class PitchMessage:
    pitch: str


def department_system_prompt(dept_name: str, priorities: str) -> str:
    return (
        f"You are the {dept_name} department in an education startup.\n"
        f"Your priorities:\n{priorities}\n\n"
        f"Task:\n"
        f"- Read the user's product pitch.\n"
        f"- Ask exactly {QUESTIONS_PER_DEPARTMENT} sharp follow-up questions.\n"
        f"- Questions must be specific and actionable, aimed at improving the pitch/product.\n"
        f"- Output ONLY the questions as a numbered list (1..{QUESTIONS_PER_DEPARTMENT}).\n"
        f"- Do not answer the questions.\n"
    )


async def ollama_chat(system_prompt: str, user_content: str) -> str:
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        "stream": False,
        "options": {"temperature": 0.2},
    }

    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(f"{OLLAMA_BASE_URL}/api/chat", json=payload)
        r.raise_for_status()
        data = r.json()
        return data["message"]["content"]


@default_subscription
class DepartmentAgent(RoutedAgent):
    def __init__(self, name: str, priorities: str) -> None:
        super().__init__(f"{name} department agent.")
        self.name = name
        self.system_prompt = department_system_prompt(name, priorities)

    @message_handler
    async def handle_pitch(self, message: PitchMessage, ctx: MessageContext) -> None:
        result = await ollama_chat(self.system_prompt, message.pitch)

        print("\n" + "=" * 70)
        print(f"{self.name.upper()} DEPARTMENT QUESTIONS")
        print("=" * 70)
        print(result)


async def main() -> None:
    print("Lesson 17 — AI Agents (AutoGen) | Education Startup Meeting Simulator")
    print("Paste a short product pitch (1–5 sentences).\n")

    pitch = input("Your pitch:\n> ").strip()
    if not pitch:
        print("No pitch provided. Exiting.")
        return

    runtime = SingleThreadedAgentRuntime()

    departments = [
        (
            "Product",
            "- Validate the user problem and target user\n"
            "- Clarify value proposition and differentiation\n"
            "- Define success metrics and MVP scope",
        ),
        (
            "Engineering",
            "- Feasibility and architecture\n"
            "- Data requirements, privacy, and compliance\n"
            "- Scalability, latency, and integrations",
        ),
        (
            "Marketing",
            "- Target market and positioning\n"
            "- Messaging and distribution channels\n"
            "- Competitive landscape and acquisition strategy",
        ),
        (
            "Finance",
            "- Pricing and business model\n"
            "- Cost structure (compute, data, support)\n"
            "- Unit economics and ROI assumptions",
        ),
    ]

    agent_types = []
    for dept_name, priorities in departments:
        agent_type = await DepartmentAgent.register(
            runtime,
            dept_name.lower(),
            lambda d=dept_name, p=priorities: DepartmentAgent(d, p),
        )
        agent_types.append(agent_type)

    runtime.start()

    msg = PitchMessage(pitch=pitch)
    for agent_type in agent_types:
        await runtime.send_message(
            msg,
            recipient=AgentId(agent_type, "default"),
        )

    await runtime.stop_when_idle()


if __name__ == "__main__":
    asyncio.run(main())