# coding: utf-8
"""
Factory for creating EDIFACT segment group resolvers.

This module provides a factory class that creates and manages resolvers for different
EDIFACT message types. Each message type (MSCONS, APERAK, etc.) has its own segment
group structure and requires a specialized resolver to determine which segment group
a particular segment belongs to during parsing.

The factory pattern centralizes the creation of these resolvers and allows the parser
to dynamically select the appropriate resolver based on the message type being processed.
"""

import logging
from typing import Dict, Optional

from .group_state_resolver import GroupStateResolver

from ..wrappers.constants import EdifactMessageType

from ..mods.mscons.group_state_resolver import MsconsGroupStateResolver
from ..mods.aperak.group_state_resolver import AperakGroupStateResolver

logger = logging.getLogger(__name__)


class GroupStateResolverFactory:
    """
    Factory class for creating group resolvers.

    This factory maintains a registry of group resolvers and provides a method to
    retrieve the appropriate resolver for a given Edifact message type. It centralizes the
    creation and management of group resolvers, ensuring that each message type
    is processed by its specialized resolver.
    """

    def __init__(self):
        """
        Initialize the factory by registering all group state resolvers.

        This constructor creates a dictionary mapping an EDIFACT message type to their respective
        resolver instances, initializing each resolver with the provided syntax parser.

        """
        self.__handlers: Dict[str, GroupStateResolver] = {}
        self.__register_resolvers()

    def __register_resolvers(self) -> None:
        """
        Initialize and register the resolver dictionary with instances of all group state resolvers.
        """
        # Initialize handlers for each segment type
        self.__handlers = {
            EdifactMessageType.APERAK: AperakGroupStateResolver(),
            EdifactMessageType.MSCONS: MsconsGroupStateResolver(),
        }

    def get_resolver(self, message_type: EdifactMessageType) -> Optional[GroupStateResolver]:
        """
        Get the resolver for the specified edifact message type.

        Args:
            message_type: The message type to get a resolver for.

        Returns:
            The resolver for the edifact message type, or None if no resolver is found.
        """
        resolver = self.__handlers.get(message_type)
        if not resolver:
            logger.warning(f"No resolver found for EdifactMessageType '{message_type}'.")
        return resolver
