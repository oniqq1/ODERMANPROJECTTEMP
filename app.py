from flask import Flask, render_template, request, redirect, url_for, abort
import sqlite3

app = Flask(__name__)

name = "Арсен"
surname = "Кропачев"





def create_connect_bd():
    try:
        sql_conection = sqlite3.connect('oderman_pizzas.db')
        cursor = sql_conection.cursor()


        sqlite_create_table_query = """CREATE TABLE pizzas
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name TEXT UNIQUE,
                                    description TEXT NOT NULL,
                                    cost INTEGER NOT NULL)"""

        try:
            cursor.execute(sqlite_create_table_query)
            sql_conection.commit()
            print(f'DB created')
        except sqlite3.Error as error:
            print(f'DB connected but error - {error}')

        

    except sqlite3.Error as error:
        print(f'In DB error - {error}')
    finally:
        if (sql_conection):
            cursor.close()
            sql_conection.close()

create_connect_bd()


@app.get('/')
def about():

    return render_template("about.html", name=name, surname=surname)


@app.post('/admin/')
def post_admin():
    name = request.form['name']
    description = request.form['description']
    cost = request.form['cost']

    print(name, description, cost)

    try:
        sql_conection = sqlite3.connect('oderman_pizzas.db')
        cursor = sql_conection.cursor()
        sqlite_values_query = ('INSERT INTO pizzas'
                               '(name,description,cost)'
                               'VALUES'
                               f'("{name}","{description}",{cost})')

        cursor.execute(sqlite_values_query)
        sql_conection.commit()
        print('all is allright')
    except sqlite3.Error as error:
        print(error)
    finally:
        if (sql_conection):
            cursor.close()
            sql_conection.close()
    return redirect("http://127.0.0.1:8099")




@app.get('/admin/')
def get_admin():
    return render_template('admin.html')



@app.get('/pizza/')
def info():
    new_pizzas = {}
    try:
        sql_conection = sqlite3.connect('oderman_pizzas.db')
        cursor = sql_conection.cursor()
        sqlite_values_query = 'SELECT * FROM pizzas'
        cursor.execute(sqlite_values_query)
        new_pizzas['pizzas'] = cursor.fetchall()
        print(new_pizzas.get('pizzas'))


    finally:
        if (sql_conection):
            cursor.close()
            sql_conection.close()


    return render_template("info.html", **new_pizzas)


if __name__ == '__main__':
    app.run(port=8099, debug=True)

