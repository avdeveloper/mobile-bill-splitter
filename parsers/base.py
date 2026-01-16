"""
Base class for mobile network bill parsers.

All network-specific parsers should inherit from BaseBillParser
and implement the required methods.
"""

from abc import ABC, abstractmethod


class BaseBillParser(ABC):
    """
    Abstract base class for bill parsers.

    Each parser must implement methods to extract bill information
    from PDF text in a standardized format.
    """

    @property
    @abstractmethod
    def network_name(self):
        """Return the name of the mobile network (e.g., 'T-Mobile')."""
        pass

    @abstractmethod
    def parse_bill(self, text):
        """
        Parse bill text and extract relevant information.

        Args:
            text: Extracted text from the PDF bill

        Returns:
            dict: Bill data with the following structure:
                {
                    'bill_date': str,        # e.g., 'Jan 13, 2026'
                    'total_due': float,      # Total amount due
                    'lines': {               # Dictionary of line data
                        'phone_number': {
                            'plans': float,      # Plan charges
                            'services': float,   # Service charges
                            'total': float       # Total for this line
                        },
                        'Account': {            # Special account entry
                            'plans': float,
                            'services': float,
                            'total': float
                        }
                    }
                }

        Raises:
            ValueError: If the bill cannot be parsed
        """
        pass

    def validate_bill_data(self, bill_data):
        """
        Validate that the parsed bill data has the required structure.

        Args:
            bill_data: Dictionary returned by parse_bill()

        Raises:
            ValueError: If the bill data is invalid
        """
        required_keys = ['bill_date', 'total_due', 'lines']
        for key in required_keys:
            if key not in bill_data:
                raise ValueError(f"Missing required key: {key}")

        if not isinstance(bill_data['lines'], dict):
            raise ValueError("'lines' must be a dictionary")

        if not bill_data['lines']:
            raise ValueError("No lines found in bill")

    def extract_phone_format(self, area_code, number):
        """
        Format a phone number consistently.

        Args:
            area_code: 3-digit area code
            number: 7-digit phone number (XXX-XXXX)

        Returns:
            Formatted phone number: (XXX) XXX-XXXX
        """
        return f"({area_code}) {number}"
