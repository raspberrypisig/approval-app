from nicegui import ui

from pathlib import Path
from datetime import datetime

selected_file = ""

approved_files = []
unapproved_files = []

def list_upload_files_with_metadata(directory='uploads'):
    """
    Lists all files in the specified directory along with their last modified date (non-recursive).

    Args:
        directory (str): The directory to list files from. Default is 'uploads'.

    Returns:
        list: A list of dictionaries containing 'filename' and 'date_modified'.
    """
    # Create a Path object for the given directory
    dir_path = Path(directory)

    # Check if the directory exists
    if not dir_path.exists():
        raise FileNotFoundError(f"The directory '{directory}' does not exist.")
    
    if not dir_path.is_dir():
        raise NotADirectoryError(f"'{directory}' is not a directory.")

    # List only files in the top-level directory (non-recursive)
    files_with_metadata = []
    for file in dir_path.iterdir():
        if file.is_file():
            # Get the last modified time and convert it to a readable format
            modified_time = file.stat().st_mtime  # Last modified time in seconds since epoch
            modified_date = datetime.fromtimestamp(modified_time)
            
            # Format the date and time
            day = modified_date.strftime('%d').lstrip('0')  # Remove leading zero from day
            month = modified_date.strftime('%m').lstrip('0')  # Remove leading zero from month
            year = modified_date.strftime('%Y')
            hour = modified_date.strftime('%I').lstrip('0')  # Remove leading zero from hour
            minute = modified_date.strftime('%M')
            am_pm = modified_date.strftime('%p')
            
            # Construct the formatted date string
            modified_date = f"{day}/{month}/{year} {hour}:{minute} {am_pm}"
            
            # Append the filename and modified date as a dictionary
            files_with_metadata.append({
                'filename': str(file.name),  # Just the file name (not full path)
                'date': modified_date
            })

    return files_with_metadata

def approve_file(dialog: ui.dialog, filename: str):
    ui.notify(filename)
    dialog.close()

def show_dialog(filename):

    with ui.context.client.content:
        with ui.dialog() as dialog:
            with ui.card():
                ui.label(f'Are you sure you want to approve file {filename}?')
                with ui.row():
                    ui.button("OK", on_click=lambda: approve_file(dialog, filename))
                    ui.button("Cancel", on_click=dialog.close)                    
    dialog.open()

# Function to handle approve button clicks
def on_approve(filename):
    #ui.notify(f"Approved: {filename}")
    show_dialog(filename)


@ui.page('/history')
async def approval_history():
    # Create a row to hold the heading and hyperlinks
    with ui.row().classes('w-full items-center'):  # Full-width row, vertically aligned items
        # Left-justified heading
        ui.label("Approval History").classes('text-h6 font-bold flex-grow')

        # Right-justified hyperlinks
        with ui.row().classes('gap-4 justify-end'):  # Small gap between links, right-aligned
            ui.link('Back', '/').classes('text-blue-600 hover:underline')  # Points to "/"
    


@ui.page('/')
async def index():
    # Create a row to hold the heading and hyperlinks
    with ui.row().classes('w-full items-center'):  # Full-width row, vertically aligned items
        # Left-justified heading
        ui.label("Awaiting your approval").classes('text-h6 font-bold flex-grow')

        # Right-justified hyperlinks
        with ui.row().classes('gap-4 justify-end'):  # Small gap between links, right-aligned
            ui.link('Approval History', '/history').classes('text-blue-600 hover:underline')  # Points to "/history"

    table_data = list_upload_files_with_metadata()

    # Create a custom table layout
    headers = ["Filename", "Date", "Actions"]
    with ui.column().classes('w-full'):
        # Add headers
        with ui.row().classes('w-full font-bold border-b border-gray-300 py-2'):
            # Filename column header (50vw)
            ui.label(headers[0]).style('width: 50vw; text-align: left;')  
            # Date column header
            ui.label(headers[1]).style('width: 15vw; text-align: left;')  
            # Actions column header
            ui.label(headers[2]).style('width: 20vw; text-align: center;').classes('hidden-for-small-screen')

        # Add rows
        for row in table_data:
            with ui.row().classes('w-full py-2 border-b border-gray-200'):
                # Filename column (downloadable link, 50vw)
                ui.link(
                    row['filename'], 
                    f"{row['filename']}", 
                    new_tab=True
                ).style('width: 50vw; text-align: left; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;')
                
                # Date column
                ui.label(row['date']).style('width: 15vw; text-align: left;')
                
                # Actions column (only Approve button)
                with ui.row().style('width: 20vw; justify-content: center;'):
                    ui.button('Approve', on_click=lambda _, r=row: on_approve(r['filename'])).props('size=sm color=green')

    # Add custom CSS for responsiveness
    ui.add_head_html('''
    <style>
    .hidden-for-small-screen {
        display: block;
    }
    @media (max-width: 500px) {
        .hidden-for-small-screen {
            display: none;
        }
    }
    </style>
    ''')

# Run the app
ui.run()

