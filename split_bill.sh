#!/bin/bash
# Convenience wrapper for split_bill.py

# Change to script directory
cd "$(dirname "$0")"

# Check if phone_names.txt exists and append it to args if user didn't specify it
if [ $# -eq 1 ] && [ -f "phone_names.txt" ]; then
    # User provided only PDF file, auto-add phone_names.txt if it exists
    source venv/bin/activate && python3 split_bill.py "$1" phone_names.txt
else
    # User provided both args or phone_names.txt doesn't exist
    source venv/bin/activate && python3 split_bill.py "$@"
fi
