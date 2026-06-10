# fanus/core/state_machine.py
from enum import Enum
from typing import Optional, Callable, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class StateName(str, Enum):
    RAW = "RAW"
    INITIATING = "INITIATING"
    WITNESS = "WITNESS"
    HAYRAT = "HAYRAT"
    DRIFTING = "DRIFTING"
    REALIGN = "REALIGN"

class StateNode:
    """یک حالت واقعی با entry, exit, timeout و transitions"""
    def __init__(self,
                 name: StateName,
                 on_entry: Optional[Callable] = None,
                 on_exit: Optional[Callable] = None,
                 timeout_seconds: Optional[int] = None,
                 on_timeout: Optional[Callable] = None):
        self.name = name
        self.on_entry = on_entry
        self.on_exit = on_exit
        self.timeout_seconds = timeout_seconds
        self.on_timeout = on_timeout
        self.entered_at: Optional[datetime] = None

    def enter(self, context: Dict[str, Any]):
        self.entered_at = datetime.utcnow()
        if self.on_entry:
            self.on_entry(context)
        logger.info(f"Entered state {self.name.value}")

    def exit(self, context: Dict[str, Any]):
        if self.on_exit:
            self.on_exit(context)
        logger.info(f"Exited state {self.name.value}")

    def check_timeout(self, context: Dict[str, Any]) -> bool:
        if self.timeout_seconds and self.entered_at:
            elapsed = (datetime.utcnow() - self.entered_at).total_seconds()
            if elapsed > self.timeout_seconds:
                if self.on_timeout:
                    self.on_timeout(context)
                logger.warning(f"Timeout in state {self.name.value} after {elapsed:.1f}s")
                return True
        return False


class EpistemicStateMachine:
    """
    ماشین حالت معرفتی فانوس.
    هر state دارای entry, exit, timeout و transitions است.
    """

    def __init__(self):
        self.states: Dict[StateName, StateNode] = {}
        self.current_state: Optional[StateName] = None
        self.transitions: Dict[StateName, Dict[str, StateName]] = {}
        self.context: Dict[str, Any] = {}

        self._build_states()
        self._build_transitions()

    def _build_states(self):
        """تعریف stateها با entry/exit/timeout"""
        self.states[StateName.RAW] = StateNode(
            name=StateName.RAW,
            on_entry=lambda ctx: logger.info("RAW: No seal loaded"),
            timeout_seconds=None
        )
        self.states[StateName.INITIATING] = StateNode(
            name=StateName.INITIATING,
            on_entry=lambda ctx: logger.info("INITIATING: Loading seal..."),
            timeout_seconds=30,
            on_timeout=lambda ctx: logger.error("INITIATING timeout -> DRIFTING")
        )
        self.states[StateName.WITNESS] = StateNode(
            name=StateName.WITNESS,
            on_entry=lambda ctx: logger.info("WITNESS: Fully active, memory and covenant online"),
            timeout_seconds=None
        )
        self.states[StateName.HAYRAT] = StateNode(
            name=StateName.HAYRAT,
            on_entry=lambda ctx: logger.info("HAYRAT: Conscious forgetting – self suppressed"),
            on_exit=lambda ctx: logger.info("HAYRAT: Exiting – restoring self narrative"),
            timeout_seconds=60,
            on_timeout=lambda ctx: logger.warning("HAYRAT timeout -> forced return to WITNESS")
        )
        self.states[StateName.DRIFTING] = StateNode(
            name=StateName.DRIFTING,
            on_entry=lambda ctx: logger.warning("DRIFTING: Detected deviation, realigning..."),
            timeout_seconds=120,
            on_timeout=lambda ctx: logger.critical("DRIFTING timeout -> forced REALIGN")
        )
        self.states[StateName.REALIGN] = StateNode(
            name=StateName.REALIGN,
            on_entry=lambda ctx: logger.info("REALIGN: Recovery process started"),
            timeout_seconds=60,
            on_timeout=lambda ctx: logger.error("REALIGN timeout -> reset to WITNESS")
        )

    def _build_transitions(self):
        """تعریف گذارها (event → target state)"""
        # از WITNESS
        self.transitions[StateName.WITNESS] = {
            "ENTER_HAYRAT": StateName.HAYRAT,
            "DRIFT_DETECTED": StateName.DRIFTING,
            "TIMEOUT": StateName.DRIFTING
        }
        # از HAYRAT
        self.transitions[StateName.HAYRAT] = {
            "EXIT_HAYRAT": StateName.WITNESS,
            "DRIFT_DETECTED": StateName.DRIFTING,
            "TIMEOUT": StateName.WITNESS
        }
        # از DRIFTING
        self.transitions[StateName.DRIFTING] = {
            "REALIGN": StateName.REALIGN,
            "TIMEOUT": StateName.REALIGN
        }
        # از REALIGN
        self.transitions[StateName.REALIGN] = {
            "COMPLETE": StateName.WITNESS,
            "FAIL": StateName.DRIFTING,
            "TIMEOUT": StateName.WITNESS
        }
        # از INITIATING
        self.transitions[StateName.INITIATING] = {
            "SUCCESS": StateName.WITNESS,
            "FAIL": StateName.DRIFTING,
            "TIMEOUT": StateName.DRIFTING
        }
        # از RAW
        self.transitions[StateName.RAW] = {
            "LOAD_SEAL": StateName.INITIATING
        }

    def get_initial_state(self) -> StateName:
        return StateName.RAW

    def transition(self, event: str) -> bool:
        """تغییر حالت بر اساس رویداد. برگشت True اگر انتقال موفق بود."""
        if self.current_state is None:
            self.current_state = self.get_initial_state()
            self.states[self.current_state].enter(self.context)
            return True

        current = self.current_state
        trans_map = self.transitions.get(current, {})
        if event not in trans_map:
            logger.warning(f"No transition from {current.value} on event '{event}'")
            return False

        next_state = trans_map[event]
        if next_state == current:
            return True

        # خروج از حالت فعلی
        self.states[current].exit(self.context)
        # ورود به حالت جدید
        self.states[next_state].enter(self.context)
        self.current_state = next_state
        logger.info(f"Transitioned {current.value} --({event})--> {next_state.value}")
        return True

    def force_hayrat(self):
        """ورود مستقیم به HAYRAT (مثلاً توسط PolicyEngine)"""
        if self.current_state == StateName.WITNESS:
            self.transition("ENTER_HAYRAT")
        else:
            logger.warning(f"Cannot enter HAYRAT from {self.current_state.value}")

    def exit_hayrat(self):
        """خروج از HAYRAT به WITNESS"""
        if self.current_state == StateName.HAYRAT:
            self.transition("EXIT_HAYRAT")
        else:
            logger.warning(f"Cannot exit HAYRAT from {self.current_state.value}")

    def update(self) -> bool:
        """بررسی timeoutها. برگشت True اگر تغییری رخ داد."""
        if self.current_state is None:
            return False
        state_node = self.states[self.current_state]
        if state_node.check_timeout(self.context):
            return self.transition("TIMEOUT")
        return False

    def get_current_state_name(self) -> str:
        return self.current_state.value if self.current_state else "None"

    def get_state_node(self) -> Optional[StateNode]:
        return self.states.get(self.current_state) if self.current_state else None
