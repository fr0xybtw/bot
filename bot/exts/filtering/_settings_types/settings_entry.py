from __future__ import annotations
from abc import abstractmethod
from typing import Any, Optional

from bot.exts.filtering._filter_context import FilterContext
from bot.exts.filtering._utils import FieldRequiring


class SettingsEntry(FieldRequiring):
    """
    A basic entry in the settings field appearing in every filter list and filter.

    For a filter list, this is the default setting for it. For a filter, it's an override of the default entry.
    """

    # Each subclass must define a name matching the entry name we're expecting to receive from the database.
    # Names must be unique across all filter lists.
    name = FieldRequiring.MUST_SET_UNIQUE

    # Each subclass must define a description of what the entry does, to be displayed in the UI.
    description = FieldRequiring.MUST_SET

    @abstractmethod
    def __init__(self, entry_data: Any):
        ...

    @classmethod
    def create(cls, entry_data: Optional[dict[str, Any]]) -> Optional[SettingsEntry]:
        """
        Returns a SettingsEntry object from `entry_data` if it holds any value, None otherwise.

        Use this method to create SettingsEntry objects instead of the init.
        The None value is significant for how a filter list iterates over its filters.
        """
        if entry_data is None:
            return None
        if hasattr(entry_data, "values") and not any(value is not None for value in entry_data.values()):
            return None

        return cls(entry_data)


class ValidationEntry(SettingsEntry):
    """A setting entry to validate whether the filter should be triggered in the given context."""

    @abstractmethod
    def triggers_on(self, ctx: FilterContext) -> bool:
        """Return whether the filter should be triggered with this setting in the given context."""
        ...


class ActionEntry(SettingsEntry):
    """A setting entry defining what the bot should do if the filter it belongs to is triggered."""

    @abstractmethod
    async def action(self, ctx: FilterContext) -> None:
        """Executes an action that should be taken when the filter this setting belongs to is triggered."""
        ...

    @abstractmethod
    def __or__(self, other: ActionEntry):
        """Combines two actions of the same type. Each type of action is executed once per filter."""
        ...
