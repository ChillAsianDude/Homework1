from flask import Flask, render_template, request
import google.generativeai as genai
import os
import re

api = "AIzaSyA85Gy2EW9b67GHgnWih9J_M33_WXtw3-c"
genai.configure(api_key=api)
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)

@app.route("/ai_agent", methods=["GET", "POST"])
def ai_agent():
    return render_template("ai_agent.html")
    
@app.route("/ai_agent_reply", methods=["GET", "POST"])
def ai_agent_reply():
    q = request.form.get("q")  
    response = model.generate_content(q)
    r = response.candidates[0].content.parts[0].text

    formatted_response = re.sub(r'<[^>]*>', '', r) 
    formatted_response = re.sub(r'\*\*', '', formatted_response) 
    formatted_response = re.sub(r'\*', '', formatted_response)  
    formatted_response = formatted_response.replace('\n', ' ')  

    return render_template("ai_agent_reply.html", r=formatted_response)

@app.route("/joke", methods=["GET", "POST"])
def joke():
    return render_template("joke.html")

@app.route("/joke_reply", methods=["GET", "POST"])
def joke_reply():
    joke_type = request.form.get("joke_type")
    
    if joke_type == "singapore":
        q = "Tell me a common joke in Singapore."
    elif joke_type == "financial_news":
        q = "Tell me a joke about financial news."
    else:
        q = "Tell me a random joke."
    
    response = model.generate_content(q)
    r = response.candidates[0].content.parts[0].text

    formatted_response = re.sub(r'<[^>]*>', '', r)  
    formatted_response = re.sub(r'\*\*', '', formatted_response)  
    formatted_response = re.sub(r'\*', '', formatted_response)  
    
    formatted_response = formatted_response.replace('\n', ' ')  

    return render_template("joke_reply.html", r=formatted_response)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
