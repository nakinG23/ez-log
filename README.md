# EZ Log - Frictionless Expense Tracking

**Log expenses in seconds. Think less, track more.**

EZ Log is a minimalist expense tracking API designed for **maximum convenience, minimum friction**. Log expenses via Apple Shortcuts, Siri, or any voice assistant without ever needing to open the app.

> "If it can't be done in one breath, it's too complicated." - EZ Log Philosophy

### Local Development
```bash
# Clone the repo
git clone https://github.com/yourusername/ez-log.git
cd ez-log

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
# Server starts at http://localhost:5001
# log expenses at http://localhost:5001/log
# view expenses at http://localhost:5001/expenses

🔧 API Endpoints

Method	Endpoint	Description
POST	/log	    Log an expense (JSON: {"text": "coffee 5"})
GET	    /log	    Web form for manual entry
GET	    /expenses	View all expenses as HTML table
GET	    /	        Homepage with instructions