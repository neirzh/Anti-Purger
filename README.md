### Functionality

- Monitors messages for words like "purge," "purging," "purged," etc.
- Collects up to 100 most recent messages.
- Generates a PDF with message details (timestamp, author, content).
- Sends the PDF to the specified user's DM.
- Uses Bangladesh timezone (Asia/Dhaka) for timestamps.

### Requirements

- Python 3.8+
- discord.py
- reportlab
- pytz

### Notes

- Ensure the bot has proper permissions to read messages and access channel history.
- The target user must be accessible by the bot (e.g., share a server or allow DMs).
