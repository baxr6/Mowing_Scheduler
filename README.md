# Mowing Scheduler

**Mowing Scheduler** is a desktop application built with Python and Tkinter to help manage and schedule weekly lawn mowing services. It stores client information, displays scheduled jobs in a weekly view, and allows for quick updates like marking jobs as completed.

This is ideal for small landscaping businesses or individuals who want a lightweight scheduling tool without the complexity of online calendars or CRMs.

## Features

- 🗓 Weekly schedule view with dynamic calendar navigation
- 👤 Add, edit, and store client details
- ✅ Mark appointments as completed
- 💾 Persistent storage using CSV for client and schedule data
- 🔍 View and filter scheduled jobs for a selected week
- 📦 Built with only the Python standard library (no dependencies!)

## Getting Started

### Prerequisites

- Python 3.7 or higher

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/baxr6/Mowing_Scheduler.git
cd Mowing_Scheduler

    Run the app:

python mowing_scheduler.py

    ✅ No need for external libraries — everything runs from the standard Python installation!

Usage

Once you run the application:

    Use the "Add Client" button to input a client's name, address, day of the week, and completion status.

    The schedule is automatically updated and saved in schedule.csv.

    Use navigation buttons to change weeks and review upcoming or past mowing schedules.

    Click "Complete" to mark a client's mowing job for the week as finished.

Project Structure

Mowing_Scheduler/
├── client.py               # Client model definition
├── mowing_scheduler.py     # Main GUI application using Tkinter
├── schedule.csv            # Stores the list of clients and mowing schedules
└── README.md               # Project documentation

File Descriptions

    mowing_scheduler.py
    Main file that runs the GUI application. Handles calendar logic, user input, and CSV reading/writing.

    client.py
    Defines a Client class with attributes like name, address, scheduled day, and completion status.

    schedule.csv
    CSV file used to persist client and mowing schedule data. Automatically updated when you add or modify clients.

Roadmap / Improvements

Add editing functionality for existing clients

Support for one-time or custom-date jobs

Move to SQLite or JSON for better structure and flexibility

    Export weekly reports or invoices

Contributing

Contributions are welcome! Here's how to get started:

    Fork the repository

    Create a new branch: git checkout -b feature/your-feature

    Commit your changes: git commit -m "Add feature"

    Push to the branch: git push origin feature/your-feature

    Open a pull request

License

This project is licensed under the MIT License.
Author

Created by @baxr6
