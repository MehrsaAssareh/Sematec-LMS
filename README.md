# Sematec LMS

Sematec LMS is a Python desktop CRUD application for managing people, employees, teachers, students, courses, schedules, registrations, certificates, and administration users.

## Tech Stack

- Python
- Tkinter / ttkbootstrap
- SQL Server
- pyodbc
- Pillow
- PyInstaller

## Project Structure

- `SematecLMS/BusinessLogicLayer`: validation and application rules
- `SematecLMS/DataAccessLayer`: SQL Server data access
- `SematecLMS/Model`: data models
- `SematecLMS/UserInterfaceLayer`: desktop UI pages
- `SematecLMS/DatabaseScripts`: database setup and migration scripts
- `SematecLMS/images`: app icon and UI image assets

## Setup

Install dependencies:

```powershell
cd SematecLMS
python -m pip install -r requirements.txt
```

Create or restore the SQL Server database, then update the connection string if needed:

```powershell
$env:SEMATEC_LMS_CONNECTION_STRING="Driver={SQL Server};Server=YOUR_SERVER;Database=SematecLearningManagementSystem;Trusted_Connection=yes"
```

Run the app:

```powershell
python Main.py
```

## Build EXE

```powershell
cd SematecLMS
python -m PyInstaller SematecLMS.spec
```

The generated app folder will be created in `SematecLMS/dist/SematecLMS`.

## Database

Use `SematecLMS/DatabaseScripts/20260527_final_database.sql` for a clean database setup matching the current app schema and public demo seed data.

Demo admin login:

```text
Username: admin.demo
Password: Demo@12345
```

The public database script uses demo people, placeholder photos, and demo credentials.

## License

No license is included. The source code is public for viewing, but reuse, copying, or redistribution is not granted unless the owner adds a license later.
