"""
Script to consolidate pages into Issue Tracker and create Route Optimizer
"""

# Read the original file
with open('courier_insights.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find line numbers for each page section
page_markers = []
for i, line in enumerate(lines):
    if 'elif page ==' in line or (i > 500 and 'if page ==' in line):
        page_markers.append((i, line.strip()))

print("Found page markers:")
for marker in page_markers:
    print(f"Line {marker[0]}: {marker[1]}")
