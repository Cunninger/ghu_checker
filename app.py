from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_inputs = request.form.get('tokens').strip().split('\n')
        alive_tokens = []
        dead_tokens = []

        for user_input in user_inputs:
            if not user_input or not user_input.startswith('gh'):
                return '请输入以 "gh" 开头的字符串,一行一个,ghu_1234567890abcdef\n'

            GHO_TOKEN = user_input.strip()

            headers = {
                'Host': 'api.github.com',
                'authorization': f'token {GHO_TOKEN}',
                'Editor-Version': 'vscode/1.85.2',
                'Editor-Plugin-Version': 'copilot-chat/0.11.1',
                'User-Agent': 'GitHubCopilotChat/0.11.1',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br'
            }

            response = requests.get('https://api.github.com/copilot_internal/v2/token', headers=headers)
            response_body = response.json()

            if response.status_code == 200 and response_body.get('token'):
                alive_tokens.append(f"{GHO_TOKEN} - {response_body['sku']}")
            else:
                notification_id = None
                if response_body.get('error_details'):
                    notification_id = response_body['error_details']['notification_id']
                dead_tokens.append(f"{GHO_TOKEN} - {response_body['message']} - {notification_id}")

        return render_template('result.html', alive_tokens=alive_tokens, dead_tokens=dead_tokens)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)