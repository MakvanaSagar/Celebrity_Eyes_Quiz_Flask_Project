from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "quiz_secret"

# List of questions with Indian cricketers
questions = [
    {"image": "viratkohli.jpg", "answer": "Virat Kohli", 
     "options": ["Virat Kohli", "Rohit Sharma", "Shikhar Dhawan"]},
    
    {"image": "msd.jpg", "answer": "MS Dhoni", 
     "options": ["MS Dhoni", "Hardik Pandya", "Ravindra Jadeja"]},
    
    {"image": "sachin.jpg", "answer": "Sachin Tendulkar", 
     "options": ["Sachin Tendulkar", "Virender Sehwag", "Yuvraj Singh"]},
    
    {"image": "rohit.jpg", "answer": "Rohit Sharma", 
     "options": ["Rohit Sharma", "KL Rahul", "Ajinkya Rahane"]},
    
    {"image": "bumrah.jpg", "answer": "Jasprit Bumrah", 
     "options": ["Jasprit Bumrah", "Bhuvneshwar Kumar", "Mohammad Shami"]}
]


@app.route("/")
def start():
    session["score"] = 0
    session["qno"] = 0
    random.shuffle(questions)
    return redirect(url_for("quiz"))

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if session["qno"] >= len(questions):
        return redirect(url_for("result"))

    q = questions[session["qno"]]
    random.shuffle(q["options"])

    if request.method == "POST":
        if request.form.get("answer") == q["answer"]:
            session["score"] += 1
        session["qno"] += 1
        return redirect(url_for("quiz"))

    level = "Beginner"
    if session["score"] >= 3:
        level = "Intermediate"
    if session["score"] >= 5:
        level = "Expert"

    return render_template("quiz.html", q=q, qno=session["qno"] + 1,
                           total=len(questions), score=session["score"],
                           level=level)

@app.route("/result")
def result():
    return render_template("result.html",
                           score=session["score"],
                           total=len(questions))

if __name__ == "__main__":
    app.run(debug=True)
