"""
Network bill parsers package.

This package provides parsers for different mobile network bills.
Each parser extracts bill information in a standardized format.
"""

from .base import BaseBillParser
from .tmobile import TMobileBillParser

__all__ = ['BaseBillParser', 'TMobileBillParser']

# Registry of available parsers
AVAILABLE_PARSERS = {
    'tmobile': TMobileBillParser,
    't-mobile': TMobileBillParser,
}


def get_parser(network_name):
    """
    Get a parser instance for the specified network.

    Args:
        network_name: Name of the mobile network (e.g., 'tmobile', 'verizon')

    Returns:
        An instance of the appropriate parser class

    Raises:
        ValueError: If the network is not supported
    """
    network_key = network_name.lower().strip()

    if network_key not in AVAILABLE_PARSERS:
        available = ', '.join(sorted(set(AVAILABLE_PARSERS.keys())))
        raise ValueError(
            f"Unsupported network: '{network_name}'. "
            f"Available parsers: {available}"
        )

    parser_class = AVAILABLE_PARSERS[network_key]
    return parser_class()


def list_supported_networks():
    """
    List all supported mobile networks.

    Returns:
        List of supported network names
    """
    return sorted(set(AVAILABLE_PARSERS.keys()))
