import os
from flask import Flask, redirect, render_template, request
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_restful import abort

from data import db_session
from data.inventory import Inventory, InventoryAddForm
from data.users import LoginForm, User, RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

def main():
    db_session.global_init("db/base.sqlite")

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("index.html", title='Главное меню')
    else:
        return redirect("/login")


@app.route('/inventory')
@login_required
def inventory():
    session = db_session.create_session()
    return render_template("inventory.html", title="Список инвентаря",
                           inventory=session.query(Inventory).all(), admin=current_user.is_admin)


@app.route('/inventory_delete/<int:id>')
@login_required
def inventory_delete(id):
    session = db_session.create_session()

    item = session.query(Inventory).filter(Inventory.id == id).first()
    if item and current_user.is_admin:
        session.delete(item)
        session.commit()
    else:
        abort(404)
    return redirect('/inventory')


@app.route('/inventory_edit', methods=['GET', 'POST'])
@login_required
def inventory_add():
    session = db_session.create_session()

    form = InventoryAddForm()
    if form.validate_on_submit():
        for i in range(form.quantity.data):
            item = Inventory()
            item.name = form.name.data
            item.state = 'Новый'
            item.owner_id = 1
            session.add(item)
        session.commit()
        return redirect('/inventory')

    return render_template('inventory_edit.html', title='Добавление инвентаря', form=form)


# @app.route('/inventory_edit/<int:id>', methods=['GET', 'POST'])
# @login_required
# def inventory_edit(id):
#     session = db_session.create_session()
#
#     item = session.query(Inventory).filter(Inventory.id == id).first()
#     if not item:
#         abort(404)
#
#     form = InventoryAddForm()
#     if request.method == 'GET':
#         form.name = item.name
#         form.quantity = item.quantity
#


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = User()
        user.login = form.login.data
        user.set_password(form.password.data)
        user.is_admin = False
        try:
            session.add(user)
            session.commit()
        except:
            return render_template('register.html',
                                   message="Пользователь с таким логином уже существует",
                                   form=form)
        return redirect("/login")
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.get(User, user_id)

if __name__ == '__main__':
    main()