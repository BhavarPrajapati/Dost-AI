from flask import Flask, render_template, jsonify, request
import google.generativeai as genai
from PIL import Image

app = Flask(__name__)

genai.configure(api_key="AIzaSyBsE2N5HICzt1LM0O3dEn2zS328WrEIGww")

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/product-upload")
def product_upload():
    return render_template("product_upload.html")

@app.route("/project-ideas")
def product_ideas():
    return render_template("product_ideas.html")

@app.route("/product-sell")
def product_sell():
    return render_template("product_sell.html")

@app.route("/competition")
def competition():
    return render_template("competition.html")

@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_msg = request.json.get("message")
    prompt = f"You are a helpful assistant. User: {user_msg}\nAssistant:"
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return jsonify({"reply": response.text.strip()})


@app.route("/generate_post", methods=["POST"])
def generate_post():
    file = request.files['image']
    title = request.form.get("title")
    price = request.form.get("price")

    # Load image
    image = Image.open(file.stream)

    # Create prompt
    prompt = f"""
    You are a creative social media assistant.
    Title: {title}
    {"Price: " + price if price else ""}
    Task: Write a catchy, engaging product description for this post in 3-5 lines. Make it attractive and informative for social media. 
    Then generate 10-15 trending, relevant hashtags (no numbering, just hashtags separated by spaces or commas).
    Only output the description and hashtags, nothing else.
    """

    # Call Gemini
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([prompt, image])

    return jsonify({"post": response.text})
@app.route("/product-sell", methods=["GET", "POST"])
def product_sell_web():
    if request.method == "POST":
        # File aur category nikalna
        category = request.form.get("category")
        file = request.files.get("file")

        # Agar file diya gaya hai to uska naam le lo (demo ke liye)
        file_info = f"User uploaded a product file: {file.filename}" if file else "No file uploaded"

        # Prompt Gemini ke liye
        prompt = f"""
        A user wants to sell their handmade product or art.
        File info: {file_info}
        Category: {category}

        Suggest exactly 3 websites or apps where the user can easily sell this type of product.
        For each website, provide:
        1. Website/App name
        2. Short description
        3. Direct link (URL)

        Return the answer in clear JSON format with keys: name, description, link.
        """

        # Gemini model
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        return jsonify({"recommendations": response.text})

@app.route("/project-ideas", methods=["GET", "POST"])
def project_ideas_web():
    if request.method == "POST":
        topic = request.form.get("topic")

        prompt = f"""
        The user is looking for creative project ideas.
        Topic: {topic}

        Generate exactly 5 unique and creative project ideas related to this topic.
        Return the answer in JSON format like:
        [
            {{"idea": "First idea"}},
            {{"idea": "Second idea"}},
            ...
        ]
        """

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        return jsonify({"ideas": response.text})

if __name__ == "__main__":
    app.run(debug=True)
