from flask import Flask, request, redirect, session, jsonify
from twitter_oauth2_client import (
    get_authorization_url,
    exchange_code_for_token,
    generate_code_verifier,
    post_tweet
)

app = Flask(__name__)
app.secret_key = 'eifhfrhlrhlefh'

@app.route('/')
def home():
    return '<a href="/login">Login with Twitter</a>'

@app.route('/login')
def login():
    code_verifier = generate_code_verifier()
    session['code_verifier'] = code_verifier
    auth_url = get_authorization_url(code_verifier)
    return redirect(auth_url)

@app.route('/callback')
def callback():
    auth_code = request.args.get('code')
    code_verifier = session.get('code_verifier')

    if not auth_code or not code_verifier:
        return "Error: Missing authorization code or code verifier.", 400

    try:
        token_response = exchange_code_for_token(auth_code, code_verifier)
        access_token = token_response.get('access_token')
        session['access_token'] = access_token  # Store access token in session

        # Display a form to submit a tweet
        return '''
            <p>Successfully authenticated!</p>
            <form action="/tweet" method="post">
                <label for="tweet_text">Enter your tweet:</label><br>
                <input type="text" id="tweet_text" name="tweet_text" maxlength="280" required><br><br>
                <input type="submit" value="Post Tweet">
            </form>
        '''
    except Exception as e:
        return str(e), 500

@app.route('/tweet', methods=['POST'])
def tweet():
    tweet_text = request.form.get('tweet_text')
    access_token = session.get('access_token')

    if not access_token:
        return "Error: User is not authenticated.", 401

    try:
        tweet_response = post_tweet(access_token, tweet_text)
        return jsonify(tweet_response)
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
