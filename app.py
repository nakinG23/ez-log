"""
EZ Log - Frictionless expense tracking API
WARNING: This uses in-memory storage. Data will be lost on server restart.
For production, add a database.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import re
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

expenses = []

@app.route('/log', methods=['POST', 'GET', 'OPTIONS'])
def log_expense():
    try:
        if request.method == 'OPTIONS':
            return '', 200
        
        # for GET requests (testing), show form
        if request.method == 'GET':
            return '''
            <form method="POST">
                <h3>Test Expense Logging</h3>
                <input type="text" name="text" placeholder="coffee, 5" style="padding: 10px; width: 300px;">
                <button type="submit" style="padding: 10px;">Log Expense</button>
            </form>
            <p>Or send POST request with JSON: {"text": "coffee 5"}</p>
            <p><a href="/expenses">View all expenses</a></p>
            '''
        
        # handling POST request
        if request.is_json:
            data = request.get_json()
            text = data.get('text', '').strip()
        else:
            text = request.form.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # extracting amount and item
        amount = 0.0
        item = "Unknown"
        
        # find the numbers for $$
        numbers = re.findall(r'\d+\.?\d*', text)
        if numbers:
            amount = float(numbers[0])
        
        # remove numbers to get item so order doesnt matter
        item = re.sub(r'\d+\.?\d*', '', text).strip(' $,.')
        
        # create the expense
        expense = {
            'id': len(expenses) + 1,
            'text': text,
            'item': item if item else "Unknown",
            'amount': amount,
            'timestamp': datetime.now().isoformat()
        }
        expenses.append(expense)
        # success response
        print(f"✅ Logged: {expense}")
        return jsonify({
            'success': True,
            'message': f'Logged: {item} - ${amount}',
            'expense': expense
        })
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/expenses', methods=['GET'])
def get_expenses():
    """View all expenses"""
    # calculate total
    total = sum(exp['amount'] for exp in expenses)
    
    # showing as simple HTML table for now, gonna move this to a proper desing file with styling
    html = f"""
    <html>
    <head><title>Expenses</title>
    <style>
        body {{ font-family: Arial; padding: 20px; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        tr:hover {{ background-color: #f5f5f5; }}
    </style>
    </head>
    <body>
        <h1>📊 EZ Log</h1>
        <p>Total logged: ${total:.2f} from {len(expenses)} expenses</p>
        <p><a href="/">Back to logging</a></p>
        
        <table>
            <tr>
                <th>ID</th>
                <th>Item</th>
                <th>Amount</th>
                <th>Time</th>
                <th>Raw Text</th>
            </tr>
    """
    
    for exp in reversed(expenses):  # showing newest first
        html += f"""
            <tr>
                <td>{exp['id']}</td>
                <td><strong>{exp['item']}</strong></td>
                <td>${exp['amount']:.2f}</td>
                <td>{exp['timestamp'][11:16]}</td>
                <td><small>{exp['text']}</small></td>
            </tr>
        """
    
    html += """
        </table>
    </body>
    </html>
    """
    
    return html

@app.route('/clear', methods=['GET'])
def clear_expenses():
    """Clear all expenses (for testing)"""
    global expenses
    expenses.clear()
    return '<h3>All expenses cleared</h3><a href="/">Go back</a>'

@app.route('/')
def home():
    return f'''
    <html>
    <head>
        <title>EZ Log API</title>
        <style>
            body {{ font-family: Arial; padding: 40px; max-width: 800px; margin: 0 auto; }}
            code {{ background: #f4f4f4; padding: 10px; display: block; margin: 10px 0; }}
            .endpoint {{ background: #e8f4f8; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <h1>💰 EZ Log API</h1>
        <p><strong>API is running!</strong> Logged {len(expenses)} expenses so far.</p>
        
        <div class="endpoint">
            <h3>📝 Log an Expense</h3>
            <p><a href="/log">Click here to log via web form</a></p>
            <p>Or send POST request:</p>
            <code>curl -X POST {request.host_url}log -H "Content-Type: application/json" -d '{{"text": "coffee 5"}}'</code>
        </div>
        
        <div class="endpoint">
            <h3>📊 View Expenses</h3>
            <p><a href="/expenses">View all expenses as HTML table</a></p>
            <p>Or GET: <code>{request.host_url}expenses</code></p>
        </div>
        
        <div class="endpoint">
            <h3>📱 Apple Shortcuts Setup</h3>
            <ol>
                <li>Open Shortcuts app on iPhone</li>
                <li>Create new shortcut</li>
                <li>Add "Ask for Input" action</li>
                <li>Add "Get contents of URL" action</li>
                <li>URL: <code>{request.host_url}log</code></li>
                <li>Method: POST, Request Body: JSON</li>
                <li>Add: <code>{{"text": "Provided Input"}}</code></li>
                <li>Add to home screen!</li>
            </ol>
        </div>
    </body>
    </html>
    '''.format(expenses_count=len(expenses))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))  #setting 5001 for local testing since 5000 is used by airplay or smn
    app.run(host='0.0.0.0', port=port, debug=False)  # debug=False for production