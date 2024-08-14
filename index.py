import pandas as pd
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

csv_file_path = 'accounts.csv'  # Path to your CSV file
md_file_path = 'table.md'       # Path to the output Markdown file

def csv_to_markdown(csv_file_path, md_file_path):
    # Read CSV file into DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Calculate the maximum width for each column
    max_widths = df.apply(lambda x: x.astype(str).map(len).max()).to_dict()
    
    # Include header lengths in the maximum widths
    for col in df.columns:
        max_widths[col] = max(max_widths[col], len(col))
    
    # Function to pad each cell content to align with the column width
    def pad_cell(text, width):
        return text.ljust(width)
    
    # Create Markdown table with aligned columns
    headers = df.columns
    markdown = f"| {' | '.join(pad_cell(header, max_widths[header]) for header in headers)} |\n"
    markdown += f"| {' | '.join('-' * max_widths[header] for header in headers)} |\n"
    
    for _, row in df.iterrows():
        markdown += f"| {' | '.join(pad_cell(str(row[header]), max_widths[header]) for header in headers)} |\n"
    
    # Write Markdown to file
    with open(md_file_path, 'w') as md_file:
        md_file.write(markdown)
    
    print('Markdown file updated.')

class CSVHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == csv_file_path:
            print(f'{csv_file_path} has been changed. Updating Markdown file...')
            csv_to_markdown(csv_file_path, md_file_path)

if __name__ == "__main__":
    # Initial conversion
    csv_to_markdown(csv_file_path, md_file_path)

    # Set up file watcher
    event_handler = CSVHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
