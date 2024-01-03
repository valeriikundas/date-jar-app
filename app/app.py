from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import random

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Initialize the SQLite database
conn = sqlite3.connect("date_jar.db", check_same_thread=False)
cursor = conn.cursor()

# Create the date_ideas table if it doesn't exist
cursor.execute(
    "CREATE TABLE IF NOT EXISTS date_ideas (id INTEGER PRIMARY KEY, idea TEXT)"
)
conn.commit()


def add_date_idea(idea):
    cursor.execute("INSERT INTO date_ideas (idea) VALUES (?)", (idea,))
    conn.commit()


def get_random_date_idea():
    cursor.execute("SELECT id, idea FROM date_ideas")
    ideas = cursor.fetchall()
    if ideas:
        random_idea = random.choice(ideas)
        return random_idea[1]
    else:
        return None


def use_date_idea(idea):
    idea_id = get_idea_id_by_name(idea)
    delete_date_idea(idea_id)


def get_idea_id_by_name(idea_title: str):
    cursor.execute("SELECT id, idea FROM date_ideas WHERE idea = ?", (idea_title,))
    return cursor.fetchone()[0]


def get_all_date_ideas():
    cursor.execute("SELECT idea FROM date_ideas")
    return [idea[0] for idea in cursor.fetchall()]


def delete_date_idea(idea_id):
    cursor.execute("DELETE FROM date_ideas WHERE id = ?", (idea_id,))
    conn.commit()


@app.route("/")
def home():
    return render_template("index.html", ideas=get_all_date_ideas())


@app.route("/add_idea", methods=["POST"])
def add_idea():
    idea = request.form["idea"]
    if idea:
        add_date_idea(idea)
    return redirect(url_for("home"))


@app.route("/get_random_idea")
def random_idea():
    idea = get_random_date_idea()
    return render_template("random_idea.html", idea=idea)


@app.route("/use/<string:idea>")
def use_idea(idea):
    use_date_idea(idea)
    return redirect(url_for("home"))


@app.route("/all")
def all():
    ideas = get_all_date_ideas()
    return render_template("all_ideas.html", ideas=ideas)


if __name__ == "__main__":
    app.run(debug=True)
