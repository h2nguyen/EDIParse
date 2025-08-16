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

import importlib
import inspect
import logging
import os
import pkgutil
from typing import Optional

from .group_state_resolver import GroupStateResolver

from ..mods.module_constants import EdifactMessageType

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
        self.__handlers: dict[str, GroupStateResolver] = {}
        self.__register_resolvers()

    def __register_resolvers(self) -> None:
        """
        Initialize and register the resolver dictionary with instances of all group state resolvers.
        """
        # Initialize handlers for each message type by discovering them in the mods folder
        self.__handlers = self.__discover_resolvers()

    @staticmethod
    def __discover_resolvers() -> dict[str, GroupStateResolver]:
        """
        Dynamically discover and instantiate all group state resolvers in the mods folder.

        Returns:
            A dictionary mapping message types to their respective group state resolver instances.
        """
        resolvers = {}

        # Get the path to the mods folder
        mods_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mods')

        # Iterate through all modules in the mods folder
        for _, mod_name, is_pkg in pkgutil.iter_modules([mods_path]):
            if is_pkg:
                # Check if this module has a group_state_resolver.py file
                resolver_filename = "group_state_resolver.py"
                resolver_path = os.path.join(mods_path, mod_name, resolver_filename)

                if os.path.exists(resolver_path):
                    try:
                        # Import the module
                        module_name = f"..mods.{mod_name}.group_state_resolver"
                        module = importlib.import_module(module_name, package=__package__)

                        # Find all classes in the module that inherit from GroupStateResolver
                        for name, obj in inspect.getmembers(module, inspect.isclass):
                            if issubclass(obj, GroupStateResolver) and obj != GroupStateResolver:
                                # Extract the message type from the class name
                                # The class name should follow the pattern <MessageType>GroupStateResolver
                                expected_suffix = "GroupStateResolver"
                                if name.endswith(expected_suffix):
                                    message_type_name = name.replace(expected_suffix, '')

                                    # Check if this message type is defined in the EdifactMessageType enum
                                    try:
                                        # Convert to uppercase to match the enum values
                                        message_type = EdifactMessageType(message_type_name.upper())
                                        # Instantiate the resolver and add it to the dictionary
                                        resolvers[message_type] = obj()
                                    except ValueError:
                                        logger.warning(
                                            f"Message type {message_type_name} not found in EdifactMessageType enum."
                                        )
                    except (ImportError, AttributeError) as e:
                        logger.warning(f"Error importing group state resolver for module {mod_name}: {e}.")

        return resolvers

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
