from nicegui import ui

# Create a row to hold the heading and hyperlinks
with ui.row().classes('w-full items-center'):  # Full-width row, vertically aligned items
    # Left-justified heading
    ui.label("Awaiting your approval").classes('text-h6 font-bold flex-grow')

    # Right-justified hyperlinks
    with ui.row().classes('gap-4 justify-end'):  # Small gap between links, right-aligned
        ui.link('View Records', '/').classes('text-blue-600 hover:underline')  # Points to "/"
        ui.link('Approval History', '/history').classes('text-blue-600 hover:underline')  # Points to "/history"

# Define table data
table_data = [
    {"filename": "document1.pdf", "date": "2023-10-01"},
    {"filename": "report2.xlsx", "date": "2023-10-05"},
]

# Function to handle approve button clicks
def on_approve(filename):
    ui.notify(f"Approved: {filename}")

# Base URL for file downloads
BASE_URL = "http://localhost:8000/uploads/"

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
                f"{BASE_URL}{row['filename']}", 
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

