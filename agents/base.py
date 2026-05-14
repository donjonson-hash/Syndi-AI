"""AI Agents Base Module — complete stubs for tests"""

from enum import Enum

class AgentRole(str, Enum):
    UX_DESIGNER = "ux_designer"
    DEVELOPER = "developer"
    ANALYST = "analyst"
    PRODUCT_MANAGER = "product_manager"
    MARKETING = "marketing"
    MENTOR = "mentor"
    GENERAL = "general"

class MessageType(str, Enum):
    TEXT = "text"
    ACTION = "action"
    THINKING = "thinking"
    CODE = "code"
    DESIGN = "design"
    ADVICE = "advice"
    QUESTION = "question"
    FEEDBACK = "feedback"

class AgentMemory:
    max_messages = 50

    def __init__(self, user_id: str = ""):
        self.user_id = user_id
        self.messages: list[dict] = []
        self.user_profile = None
        self.project_context = None

    def add_message(self, role: str, content: str, metadata: dict | None = None):
        self.messages.append({
            "role": role,
            "content": content,
            "metadata": metadata or {}
        })
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def get_context(self, limit: int = 5):
        return self.messages[-limit:]

    def clear(self):
        self.messages = []
        self.user_profile = None
        self.project_context = None

class AgentResponse:
    def __init__(self, content: str = "", message_type: MessageType = MessageType.TEXT,
                 suggestions: list | None = None, actions: list | None = None,
                 metadata: dict | None = None):
        self.text = content          # для совместимости
        self.content = content
        self.message_type = message_type
        self.suggestions = suggestions or []
        self.actions = actions or []
        self.metadata = metadata or {}

class AIAgent:
    def __init__(self, agent_id: str, name: str, role: AgentRole,
                 personality: str, expertise: list, system_prompt: str):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.personality = personality
        self.expertise = expertise
        self.system_prompt = system_prompt
        self.memory = AgentMemory(user_id=agent_id)
        self.total_conversations = 0

    def get_memory(self, user_id: str):
        return self.memory

    def get_info(self) -> dict:
        return {
            "id": self.agent_id,
            "name": self.name,
            "role": self.role.value,
            "personality": self.personality,
            "expertise": self.expertise
        }

    async def process_message(self, user_id: str, message: str, context=None) -> AgentResponse:
        """Асинхронная обработка сообщения (заглушка)"""
        self.total_conversations += 1
        return AgentResponse(content=f"Ответ на: {message}")

    async def process(self, message: str) -> AgentResponse:
        """Совместимость с test_kristina"""
        return await self.process_message("test_user", message)
