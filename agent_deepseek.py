#!/usr/bin/env python3
"""
agent_deepseek.py — Autonomous DeepSeek Developer Agent for Syndi-AI

Terminal-based AI partner that can:
  - Chat about code and architecture
  - Read/write files in the project
  - Create commits, branches, PRs via GitHub API
  - Run shell commands (with confirmation)
  - Search and analyze the codebase

Usage:
    python agent_deepseek.py

Environment (.env):
    DEEPSEEK_API_KEY=sk-...
    GITHUB_TOKEN=ghp_...
    GITHUB_REPO=donjonson-hash/Syndi-AI
"""

import os
import sys
import json
import subprocess
import base64
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

# --- Load .env manually (no python-dotenv required) ---
def load_env(path=".env"):
    if Path(path).exists():
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())

load_env()

# --- Dependencies check ---
try:
    import requests
except ImportError:
    print("[ERROR] Install requests: pip install requests")
    sys.exit(1)

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
GITHUB_TOKEN     = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO      = os.environ.get("GITHUB_REPO", "donjonson-hash/Syndi-AI")
DEEPSEEK_URL     = "https://api.deepseek.com/v1/chat/completions"
GITHUB_API_URL   = "https://api.github.com"

COLOR = {
    "cyan":   "\033[96m",
    "green":  "\033[92m",
    "yellow": "\033[93m",
    "red":    "\033[91m",
    "bold":   "\033[1m",
    "reset":  "\033[0m",
}

def c(text, color): return f"{COLOR[color]}{text}{COLOR['reset']}"
def banner():
    print(c("""
 ╔═══════════════════════════════════════╗
 ║   DeepSeek Agent — Syndi-AI Partner   ║
 ║   GitHub: donjonson-hash/Syndi-AI     ║
 ╚═══════════════════════════════════════╝""", "cyan"))

# ─────────────────────────────────────────────
# GITHUB API HELPER
# ─────────────────────────────────────────────
class GitHubAPI:
    def __init__(self, token: str, repo: str):
        self.token = token
        self.repo  = repo
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }

    def _url(self, path):
        return f"{GITHUB_API_URL}/repos/{self.repo}{path}"

    def get_file(self, filepath: str, branch: str = "main") -> Optional[str]:
        r = requests.get(self._url(f"/contents/{filepath}"),
                         headers=self.headers, params={"ref": branch})
        if r.status_code == 200:
            data = r.json()
            return base64.b64decode(data["content"]).decode("utf-8"), data["sha"]
        return None, None

    def list_files(self, path: str = "", branch: str = "main") -> List[str]:
        r = requests.get(self._url(f"/contents/{path}"),
                         headers=self.headers, params={"ref": branch})
        if r.status_code == 200:
            return [item["path"] for item in r.json()]
        return []

    def create_or_update_file(self, filepath: str, content: str,
                               message: str, branch: str = "main") -> bool:
        _, sha = self.get_file(filepath, branch)
        encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")
        payload = {"message": message, "content": encoded, "branch": branch}
        if sha:
            payload["sha"] = sha
        r = requests.put(self._url(f"/contents/{filepath}"),
                         headers=self.headers, json=payload)
        return r.status_code in (200, 201)

    def create_branch(self, new_branch: str, from_branch: str = "main") -> bool:
        r = requests.get(self._url(f"/git/ref/heads/{from_branch}"), headers=self.headers)
        if r.status_code != 200:
            return False
        sha = r.json()["object"]["sha"]
        r2 = requests.post(self._url("/git/refs"), headers=self.headers,
                           json={"ref": f"refs/heads/{new_branch}", "sha": sha})
        return r2.status_code == 201

    def create_pr(self, title: str, body: str, head: str, base: str = "main") -> Optional[str]:
        r = requests.post(self._url("/pulls"), headers=self.headers,
                          json={"title": title, "body": body, "head": head, "base": base})
        if r.status_code == 201:
            return r.json()["html_url"]
        return None

    def list_prs(self, state: str = "open") -> List[Dict]:
        r = requests.get(self._url("/pulls"),
                         headers=self.headers, params={"state": state})
        return r.json() if r.status_code == 200 else []

    def list_issues(self, state: str = "open") -> List[Dict]:
        r = requests.get(self._url("/issues"),
                         headers=self.headers, params={"state": state})
        return r.json() if r.status_code == 200 else []

    def create_issue(self, title: str, body: str) -> Optional[str]:
        r = requests.post(self._url("/issues"), headers=self.headers,
                          json={"title": title, "body": body})
        if r.status_code == 201:
            return r.json()["html_url"]
        return None

    def get_repo_info(self) -> Dict:
        r = requests.get(f"{GITHUB_API_URL}/repos/{self.repo}", headers=self.headers)
        return r.json() if r.status_code == 200 else {}

# ─────────────────────────────────────────────
# DEEPSEEK CHAT
# ─────────────────────────────────────────────
class DeepSeekAgent:
    SYSTEM_PROMPT = """Ты — автономный AI-разработчик внутри проекта Syndi-AI на GitHub (donjonson-hash/Syndi-AI).

Твои возможности:
- Анализируй код проекта, предлагай улучшения и рефакторинг.
- Пиши новые файлы, модули, тесты.
- Создавай ветки, коммиты и PR через GitHub API.
- Запускай shell-команды (только с подтверждением пользователя).
- Отслеживай issues и PRs.

Стиль работы:
- Отвечай по-русски, если пользователь пишет по-русски.
- Давай конкретный код, не только объяснения.
- Когда предлагаешь изменения в файле — пиши полный итоговый код.
- Всегда указывай путь к файлу при работе с кодом.

Доступные команды терминала (пиши [CMD] в начале строки):
  [CMD] read <file>         — прочитать файл из GitHub
  [CMD] write <file>        — записать/создать файл в GitHub
  [CMD] ls [path]           — список файлов
  [CMD] branch <name>       — создать ветку
  [CMD] pr <title>          — создать PR (текущая ветка → main)
  [CMD] prs                 — список открытых PRs
  [CMD] issues              — список открытых issues
  [CMD] issue <title>       — создать issue
  [CMD] shell <command>     — запустить shell-команду (с подтверждением)
  [CMD] status              — статус агента и репозитория
  [CMD] help                — список команд
  exit / quit               — выход"""

    def __init__(self, api_key: str, github: GitHubAPI):
        self.api_key  = api_key
        self.github   = github
        self.history: List[Dict] = []
        self.current_branch = "main"

    def chat(self, message: str) -> str:
        self.history.append({"role": "user", "content": message})
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": self.SYSTEM_PROMPT},
                *self.history[-40:],
            ],
            "temperature": 0.7,
            "max_tokens": 4096,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        try:
            r = requests.post(DEEPSEEK_URL, headers=headers, json=payload, timeout=60)
            r.raise_for_status()
            answer = r.json()["choices"][0]["message"]["content"]
        except requests.exceptions.Timeout:
            answer = "[ERROR] Timeout — DeepSeek API не ответил за 60 сек."
        except Exception as e:
            answer = f"[ERROR] {e}"
        self.history.append({"role": "assistant", "content": answer})
        return answer

    def self_test(self) -> Dict[str, Any]:
        """Полный тест агента: API, GitHub, права."""
        results = {}

        # 1. DeepSeek API
        print(c("  → Тестирую DeepSeek API...", "yellow"))
        try:
            reply = self.chat("Ответь одним словом: OK")
            results["deepseek_api"] = "✅ OK" if reply and "ERROR" not in reply else f"❌ {reply}"
        except Exception as e:
            results["deepseek_api"] = f"❌ {e}"

        # 2. GitHub токен
        print(c("  → Тестирую GitHub Token...", "yellow"))
        try:
            info = self.github.get_repo_info()
            if info.get("full_name"):
                results["github_token"] = f"✅ Repo: {info['full_name']} | Stars: {info.get('stargazers_count', 0)}"
            else:
                results["github_token"] = "❌ Нет доступа к репозиторию"
        except Exception as e:
            results["github_token"] = f"❌ {e}"

        # 3. Чтение файлов
        print(c("  → Тестирую чтение файлов...", "yellow"))
        try:
            content, sha = self.github.get_file("README.md")
            results["file_read"] = "✅ OK" if content else "❌ Не удалось прочитать README.md"
        except Exception as e:
            results["file_read"] = f"❌ {e}"

        # 4. Список файлов
        print(c("  → Тестирую листинг файлов...", "yellow"))
        try:
            files = self.github.list_files()
            results["file_list"] = f"✅ {len(files)} файлов найдено"
        except Exception as e:
            results["file_list"] = f"❌ {e}"

        return results

# ─────────────────────────────────────────────
# COMMAND PARSER
# ─────────────────────────────────────────────
def handle_command(cmd: str, agent: DeepSeekAgent) -> str:
    parts = cmd.strip().split(" ", 2)
    command = parts[0].lower()

    if command == "help":
        return c("""
Доступные команды:
  read <file>         — прочитать файл из репо
  write <file>        — записать файл (контент введи после команды)
  ls [path]           — список файлов
  branch <name>       — создать ветку
  pr <title>          — создать PR
  prs                 — список PR
  issues              — список issues
  issue <title>       — создать issue
  shell <cmd>         — shell-команда
  status              — статус агента
  test                — самотест агента""", "cyan")

    elif command == "status":
        info = agent.github.get_repo_info()
        return c(f"""
Агент активен ✅
DeepSeek API: {'✅ настроен' if agent.api_key else '❌ не задан'}
GitHub Token: {'✅ настроен' if agent.github.token else '❌ не задан'}
Репозиторий:  {info.get('full_name', 'N/A')}
Ветка:        {agent.current_branch}
История чата: {len(agent.history)} сообщений""", "green")

    elif command == "test":
        print(c("\n🔬 Запуск самотеста...", "bold"))
        results = agent.self_test()
        out = [c("\n📊 Результаты теста:", "bold")]
        for key, val in results.items():
            out.append(f"  {key:20s}: {val}")
        return "\n".join(out)

    elif command == "ls":
        path = parts[1] if len(parts) > 1 else ""
        files = agent.github.list_files(path, agent.current_branch)
        if not files:
            return c("Файлы не найдены", "yellow")
        return "\n".join([c("Файлы в репозитории:", "bold")] + [f"  {f}" for f in files])

    elif command == "read":
        if len(parts) < 2:
            return c("Укажи путь: read <file>", "yellow")
        content, sha = agent.github.get_file(parts[1], agent.current_branch)
        if content:
            return c(f"=== {parts[1]} (SHA: {sha[:7]}) ===", "bold") + "\n" + content
        return c(f"Файл не найден: {parts[1]}", "red")

    elif command == "write":
        if len(parts) < 2:
            return c("Укажи путь: write <file>", "yellow")
        filepath = parts[1]
        print(c(f"Введи содержимое файла (закончи строкой '###END'):", "yellow"))
        lines = []
        while True:
            line = input()
            if line.strip() == "###END":
                break
            lines.append(line)
        content = "\n".join(lines)
        msg = input(c("Сообщение коммита: ", "cyan"))
        ok = agent.github.create_or_update_file(filepath, content, msg or f"Update {filepath}", agent.current_branch)
        return c(f"✅ Файл '{filepath}' сохранён", "green") if ok else c(f"❌ Ошибка записи {filepath}", "red")

    elif command == "branch":
        if len(parts) < 2:
            return c("Укажи имя: branch <name>", "yellow")
        name = parts[1]
        ok = agent.github.create_branch(name, agent.current_branch)
        if ok:
            agent.current_branch = name
            return c(f"✅ Ветка '{name}' создана и активна", "green")
        return c(f"❌ Не удалось создать ветку '{name}'", "red")

    elif command == "pr":
        title = " ".join(parts[1:]) if len(parts) > 1 else f"PR from {agent.current_branch}"
        body = input(c("Описание PR (Enter для пропуска): ", "cyan"))
        url = agent.github.create_pr(title, body, agent.current_branch)
        return c(f"✅ PR создан: {url}", "green") if url else c("❌ Ошибка создания PR", "red")

    elif command == "prs":
        prs = agent.github.list_prs()
        if not prs:
            return c("Нет открытых PR", "yellow")
        out = [c("Открытые PR:", "bold")]
        for pr in prs:
            out.append(f"  #{pr['number']} {pr['title']} [{pr['user']['login']}]")
        return "\n".join(out)

    elif command == "issues":
        issues = agent.github.list_issues()
        if not issues:
            return c("Нет открытых issues", "yellow")
        out = [c("Открытые Issues:", "bold")]
        for iss in issues:
            out.append(f"  #{iss['number']} {iss['title']}")
        return "\n".join(out)

    elif command == "issue":
        title = " ".join(parts[1:]) if len(parts) > 1 else ""
        if not title:
            title = input(c("Заголовок issue: ", "cyan"))
        body = input(c("Описание (Enter для пропуска): ", "cyan"))
        url = agent.github.create_issue(title, body)
        return c(f"✅ Issue создан: {url}", "green") if url else c("❌ Ошибка создания issue", "red")

    elif command == "shell":
        if len(parts) < 2:
            return c("Укажи команду: shell <cmd>", "yellow")
        shell_cmd = " ".join(parts[1:])
        confirm = input(c(f"⚠️  Запустить: '{shell_cmd}'? [y/N]: ", "yellow"))
        if confirm.lower() != "y":
            return c("Отменено", "yellow")
        try:
            result = subprocess.run(shell_cmd, shell=True, capture_output=True,
                                    text=True, timeout=30)
            out = result.stdout or result.stderr or "(нет вывода)"
            return c(f"$ {shell_cmd}", "bold") + "\n" + out
        except subprocess.TimeoutExpired:
            return c("Timeout (30 сек)", "red")
        except Exception as e:
            return c(f"Ошибка: {e}", "red")

    return c(f"Неизвестная команда: {command}. Введи 'help' для справки.", "yellow")

# ─────────────────────────────────────────────
# MAIN LOOP
# ─────────────────────────────────────────────
def main():
    banner()

    if not DEEPSEEK_API_KEY:
        print(c("[WARN] DEEPSEEK_API_KEY не задан! Создай .env с ключом.", "red"))
    if not GITHUB_TOKEN:
        print(c("[WARN] GITHUB_TOKEN не задан! GitHub-функции недоступны.", "red"))

    github = GitHubAPI(GITHUB_TOKEN, GITHUB_REPO)
    agent  = DeepSeekAgent(DEEPSEEK_API_KEY, github)

    print(c(f"\nРепозиторий: {GITHUB_REPO}  |  Ветка: main", "green"))
    print(c("Команды: help | test | ls | read | write | branch | pr | shell | exit", "cyan"))
    print(c("Или просто пиши — агент ответит на любой вопрос по проекту.", "cyan"))
    print()

    # Авто-тест при запуске
    print(c("🔬 Запуск автотеста при старте...", "bold"))
    results = agent.self_test()
    for key, val in results.items():
        print(f"  {key:20s}: {val}")
    print()

    while True:
        try:
            user_input = input(c("You> ", "bold")).strip()
        except (KeyboardInterrupt, EOFError):
            print(c("\nВыход. До встречи!", "cyan"))
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit", "выход"):
            print(c("Выход. До встречи!", "cyan"))
            break

        # Обработка команд
        if user_input.lower().startswith(("read ", "write ", "ls", "branch ",
                                          "pr ", "prs", "issues", "issue ",
                                          "shell ", "status", "test", "help")):
            result = handle_command(user_input, agent)
            print(result)
        else:
            # AI чат с контекстом репозитория
            print(c("Agent> ", "cyan"), end="", flush=True)
            reply = agent.chat(user_input)
            print(reply)
        print()

if __name__ == "__main__":
    main()
