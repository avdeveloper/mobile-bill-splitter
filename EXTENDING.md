# Extending to Support Other Mobile Networks

This guide explains how to add support for additional mobile networks (Verizon, AT&T, etc.) to the bill splitter.

## Architecture Overview

The bill splitter uses a plugin-based architecture:

```
parsers/
├── __init__.py          # Parser registry and factory
├── base.py              # Abstract base class
├── tmobile.py           # T-Mobile implementation
└── verizon.py           # Your new parser (example)
```

## Quick Start: Adding a New Network

### Step 1: Create Your Parser File

Create a new file in the `parsers/` directory named after your network:

```bash
touch parsers/verizon.py
```

### Step 2: Implement the Parser Class

Use this template:

```python
"""
Verizon bill parser.

Parses Verizon family plan bills.
"""

import re
from .base import BaseBillParser


class VerizonBillParser(BaseBillParser):
    """Parser for Verizon bills."""

    @property
    def network_name(self):
        return "Verizon"

    def parse_bill(self, text):
        """
        Parse Verizon bill text and extract relevant information.

        Args:
            text: Extracted text from the Verizon PDF bill

        Returns:
            dict: Bill data with standardized structure:
                {
                    'bill_date': str,
                    'total_due': float,
                    'lines': {
                        '(XXX) XXX-XXXX': {
                            'plans': float,
                            'services': float,
                            'total': float
                        },
                        'Account': {
                            'plans': float,
                            'services': float,
                            'total': float
                        }
                    }
                }

        Raises:
            ValueError: If the bill cannot be parsed
        """
        lines_data = {}

        # TODO: Extract bill date
        bill_date_match = re.search(r'Your Pattern Here', text)
        bill_date = bill_date_match.group(1) if bill_date_match else "Unknown"

        # TODO: Extract total due
        total_match = re.search(r'Your Pattern Here', text)
        total_due = float(total_match.group(1)) if total_match else 0.0

        # TODO: Find and parse the bill summary section
        # Look for a table or section that lists all lines with their charges

        # TODO: Parse each phone line
        # Extract: phone number, plan charges, services, total

        # TODO: Parse account-level charges (shared costs)

        bill_data = {
            'bill_date': bill_date,
            'total_due': total_due,
            'lines': lines_data
        }

        # Validate the parsed data
        self.validate_bill_data(bill_data)

        return bill_data
```

### Step 3: Register Your Parser

Edit `parsers/__init__.py` and add your parser:

```python
from .base import BaseBillParser
from .tmobile import TMobileBillParser
from .verizon import VerizonBillParser  # Add this line

__all__ = ['BaseBillParser', 'TMobileBillParser', 'VerizonBillParser']  # Add here

# Add to registry
AVAILABLE_PARSERS = {
    'tmobile': TMobileBillParser,
    't-mobile': TMobileBillParser,
    'verizon': VerizonBillParser,      # Add these lines
    'vzw': VerizonBillParser,          # Aliases are OK!
}
```

### Step 4: Test Your Parser

```bash
# List supported networks
python3 split_bill.py --list-networks

# Test with your bill
python3 split_bill.py MyVerizonBill.pdf --network verizon
```

## Implementation Guide

### Understanding the Data Structure

Your parser must return data in this exact format:

```python
{
    'bill_date': 'Jan 13, 2026',  # Human-readable date
    'total_due': 240.07,           # Total bill amount
    'lines': {
        '(555) 123-4567': {        # Phone number in (XXX) XXX-XXXX format
            'plans': 6.01,          # Plan charges for this line
            'services': 14.82,      # Services for this line
            'total': 20.83          # Total for this line
        },
        '(555) 234-5678': {
            'plans': 6.01,
            'services': 0.00,
            'total': 6.01
        },
        # ... more lines ...
        'Account': {                # Special entry for shared account costs
            'plans': 122.13,
            'services': 0.00,
            'total': 122.13
        }
    }
}
```

### Phone Number Formatting

Use the `extract_phone_format()` helper method:

```python
# If you have: area_code='555', number='123-4567'
phone = self.extract_phone_format('555', '123-4567')
# Returns: '(555) 123-4567'
```

### Tips for Writing Regex Patterns

1. **Start simple**: Get the basic structure working first
2. **Test incrementally**: Test each regex pattern separately
3. **Use multiline mode**: `re.DOTALL` for sections spanning multiple lines
4. **Handle variations**: Bills may have slight format differences month-to-month

### Example: Finding a Summary Table

```python
# T-Mobile example
summary_section = re.search(
    r'THIS BILL SUMMARY.*?Line Type\s+Plans\s+Equipment\s+Services\s+Total(.*?)DETAILED CHARGES',
    text, re.DOTALL
)
if not summary_section:
    raise ValueError("Could not find bill summary section")
summary_text = summary_section.group(1)
```

### Example: Parsing Phone Lines

```python
# Pattern to match: (555) 123-4567 Voice $6.01 - $14.82 $20.83
line_pattern = r'\((\d+)\)\s+(\d{3}-\d{4})\s+Voice\s+\$(\d+\.\d+)\s+[-\$\d.]*\s+(?:\$(\d+\.\d+)|[-])\s+\$(\d+\.\d+)'

for match in re.finditer(line_pattern, summary_text):
    area_code = match.group(1)
    number = match.group(2)
    phone = self.extract_phone_format(area_code, number)
    plans = float(match.group(3))
    services = float(match.group(4)) if match.group(4) else 0.0
    total = float(match.group(5))

    lines_data[phone] = {
        'plans': plans,
        'services': services,
        'total': total
    }
```

## Testing Your Parser

### 1. Unit Testing (Optional but Recommended)

Create a test file `test_parsers.py`:

```python
from parsers import get_parser

def test_verizon_parser():
    parser = get_parser('verizon')
    assert parser.network_name == "Verizon"

    # Test with sample bill text
    with open('sample_verizon_bill.pdf', 'rb') as f:
        # ... extract text and test
```

### 2. Manual Testing

```bash
# Test with your actual bill
python3 split_bill.py MyBill.pdf --network verizon phone_names.txt

# Verify:
# - All lines are detected
# - Totals add up correctly
# - Phone numbers are formatted properly
```

## Common Pitfalls

1. **Floating Point Precision**: Use `float()` for all money values
2. **Missing Account Entry**: Always include an 'Account' entry for shared costs
3. **Phone Format**: Always use `(XXX) XXX-XXXX` format
4. **Validation**: Call `self.validate_bill_data()` before returning
5. **Error Messages**: Provide clear error messages for parsing failures

## Real-World Example: T-Mobile Parser

See `parsers/tmobile.py` for a complete, working implementation. Key features:

- Handles two bill formats (with/without one-time charges column)
- Robust regex patterns
- Clear error messages
- Proper validation

## Contributing Your Parser

Once your parser is working:

1. Test it with multiple months of bills
2. Add documentation to this file
3. Submit a pull request to the main repository
4. Include sample output (with personal data redacted!)

## Need Help?

- Check the T-Mobile parser for reference: `parsers/tmobile.py`
- Look at the base class documentation: `parsers/base.py`
- Open an issue on GitHub with questions

## Network-Specific Notes

### Verizon
- Look for: "Account Summary", "Line Access Charges"
- May have different terminology for shared vs. line-specific

### AT&T
- Look for: "Wireless Charges", "Account Level"
- May separate plan and feature charges differently

### Sprint (now T-Mobile)
- Older Sprint bills may differ from T-Mobile format
- Consider creating a separate parser if format is significantly different

Happy parsing! 🎉
