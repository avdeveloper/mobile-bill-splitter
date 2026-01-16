#!/usr/bin/env python3
"""
Mobile Bill Splitter
Parses mobile network PDF bills and calculates what each line owes.

Supports multiple mobile networks through a plugin architecture.
Default network: T-Mobile

Usage:
    python3 split_bill.py <pdf_file> [phone_names.txt] [--network NETWORK]

Examples:
    python3 split_bill.py Bill.pdf
    python3 split_bill.py Bill.pdf phone_names.txt
    python3 split_bill.py Bill.pdf --network tmobile
    python3 split_bill.py Bill.pdf phone_names.txt --network verizon
"""

import sys
import csv
import argparse
from pathlib import Path

try:
    import PyPDF2
except ImportError:
    print("Error: PyPDF2 is required. Install with:")
    print("  python3 -m venv venv")
    print("  source venv/bin/activate")
    print("  pip install -r requirements.txt")
    sys.exit(1)

try:
    from parsers import get_parser, list_supported_networks
except ImportError:
    print("Error: Could not import parsers module.")
    print("Make sure you're running from the project directory.")
    sys.exit(1)


def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file."""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text


def calculate_split(bill_data):
    """
    Calculate how much each line owes.

    How the split works:
    - ALL plan charges (base + add-a-lines + taxes/fees) are split evenly
    - Each line then pays their line-specific services on top of that

    Example from T-Mobile Jan 2026:
    - Base plan: $120 + 3×$20 add-a-lines = $180
    - Taxes & fees on plans: $45.25
    - Total shared: $225.25 ÷ 7 lines = $32.18 per line
    - Then add any line-specific services (Scam Shield, hotspot, etc.)
    """
    lines = bill_data['lines']

    # Get total plan charges (this includes ALL lines and taxes)
    # We need to sum all plan charges, not just the Account row
    total_plans = sum(data['plans'] for data in lines.values())

    # Count voice lines (exclude Account)
    voice_lines = {k: v for k, v in lines.items() if k != 'Account'}
    num_lines = len(voice_lines)

    if num_lines == 0:
        raise ValueError("No voice lines found in bill")

    # Split ALL plan charges evenly among all lines
    shared_per_line = total_plans / num_lines

    # Calculate what each line owes
    results = []
    for phone, data in voice_lines.items():
        # Line-specific services (Scam Shield, hotspot, etc.)
        line_specific = data['services']

        # Total = shared portion + line-specific services
        total_owed = shared_per_line + line_specific

        results.append({
            'phone': phone,
            'shared_plan_portion': shared_per_line,
            'line_specific_services': line_specific,
            'total_owed': total_owed
        })

    return results


def write_csv(results, bill_date, bill_total, output_file, phone_mapping=None, network_name=""):
    """Write results to CSV file."""
    phone_mapping = phone_mapping or {}

    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Name', 'Phone Number', 'Shared Plan Portion', 'Line-Specific Services', 'Total Owed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            phone = result['phone']
            name = phone_mapping.get(phone, '')
            writer.writerow({
                'Name': name,
                'Phone Number': phone,
                'Shared Plan Portion': f"${result['shared_plan_portion']:.2f}",
                'Line-Specific Services': f"${result['line_specific_services']:.2f}",
                'Total Owed': f"${result['total_owed']:.2f}"
            })

    network_info = f" ({network_name})" if network_name else ""
    print(f"\nBill Date: {bill_date}{network_info}")
    print(f"Grand Total from Bill: ${bill_total:.2f}")
    print(f"\nResults written to: {output_file}")
    print("\nPer-Line Breakdown:")
    print(f"{'Name':<15} {'Phone Number':<18} {'Shared Plans':<15} {'Services':<12} {'Total Owed':<12}")
    print("-" * 80)

    total_all = 0
    for result in results:
        phone = result['phone']
        name = phone_mapping.get(phone, 'Unknown')
        print(f"{name:<15} {phone:<18} ${result['shared_plan_portion']:>7.2f}      "
              f"${result['line_specific_services']:>7.2f}     ${result['total_owed']:>7.2f}")
        total_all += result['total_owed']

    print("-" * 80)
    print(f"{'TOTAL:':<15} {'':<18} {'':<15} {'':<12} ${total_all:>7.2f}")


def load_phone_mapping(mapping_file):
    """Load phone number to name mapping from file."""
    mapping = {}
    if not mapping_file or not Path(mapping_file).exists():
        return mapping

    with open(mapping_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or ':' not in line:
                continue
            phone_digits, name = line.split(':', 1)
            phone_digits = phone_digits.strip()
            name = name.strip()
            # Format as (XXX) XXX-XXXX
            if len(phone_digits) == 10:
                formatted = f"({phone_digits[:3]}) {phone_digits[3:6]}-{phone_digits[6:]}"
                mapping[formatted] = name

    return mapping


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Split mobile network family plan bills fairly among all lines.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  %(prog)s Bill.pdf
  %(prog)s Bill.pdf phone_names.txt
  %(prog)s Bill.pdf --network tmobile
  %(prog)s Bill.pdf phone_names.txt --network verizon

Supported networks:
  {', '.join(list_supported_networks())}
        """
    )

    parser.add_argument('pdf_file', nargs='?', help='Path to the bill PDF file')
    parser.add_argument('mapping_file', nargs='?', default=None,
                        help='Phone number to name mapping file (optional)')
    parser.add_argument('--network', '-n', default='tmobile',
                        help='Mobile network (default: tmobile)')
    parser.add_argument('--list-networks', action='store_true',
                        help='List supported networks and exit')

    args = parser.parse_args()

    # Validate that pdf_file is provided unless --list-networks
    if not args.list_networks and not args.pdf_file:
        parser.error('pdf_file is required unless using --list-networks')

    return args


def main():
    args = parse_arguments()

    # Handle --list-networks
    if args.list_networks:
        print("Supported mobile networks:")
        for network in list_supported_networks():
            print(f"  - {network}")
        sys.exit(0)

    # Validate PDF file exists
    pdf_file = args.pdf_file
    if not Path(pdf_file).exists():
        print(f"Error: File '{pdf_file}' not found")
        sys.exit(1)

    # Get the appropriate parser for the network
    try:
        parser = get_parser(args.network)
    except ValueError as e:
        print(f"Error: {e}")
        print(f"\nUse --list-networks to see supported networks")
        sys.exit(1)

    print(f"Processing: {pdf_file}")
    print(f"Network: {parser.network_name}")

    # Load phone to name mapping
    phone_mapping = load_phone_mapping(args.mapping_file)
    if phone_mapping:
        print(f"Loaded name mappings for {len(phone_mapping)} phone numbers")

    # Extract text from PDF
    text = extract_text_from_pdf(pdf_file)

    # Parse bill using network-specific parser
    try:
        bill_data = parser.parse_bill(text)
    except ValueError as e:
        print(f"\nError parsing bill: {e}")
        print(f"\nMake sure this is a {parser.network_name} bill.")
        sys.exit(1)

    # Calculate split
    results = calculate_split(bill_data)

    # Generate output filename
    output_file = Path(pdf_file).stem + "_split.csv"

    # Write to CSV
    write_csv(results, bill_data['bill_date'], bill_data['total_due'],
              output_file, phone_mapping, parser.network_name)


if __name__ == '__main__':
    main()
