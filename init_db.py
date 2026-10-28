"""Root database initialization entry point for NoteMind.

Usage:
    python init_db.py               # Initialize tables and seed data
    python init_db.py --drop        # Reset and recreate all tables
    python init_db.py --check       # Verify database tables
    python init_db.py --migrate     # Run pending migrations
    python init_db.py --seed        # Seed categories only
"""

import sys
from database.init_db import main, init_db

if __name__ == "__main__":
    main()
