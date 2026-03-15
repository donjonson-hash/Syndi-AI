#!/usr/bin/env python3
"""
Тестирование Кристины — AI-агента UX-дизайнера
"""

import asyncio
import sys
sys.path.insert(0, '/mnt/okcomputer/output/syndi')

from agents import get_kristina


async def test_kristina():
    kristina = get_kristina()
    user_id = "test_user_123"
    
    print("=" * 70)
    print("🤖 КРИСТИНА — AI-агент UX-дизайнер")
    print("=" * 70)
    
    # Информация об агенте
    info = kristina.get_info()
    print(f"""
┌──────────────────────────────────────────────────────────────────────┐
│  ID:          {info['id']:<50} │
│  Имя:         {info['name']:<50} │
│  Роль:        {info['role']:<50} │
├──────────────────────────────────────────────────────────────────────┤
│  🎯 Экспертиза:                                                      │""")
    
    for exp in info['expertise']:
        print(f"│     • {exp:<60} │")
    
    print(f"""├──────────────────────────────────────────────────────────────────────┤
│  🧠 Личность:                                                        │
│     {info['personality'][:58]:<58} │
└──────────────────────────────────────────────────────────────────────┘
""")
    
    print("=" * 70)
    print("💬 ТЕСТИРОВАНИЕ ОБЩЕНИЯ")
    print("=" * 70)
    
    # Тест 1: Приветствие
    print("\n📝 Тест 1: Приветствие")
    print("-" * 70)
    response = await kristina.process_message(user_id, "Привет! Я делаю стартап")
    print(f"👤 Пользователь: Привет! Я делаю стартап\n")
    print(f"🤖 Кристина:\n{response.content}")
    print(f"\n💡 Предложения: {response.suggestions}")
    
    # Тест 2: Вопрос об исследовании
    print("\n" + "=" * 70)
    print("📝 Тест 2: Вопрос об исследовании пользователей")
    print("-" * 70)
    response = await kristina.process_message(user_id, "Как провести исследование пользователей?")
    print(f"👤 Пользователь: Как провести исследование пользователей?\n")
    print(f"🤖 Кристина:\n{response.content}")
    
    # Тест 3: Прототипирование
    print("\n" + "=" * 70)
    print("📝 Тест 3: Вопрос о прототипировании")
    print("-" * 70)
    response = await kristina.process_message(user_id, "Нужно создать прототип для тестирования")
    print(f"👤 Пользователь: Нужно создать прототип для тестирования\n")
    print(f"🤖 Кристина:\n{response.content}")
    
    # Тест 4: Дизайн-система
    print("\n" + "=" * 70)
    print("📝 Тест 4: Вопрос о дизайн-системе")
    print("-" * 70)
    response = await kristina.process_message(user_id, "Стоит ли создавать дизайн-систему?")
    print(f"👤 Пользователь: Стоит ли создавать дизайн-систему?\n")
    print(f"🤖 Кристина:\n{response.content}")
    
    # Показываем историю
    print("\n" + "=" * 70)
    print("📜 ИСТОРИЯ СООБЩЕНИЙ")
    print("=" * 70)
    memory = kristina.get_memory(user_id)
    print(f"Всего сообщений: {len(memory.messages)}")
    for msg in memory.messages:
        role = "👤" if msg['role'] == 'user' else "🤖"
        content = msg['content'][:70] + "..." if len(msg['content']) > 70 else msg['content']
        print(f"{role} {msg['role']}: {content}")
    
    print("\n" + "=" * 70)
    print("✅ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_kristina())
