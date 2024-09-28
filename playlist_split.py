import sys
import csv
import os
import re
import urllib.parse

def sanitize_filename(name):
    """Sanitize the playlist name to create a valid filename."""
    # Replace invalid filename characters with underscores
    return re.sub(r'[<>:"/\\|?*]', '_', name)

if len(sys.argv) != 2:
    print("Usage: python playlist_split.py input.csv")
    sys.exit(1)

input_csv = sys.argv[1]

playlist_data = {}

# Read the input CSV file and organize rows by 'Playlist name'
with open(input_csv, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames
    if 'Playlist name' not in fieldnames:
        print("Error: 'Playlist name' column not found in the CSV file.")
        sys.exit(1)
    for row in reader:
        playlist_name = row['Playlist name']
        if playlist_name not in playlist_data:
            playlist_data[playlist_name] = []
        playlist_data[playlist_name].append(row)

# Create the directory 'playlist-csvs' if it doesn't exist
output_dir = 'playlist-csvs'
os.makedirs(output_dir, exist_ok=True)

# Create a new CSV file for each unique 'Playlist name' in the directory
for playlist_name, rows in playlist_data.items():
    filename = sanitize_filename(playlist_name) + '.csv'
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Created file: {filepath}")

# Process each generated CSV file in 'playlist-csvs' directory
sanitized_dir = 'sanitized'
os.makedirs(sanitized_dir, exist_ok=True)

for filename in os.listdir(output_dir):
    if filename.endswith('.csv'):
        input_filepath = os.path.join(output_dir, filename)
        output_filepath = os.path.join(sanitized_dir, filename)
        with open(input_filepath, newline='', encoding='utf-8') as infile, \
             open(output_filepath, 'w', newline='', encoding='utf-8') as outfile:
            reader = csv.DictReader(infile)
            # Check if 'Track name' and 'Artist name' columns exist
            if 'Track name' not in reader.fieldnames or 'Artist name' not in reader.fieldnames:
                print(f"Error: 'Track name' or 'Artist name' column not found in {input_filepath}.")
                continue
            writer = csv.writer(outfile)
            # Write header for the new CSV
            writer.writerow(['Track name - Artist name', 'Search URL'])
            for row in reader:
                track_artist = f"{row['Track name']} - {row['Artist name']}"
                # Create the YouTube search URL
                query = urllib.parse.quote_plus(track_artist)
                search_url = f"https://www.youtube.com/results?search_query={query}"
                writer.writerow([track_artist, search_url])
        print(f"Created sanitized file: {output_filepath}")
