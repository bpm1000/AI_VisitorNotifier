import requests

LINE_TOKEN = 'Your-LINE-Notify-Token-Here'

def send_line_notify(message):
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer ' + LINE_TOKEN}
    payload = {'message': message}
    r = requests.post(url, headers=headers, params=payload)
    return r.status_code

# テストメッセージの送信
send_line_notify("テストメッセージです")
