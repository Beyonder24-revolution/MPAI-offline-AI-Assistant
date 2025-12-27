import time
from threading import Thread, Event

class SessionManager:
    def __init__(self, timeout_seconds=300):
        self.timeout = timeout_seconds
        self.last_active = time.time()
        self.locked = True
        self._stop_event = Event()
        self._thread = Thread(target=self._monitor)
        self._thread.daemon = True
        self._thread.start()

    def _monitor(self):
        while not self._stop_event.is_set():
            if not self.locked and (time.time() - self.last_active) > self.timeout:
                self.locked = True
                print("[SessionManager] Auto-locked due to inactivity.")
            time.sleep(1)

    def activity(self):
        self.last_active = time.time()
        if self.locked:
            print("[SessionManager] Unlock required.")

    def unlock(self, password, auth_function):
        if auth_function(password):
            self.locked = False
            self.last_active = time.time()
            print("[SessionManager] Unlocked successfully.")
            return True
        print("[SessionManager] Unlock failed.")
        return False

    def stop(self):
        self._stop_event.set()

import time
from threading import Thread, Event

class SessionManager:
    def __init__(self, timeout_seconds=300, emergency_password="EMERGENCY123"):
        self.timeout = timeout_seconds
        self.last_active = time.time()
        self.locked = True
        self.emergency_password = emergency_password
        self._stop_event = Event()
        self._thread = Thread(target=self._monitor)
        self._thread.daemon = True
        self._thread.start()

    def _monitor(self):
        while not self._stop_event.is_set():
            if not self.locked and (time.time() - self.last_active) > self.timeout:
                self.locked = True
                print("[SessionManager] Auto-locked due to inactivity.")
            time.sleep(1)

    def activity(self):
        self.last_active = time.time()
        if self.locked:
            print("[SessionManager] Unlock required.")

    def unlock(self, password, auth_function):
        # ✅ Emergency password check first
        if password == self.emergency_password:
            self.locked = False
            self.last_active = time.time()
            print("[SessionManager] Emergency unlock SUCCESS")
            return True

        # Normal unlock
        if auth_function(password):
            self.locked = False
            self.last_active = time.time()
            print("[SessionManager] Unlocked successfully.")
            return True

        print("[SessionManager] Unlock failed.")
        return False

    def stop(self):
        self._stop_event.set()
