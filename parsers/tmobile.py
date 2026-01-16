"""
T-Mobile bill parser.

Parses T-Mobile Simple Choice family plan bills.
"""

import re
from .base import BaseBillParser


class TMobileBillParser(BaseBillParser):
    """Parser for T-Mobile bills (Simple Choice family plans)."""

    @property
    def network_name(self):
        return "T-Mobile"

    def parse_bill(self, text):
        """
        Parse T-Mobile bill text and extract relevant information.

        Supports both bill formats:
        - With "One-time charges" column
        - Without "One-time charges" column

        Args:
            text: Extracted text from the T-Mobile PDF bill

        Returns:
            dict: Bill data with standardized structure

        Raises:
            ValueError: If the bill cannot be parsed
        """
        lines_data = {}

        # Extract bill date
        bill_date_match = re.search(r'Bill issue date\s+(\w+ \d+, \d+)', text)
        bill_date = bill_date_match.group(1) if bill_date_match else "Unknown"

        # Extract total due
        total_match = re.search(r'TOTAL DUE\s+\$(\d+\.\d+)', text)
        total_due = float(total_match.group(1)) if total_match else 0.0

        # Find the summary table section
        # Handle two formats: with or without "One-time charges" column
        summary_section = re.search(
            r'THIS BILL SUMMARY.*?Line Type\s+Plans\s+Equipment\s+Services(?:\s+One-time charges)?\s+Total(.*?)DETAILED CHARGES',
            text, re.DOTALL
        )

        if not summary_section:
            raise ValueError(
                "Could not find T-Mobile bill summary section. "
                "Make sure this is a T-Mobile Simple Choice family plan bill."
            )

        summary_text = summary_section.group(1)

        # Parse each line (phone number) from the summary
        # The summary shows: Phone | Type | Plans | Equipment | Services | [One-time charges] | Total
        # Handle both formats: with and without one-time charges column
        # We capture services and one-time charges separately, then combine them
        line_pattern = r'\((\d+)\)\s+(\d{3}-\d{4})\s+Voice\s+\$(\d+\.\d+)\s+[-\$\d.]*\s+(?:\$(\d+\.\d+)|[-])(?:\s+(?:\$([\d.]+)|[-]))?\s+\$(\d+\.\d+)'

        for match in re.finditer(line_pattern, summary_text):
            area_code = match.group(1)
            number = match.group(2)
            phone = self.extract_phone_format(area_code, number)
            plans_charge = float(match.group(3))
            services_charge = float(match.group(4)) if match.group(4) else 0.0
            onetime_charge = float(match.group(5)) if match.group(5) else 0.0
            total_charge = float(match.group(6))

            lines_data[phone] = {
                'plans': plans_charge,
                'services': services_charge + onetime_charge,  # Combine services and one-time charges
                'total': total_charge
            }

        # Also get the Account line (handle both formats)
        account_pattern = r'Account\s+\$(\d+\.\d+)\s+[-\$\d.]*\s+[-\$\d.]*(?:\s+[-\$\d.]*)?\s+\$(\d+\.\d+)'
        account_match = re.search(account_pattern, summary_text)

        if account_match:
            account_plans = float(account_match.group(1))
            account_total = float(account_match.group(2))
            lines_data['Account'] = {
                'plans': account_plans,
                'services': 0.0,
                'total': account_total
            }

        bill_data = {
            'bill_date': bill_date,
            'total_due': total_due,
            'lines': lines_data
        }

        # Validate the parsed data
        self.validate_bill_data(bill_data)

        return bill_data
