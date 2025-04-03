from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Store your Slack webhook URL securely (or set via environment variable)
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL") or "https://hooks.slack.com/services/XXXX/YYYY/ZZZZ"

@app.route('/servicetitan-webhook', methods=['POST'])
def receive_webhook():
    data = request.json

    # Extract and format message — customize this to your needs
    job_name = data.get('jobName', 'Unnamed Job')
    customer = data.get('customerName', 'Unknown Customer')
    scheduled_time = data.get('scheduledDateTime', 'N/A')

    slack_message = {
        "text": f":hammer_and_wrench: *New Job Booked!*\n*Job:* {job_name}\n*Customer:* {customer}\n*Scheduled:* {scheduled_time}"
    }

    # Send message to Slack
    response = requests.post(SLACK_WEBHOOK_URL, json=slack_message)

    if response.status_code != 200:
        return jsonify({'error': 'Failed to send to Slack'}), 500

    return jsonify({'status': 'Message sent to Slack'}), 200

if __name__ == '__main__':
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)

