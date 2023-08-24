from flask import Flask, request, render_template_string
import openai

app = Flask(__name__)

with open('index.html', 'r') as file:
    index_html = file.read()

@app.route('/', methods=['GET'])
def index():
    return render_template_string(index_html)

@app.route('/generate_insults', methods=['POST'])
def generate_insults():
    game_name = request.form.get('game_name')
    api_key = request.form.get('api_key')  # Get the API key from the form

    if not game_name or not api_key:
        return render_template_string(index_html, error="Please provide a game name and API key.")

    openai.api_key = api_key  # Set the OpenAI API key

    prompt_messages = [
        {"role": "system", "content": "You are a 12 year old hardcore gamer with a nasty attitude who loves to insult people"},
        {"role": "user", "content": f"Generate a list of 10 insults related to {game_name}"}
    ]
    response = generate_response(prompt_messages)

    insults = response.split('\n')
    return render_template_string(index_html, insults=insults)
	
def generate_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=450,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response['choices'][0]['message']['content']

if __name__ == '__main__':
    app.run(debug=True)
