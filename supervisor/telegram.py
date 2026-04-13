from typing import List, Dict, Any

class TelegramBot:
    def __init__(self, token: str):
        self.token = token
        self.base = f"https://api.telegram.org/bot{token}"

    def get_updates(self, offset: int, timeout: int = 10) -> List[Dict[str, Any]]:
        last_err = "unknown"
        for attempt in range(3):
            try:
                r = requests.get(
                    f"{self.base}/getUpdates",
                    params={"offset": offset, "timeout": timeout}, # Removed 'allowed_updates' limit
                    timeout=timeout + 5,
                )
                r.raise_for_status()
                data = r.json()
                if data.get("ok") is not True:
                    raise RuntimeError(f"Telegram getUpdates failed: {data}")
                return data.get("result") or []
            except Exception as e:
                last_err = repr(e)
                if attempt < 2:
                    import time
                    time.sleep(0.8 * (attempt + 1))
        raise RuntimeError(f"Telegram getUpdates failed after retries: {last_err}")

    def send_with_budget(self, chat_id: int, text: str) -> None:
        """Send message with budget tracking."""
        r = requests.post(
            f"{self.base}/sendMessage",
            json={"chat_id": chat_id, "text": text},
            timeout=5,
        )
        r.raise_for_status()

# Rest of the file stays the same...
