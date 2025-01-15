import os
from flask import Flask, redirect, render_template, request
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_restful import abort

from data import db_session
from data.inventory import Inventory, InventoryAddForm, InventoryEditForm
from data.procurement import Procurement, ProcurementAddForm, ProcurementEditForm
from data.request import Request, RequestForm
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
        return render_template("index.html", title='Главное меню', admin=current_user.is_admin)
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
        item = Inventory()
        item.name = form.name.data
        item.quantity = form.quantity.data
        item.state_id = 1
        item.user_id = -1
        session.add(item)
        session.commit()
        return redirect('/inventory')

    return render_template('inventory_edit.html', title='Добавление инвентаря', form=form)


@app.route('/inventory_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def inventory_edit(id):
    session = db_session.create_session()

    item = session.query(Inventory).filter(Inventory.id == id).first()
    if not item:
        abort(404)

    form = InventoryEditForm()
    form.user.choices = [(-1, "Открепить")] + [(x.id, x.login) for x in session.query(User).filter(User.id != 1).all()]
    if request.method == 'GET':
        form.name.data = item.name
        form.quantity.data = item.quantity
        form.state.data = item.state_id
        form.user.data = item.user_id

    if form.validate_on_submit():
        item.name = form.name.data
        item.quantity = form.quantity.data
        if form.user.data == -1:
            item.state_id = form.state.data
        else:
            item.state_id = 2
        item.user_id = form.user.data
        session.commit()
        return redirect('/inventory')

    return render_template('inventory_edit.html', title='Изменение инвентаря', form=form)


@app.route('/procurement')
@login_required
def procurement():
    session = db_session.create_session()
    return render_template("procurement.html", title="Закупки",
                           procurements=session.query(Procurement).all())


@app.route('/procurement_edit', methods=['GET', 'POST'])
@login_required
def procurement_add():
    session = db_session.create_session()

    form = ProcurementAddForm()
    if form.validate_on_submit():
        item = Procurement()
        item.good = form.good.data
        item.price = form.price.data
        item.seller = form.seller.data
        session.add(item)
        session.commit()
        return redirect('/procurement')

    return render_template('procurement_edit.html', title='Добавление закупки', form=form)


@app.route('/procurement_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def procurement_edit(id):
    session = db_session.create_session()

    item = session.query(Procurement).filter(Procurement.id == id).first()
    if not item:
        abort(404)

    form = ProcurementEditForm()
    if request.method == 'GET':
        form.good.data = item.good
        form.price.data = item.price
        form.seller.data = item.seller

    if form.validate_on_submit():
        item.good = form.good.data
        item.price = form.price.data
        item.seller = form.seller.data
        session.commit()
        return redirect('/procurement')

    return render_template('procurement_edit.html', title='Изменение закупки', form=form)


@app.route('/procurement_delete/<int:id>')
@login_required
def procurement_delete(id):
    session = db_session.create_session()

    item = session.query(Procurement).filter(Procurement.id == id).first()
    if item and current_user.is_admin:
        session.delete(item)
        session.commit()
    else:
        abort(404)
    return redirect('/procurement')


@app.route('/request')
@login_required
def request_route():
    session = db_session.create_session()
    if current_user.is_admin:
        requests = session.query(Request).all()
        requests.reverse()
        return render_template("request_admin.html", title="Заявки",
                               requests=requests)
    else:
        requests = session.query(Request).filter(Request.user_id == current_user.id).all()
        requests.reverse()
        return render_template("request_user.html", title="Заявки",
                               requests=requests)


@app.route('/request/<int:id>/<string:action>')
@login_required
def request_respond(id, action):
    if current_user.is_admin:
        session = db_session.create_session()
        request = session.query(Request).filter(Request.id == id).first()
        if action == 'approve':
            if request.type_id == 1:
                request.state_id = 2
                request.item.state_id = 2
                request.item.user_id = request.user_id
            else:
                request.state_id = 2
                request.item.state_id = 3
                request.item.user_id = -1
        elif action == 'decline':
            request.state_id = 3
        session.commit()
    return redirect('/request')


@app.route('/request_create/<int:id>', methods=['GET', 'POST'])
@login_required
def request_create(id):
    session = db_session.create_session()

    form = RequestForm()
    if form.validate_on_submit():
        request = Request()
        request.type_id = form.type.data
        request.item_id = id
        request.user_id = current_user.id
        request.state_id = 1
        if session.query(Request).filter(Request.type_id == request.type_id,
                                         Request.item_id == request.item_id,
                                         Request.user_id == request.user_id,
                                         Request.state_id == request.state_id).first():
            return render_template('request_create.html', title='Создать заявку',
                                   message='Такая заявка уже существует', form=form)
        else:
            session.add(request)
            session.commit()
            return redirect('/inventory')

    return render_template('request_create.html', title='Создать заявку', form=form)


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