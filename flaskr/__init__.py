import os
# from flask_mysql_connector import MySQL
from flask_mysqldb import MySQL

from flask import Flask, render_template, request, flash, redirect, url_for # type: ignore


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'root'
    app.config['MYSQL_DB'] = 'resto-app'
    mysql = MySQL(app)
    

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def main():
        return render_template('base.html')
    @app.route('/index')
    def index():
        return render_template('index.html')
    @app.route('/about')
    def about():
        return render_template('about.html')
    @app.route('/project')
    def project():
        return render_template('project.html')
    @app.route('/contact')
    def contact():
        return render_template('contact.html')
    @app.route('/contact_mail', methods=['GET', 'POST'])
    def contact_mail():
        if request.method == 'POST':  
            print("Post Method")
            try:
                conn = mysql.connection
                cur = conn.cursor()
                fname = request.form['fname']
                lname = request.form['lname']
                email = request.form['email']
                phone = request.form['phone']
                message = request.form['message']
                print(message,phone)
                cur.execute('''insert into message values(%s, %s, %s, %s, %s) ''',(fname,lname,email,phone,message))
                conn.commit()
                flash('Item added', 'success')
                # return redirect(url_for('contact'))
                return 'Form submited'
            except Exception as e:
                print(e)
                conn.rollback
                flash('Something went wrong', 'error')
                return 'Form submition failed'
                # return redirect(url_for('contact'))
            finally:
                # conn.close()
                pass


    from . import db
    db.init_app(app)

    return app