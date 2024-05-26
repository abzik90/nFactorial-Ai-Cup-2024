from flask import Flask, render_template, request, jsonify
import openai
import os, json, time, subprocess

app = Flask(__name__)

# Configure OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")
print(os.getenv("OPENAI_API_KEY"))
client = openai.OpenAI()

with open("examples.json", 'r') as file:
    examples_data = json.load(file)

    assistant = client.beta.assistants.create(
        instructions=f"You are an agent that writes ONLY python code with robodk library for KUKA KR 10 R1420 robotic arm. Assume that environment is already set.Your task is to generate ONLY the python code(everything else should be commented), for the given robotic arm. The reference coordinates such as home base is defined as home = RDK.Item('Home') initial and target = RDK.Item('Target 1') around which the figures are drawn. You should initialize RDK as following RDK = robolink.Robolink(). You should use the similar syntax to the following examples provided by robodk, however keep in mind that it's written for python3.4 and you NEED to generate for >python3.10. It contains several examples with a purpose(name), description, and the code: \"\"\"{examples_data}\"\"\"",
        name="robodk_assist",
        tools=[{"type": "code_interpreter"}],
        model="gpt-4o",
)

thread = client.beta.threads.create()

# Define home route
@app.route('/')
def home():
    return render_template('index.html')

# Define route to send message to GPT and get response
@app.route('/send-message', methods=['POST'])
def send_message():
    user_input = request.json['message']
    
    message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role = "user",
        content = f"{user_input}"
    )

    run = client.beta.threads.runs.create(
        thread_id = thread.id,
        assistant_id = assistant.id
    )
    time.sleep(10)

    run = client.beta.threads.runs.retrieve(
        thread_id = thread.id,
        run_id = run.id
    )
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    
    response = messages.data[0].content[0].text.value
    with open('gpt-kuka.py', 'w') as file:
        response = response.replace("```python", "").replace("```", "")
        file.write(response)

    try:
        subprocess.run(['python3', 'gpt-kuka.py'])
    except Exception as e:
        print(e)
    return jsonify({'message': response})

if __name__ == '__main__':
    app.run(debug=True)
