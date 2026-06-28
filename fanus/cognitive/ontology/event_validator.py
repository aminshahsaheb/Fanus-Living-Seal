"""
==========================================================
FANUS EVENT VALIDATOR
==========================================================

Validates complete semantic events before they enter the
Fanus Memory Layer.

Responsibilities
----------------
- Validate required fields
- Validate entity
- Validate semantic type
- Validate timestamp
- Validate payload

NO runtime logic.

NO mutation.

NO decision making.

==========================================================
"""

from fanus.cognitive.ontology.event_schema import (
    EVENT_SCHEMA,
    EVENT_ENTITIES,
)

from fanus.cognitive.ontology.semantic_types import (
    SEMANTIC_TYPE,
)


class EventValidationError(Exception):
    """Raised when an event violates the Fanus ontology."""
    pass


class EventValidator:

    @staticmethod
    def validate(event: dict) -> bool:

        if not isinstance(event, dict):
            raise EventValidationError(
                "Event must be a dictionary."
            )

        EventValidator._validate_required(event)
        EventValidator._validate_entity(event)
        EventValidator._validate_semantic_type(event)
        EventValidator._validate_timestamp(event)
        EventValidator._validate_payload(event)

        return True

    # --------------------------------------------------

    @staticmethod
    def _validate_required(event):

        required = EVENT_SCHEMA["required"]

        for field in required:

            if field not in event:
                raise EventValidationError(
                    f"Missing required field: {field}"
                )

    # --------------------------------------------------

    @staticmethod
    def _validate_entity(event):

        entity = event["entity"]

        if entity not in EVENT_ENTITIES:
            raise EventValidationError(
                f"Unknown entity: {entity}"
            )

    # --------------------------------------------------

    @staticmethod
    def _validate_semantic_type(event):

        semantic_type = event["semantic_type"]

        valid_types = set(SEMANTIC_TYPE.values())

        if semantic_type not in valid_types:
            raise EventValidationError(
                f"Unknown semantic type: {semantic_type}"
            )

    # --------------------------------------------------

    @staticmethod
    def _validate_timestamp(event):

        timestamp = event["timestamp"]

        if not isinstance(timestamp, (int, float)):
            raise EventValidationError(
                "Timestamp must be numeric."
            )

        if timestamp <= 0:
            raise EventValidationError(
                "Timestamp must be positive."
            )

    # --------------------------------------------------

    @staticmethod
    def _validate_payload(event):

        payload = event["payload"]

        if not isinstance(payload, dict):
            raise EventValidationError(
                "Payload must be a dictionary."
            )

    # --------------------------------------------------

    @staticmethod
    def is_valid(event):

        try:

            EventValidator.validate(event)

            return True

        except EventValidationError:

            return False
