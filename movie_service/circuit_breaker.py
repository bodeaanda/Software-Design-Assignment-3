import asyncio
import time

class CircuitBreaker:
    def __init__(self, threshold: int = 3, recovery_timeout: float = 10.0):
        self.state = "CLOSED"       
        self.failures = 0
        self.threshold = threshold
        self.recovery_timeout = recovery_timeout
        self._opened_at = None

    async def call(self, fn):
        if self.state == "OPEN":
            if time.time() - self._opened_at >= self.recovery_timeout:
                print("[CircuitBreaker] HALF-OPEN — testing service...")
                self.state = "HALF-OPEN"
            else:
                raise Exception("Circuit OPEN — fallback activ")

        try:
            result = await fn()
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        print(f"[CircuitBreaker] Succes — state → CLOSED")
        self.failures = 0
        self.state = "CLOSED"

    def _on_failure(self):
        self.failures += 1
        print(f"[CircuitBreaker] Eșec #{self.failures}/{self.threshold}")
        if self.failures >= self.threshold:
            self.state = "OPEN"
            self._opened_at = time.time()
            print("[CircuitBreaker] OPEN — prea multe eșecuri!")

    @property
    def status(self):
        return self.state