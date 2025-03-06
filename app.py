from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

DATABASE = "p1.db"  # SQLite database file

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Enables dictionary-like access to rows
    return conn


def process_query(query):
    keywords = ["table", "give", "show", "project", "print","want"]
    if any(word in query.lower() for word in keywords):
        pass
    else:
        return "Invalid Query"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]

    query_list=query.lower().split()
    for word in query_list:
        if(word in tables):
            table=word
            break
    else:
        return "table not found"
    print(table)
    cursor.execute(f"SELECT * FROM {table} LIMIT 1")
    colums = list(map(lambda x: x[0],cursor.description))
    colum=[]
    for word in query_list:
        if(word in colums):
            colum.append(word)
    colum = ','.join(colum) if colum else '*'
    return f"select {colum} from {table}"
@app.route("/", methods=["GET", "POST"])
def index():
    data = []
    sql_query = ""
    columns=[]
    if request.method == "POST":
        user_query = request.form["query"]
        sql_query = process_query(user_query)
        if sql_query != "Invalid Query" and sql_query != "table not found" :
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql_query)
            data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            cursor.close()
            conn.close()

    return render_template("index.html", q=sql_query,columns=columns, data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5500, debug=True)