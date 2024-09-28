# Playlist Splitter

Playlist CSV downloaded from TuneMyMusic can be used as `input.csv` to split 
into multiple CSV files.

First set of CSV files is just a CSV for each playlist. The second set is just
2 columns; Track Name - Artist Name | Search URL

The Search URL is a YouTube link for the search to quickly find a link to the
track on that row.

Run the script with `python playlist_split.py input.csv`