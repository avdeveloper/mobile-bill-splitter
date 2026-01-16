# T-Mobile Bill Splitter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A CLI tool to parse T-Mobile PDF bills and fairly calculate how much each line owes. Perfect for families or groups sharing a T-Mobile family plan.

## Features

- 📊 **Fair Split**: Evenly divides base plan costs + add-a-line fees + taxes among all lines
- 👤 **Name Mapping**: Maps phone numbers to names for easy identification
- 📄 **CSV Export**: Generates CSV files for easy sharing and record-keeping
- 🔄 **One-time Charges**: Properly handles line-specific charges and one-time fees
- 🎯 **Automatic**: Detects bill format variations automatically

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/tmobile-bill-splitter.git
cd tmobile-bill-splitter
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Phone Names (Optional)

```bash
# Copy the example file
cp phone_names.txt.example phone_names.txt

# Edit with your phone numbers and names
# Format: 5551234567: Alice
```

### 4. Run the Script

```bash
# Make the script executable
chmod +x split_bill.sh

# Process a bill
./split_bill.sh YourBill.pdf
```

## Usage

### Easy Method (Recommended)

Use the wrapper script:

```bash
./split_bill.sh SummaryBillJan2026.pdf
```

If you have a `phone_names.txt` file in the same directory, it will automatically use it to show names instead of just phone numbers!

### With Custom Name Mapping File

You can specify a different mapping file:

```bash
./split_bill.sh SummaryBillJan2026.pdf my_custom_names.txt
```

### Manual Method

Or activate the virtual environment and run the Python script directly:

```bash
source venv/bin/activate
python3 split_bill.py SummaryBillJan2026.pdf
# Or with name mapping:
python3 split_bill.py SummaryBillJan2026.pdf phone_names.txt
```

## How It Works

The script parses your T-Mobile bill PDF and:

1. Extracts ALL plan charges (base plan + add-a-lines + taxes/fees)
2. Splits those charges evenly among all lines
3. Adds any line-specific services to each line's share
4. Calculates how much each line owes:
   - **Shared Plan Portion**: ALL plan costs divided evenly among all lines
   - **Line-Specific Services**: Services unique to that line (Scam Shield, hotspot add-ons, etc.)
   - **Total Owed**: Shared portion + line-specific services

## Phone Number to Name Mapping

Create a `phone_names.txt` file in the same directory with this format:

```
5551234567: Alice
5552345678: Bob
5553456789: Charlie
5554567890: Diana
5555678901: Eve
5556789012: Frank
5557890123: Grace
```

**Format**: `<10-digit phone number>: <Name>`

The script will automatically use this file if it exists, showing names in both the console output and CSV file.

## Output

The script generates:
- A CSV file named `<original_filename>_split.csv` with the breakdown
- Console output showing the per-line breakdown

### Example Output (with names)

```
Bill Date: Jan 13, 2026
Grand Total from Bill: $240.07

Results written to: SummaryBillJan2026_split.csv

Per-Line Breakdown:
Name            Phone Number       Shared Plans    Services     Total Owed
--------------------------------------------------------------------------------
Alice           (555) 123-4567     $  32.18      $  14.82     $  47.00
Bob             (555) 234-5678     $  32.18      $   0.00     $  32.18
Charlie         (555) 345-6789     $  32.18      $   0.00     $  32.18
Diana           (555) 456-7890     $  32.18      $   0.00     $  32.18
Eve             (555) 567-8901     $  32.18      $   0.00     $  32.18
Frank           (555) 678-9012     $  32.18      $   0.00     $  32.18
Grace           (555) 789-0123     $  32.18      $   0.00     $  32.18
--------------------------------------------------------------------------------
TOTAL:                                                          $ 240.07
```

### CSV Format

The generated CSV includes:
```csv
Name,Phone Number,Shared Plan Portion,Line-Specific Services,Total Owed
Alice,(555) 123-4567,$32.18,$14.82,$47.00
Bob,(555) 234-5678,$32.18,$0.00,$32.18
...
```

## Understanding the Charges

**Shared Plan Portion**: ALL plan costs split evenly among all 7 lines. In the Jan 2026 example:
- Base family plan: $120.00 (covers 4 lines)
- 3 add-a-lines at $20 each: $60.00
- Taxes & fees on plans: $45.25
- **Total to split**: $225.25 ÷ 7 = **$32.18 per line**

This means everyone pays the same base amount, regardless of whether they're an "included" line or an "add-a-line."

**Line-Specific Services**: Any services unique to that line:
- Scam Shield Premium: $4.00
- Additional hotspot data: $10.00
- International roaming packages
- etc.

**Total Owed**: Shared plan portion + line-specific services

In the example above:
- Most lines pay: $32.18 (just their share of plans)
- Alice pays: $32.18 + $14.82 (services) = $47.00

## Files

- `split_bill.py` - Main Python script
- `split_bill.sh` - Convenience wrapper script
- `phone_names.txt` - Phone number to name mapping (optional)
- `venv/` - Python virtual environment
- `README.md` - This file
- `*_split.csv` - Generated CSV files with bill splits

## Troubleshooting

### PyPDF2 not found
```bash
source venv/bin/activate
pip install PyPDF2
```

### Permission denied on wrapper script
```bash
chmod +x split_bill.sh
```

### Bill summary not found
Make sure you're using a T-Mobile bill PDF. The script is designed for T-Mobile "Simple Choice" family plans.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

```bash
# Clone the repo
git clone https://github.com/yourusername/tmobile-bill-splitter.git
cd tmobile-bill-splitter

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Privacy & Security

- **No data collection**: This script runs entirely locally on your machine
- **No internet connection required**: All processing happens offline
- **Your data stays private**: Bills and CSVs are automatically excluded from git via `.gitignore`

**Important**: Never commit your actual `phone_names.txt` file or bill PDFs to a public repository!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This is an unofficial tool and is not affiliated with or endorsed by T-Mobile. Use at your own risk. Always verify the calculations against your actual bill.

## Support

If you find this tool helpful, please star the repository! ⭐

For issues or questions, please [open an issue](https://github.com/yourusername/tmobile-bill-splitter/issues) on GitHub.
