# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request, g, session
from app.forms import *
from flask_login import current_user, login_user, login_required, logout_user
from app.models import *
from werkzeug.urls import url_parse
from app import app, db
from app.forms import EditProfileForm
from sqlalchemy import exc
from datetime import timedelta, date


#Главная
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Главная')

#Вход
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверный логин и/или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html', title='Войти', form=form)

#Выход
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

#Страница пользователя
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('user.html', user=user)

#Изменить профиль
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.name = form.name.data
        current_user.lastname = form.lastname.data
        current_user.patronym = form.patronym.data
        current_user.phone = form.phone.data
        current_user.address = form.address.data
        current_user.checkver = True
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.name.data = current_user.name
        form.lastname.data = current_user.lastname
        form.patronym.data = current_user.patronym
        form.phone.data = current_user.phone
        form.address.data = current_user.address
    return render_template('edit_profile.html', title='EditProfile', form=form)

#Получение прав Администратора
@app.route('/admprofile', methods=['GET', 'POST'])
@login_required
def AdmProfile():
    form = AdmProfileForm()
    if form.validate_on_submit():
        if form.admpassword.data == 'helloworld':
            current_user.checkadm = form.checkadm.data
            db.session.commit()
            flash('Были получены права администратора')
            return redirect(url_for('index'))
    return render_template('admprofile.html', title='Администрирование', form=form, user=user)
#Панель Админа
@app.route('/admpanel', methods=['GET', 'POST'])
@login_required
def admPanel():
    return render_template('admpanel.html', title='Администрирование', user=user)
#Панель Покупателя
@app.route('/customerpanel', methods=['GET', 'POST'])
@login_required
def customerPanel():
    return render_template('customerpanel.html', title='Панель покупателя', user=user)
#Создание блюда
@app.route('/create_dish', methods=['GET', 'POST'])
@login_required
def createDish():
    form = CreateDishForm()
    if form.validate_on_submit():
        try:
            db.session.add(Dish(NameDish=form.name.data, DescDish=form.details.data, KcalDish=form.calories.data))
            db.session.flush()
        except exc.IntegrityError:
            db.session.rollback()
        else:
            db.session.commit()
            return redirect(url_for("admPanel"))
    return render_template('create_dish.html', title='Создание блюда', form=form, user=user)
#Создание меню
@app.route('/create_menu', methods=['GET', 'POST'])
@login_required
def createMenu():
    if request.method == 'POST':
        days = Day.query.all()
        eats = Eating.query.all()
        subs = Subscription.query.filter_by(NameSub=request.form['subs']).first()
        menu = request.form['menu_name']
        Monday = [request.form.get('mon_dish1'), request.form.get('mon_dish2'), request.form.get('mon_dish3'), request.form.get('mon_dish4'), request.form.get('mon_dish5')]
        Tuesday = [request.form.get('thu_dish1'), request.form.get('thu_dish2'), request.form.get('thu_dish3'), request.form.get('thu_dish4'), request.form.get('thu_dish5')]
        Wednesday = [request.form.get('wen_dish1'), request.form.get('wen_dish2'), request.form.get('wen_dish3'), request.form.get('wen_dish4'), request.form.get('wen_dish5')]
        Thursday = [request.form.get('thir_dish1'), request.form.get('thir_dish2'), request.form.get('thir_dish3'), request.form.get('thir_dish4'), request.form.get('thir_dish5')]
        Friday = [request.form.get('fri_dish1'), request.form.get('fri_dish2'), request.form.get('fri_dish3'), request.form.get('fri_dish4'), request.form.get('fri_dish5')]
        Saturday = [request.form.get('sat_dish1'), request.form.get('sat_dish2'), request.form.get('sat_dish3'), request.form.get('sat_dish4'), request.form.get('sat_dish5')]
        Sunday = [request.form.get('sun_dish1'), request.form.get('sun_dish2'), request.form.get('sun_dish3'), request.form.get('sun_dish4'), request.form.get('sun_dish5')]
        dishes = [Monday, Tuesday,Wednesday,Thursday, Friday, Saturday, Sunday]
        for i in range(7):
            for j in range(5):
                try:
                    db.session.add(DishInMenu(day=days[i].idDay, menuu=menu, sub=subs.idSub, eat_id=eats[j].idEat, dish=dishes[i][j]))
                    db.session.flush()
                except exc.IntegrityError:
                    db.session.rollback()
                else:
                    db.session.commit()
                print(eats[j].idEat)
        return redirect(url_for("admPanel"))
    elif request.method == 'GET':
        dishes = Dish.query.all()
        subs = Subscription.query.all()
    return render_template('create_menu.html', title='Создание блюда', dishes=dishes, subs=subs)
#Создание подписки
@app.route('/create_subscription', methods=['GET', 'POST'])
@login_required
def createSubscription():
    form = CreateSubscription()
    if form.validate_on_submit():
        try:
            db.session.add(Subscription(NameSub=form.NameSub.data, DescSub=form.DescSub.data,\
                    PriceSub=form.PriceSub.data))
            db.session.flush()
        except exc.IntegrityError:
            db.session.rollback()
            error = f"Same subscription is already registered."
        else:
            db.session.commit()
            return redirect(url_for("admPanel"))
    return render_template('create_subscription.html', title='Создание блюда', form=form, user=user)
#Показать подробности подписки
@app.route('/show_subscriptions', methods=['GET', 'POST'])
@login_required
def showSubs():
    if request.method == 'POST':
        subid = request.form['subid']
        return redirect(url_for("showSubDetails", subid=subid))
    elif request.method == 'GET':
        subs = Subscription.query.all()
        menus_in_sub = {}
        for s in subs:
            dishes = DishInMenu.query.filter_by(sub=s.idSub).all()
            cals = 0
            menus = []
            for d in dishes:
                menus.append(d.menuu)
                cals += Dish.query.filter_by(NameDish=d.dish).first().KcalDish
            menus_in_sub[s.idSub] = set(menus)
            s.KcalSub = cals
    return render_template('show_subscriptions.html', title='Подписки', subs=subs, menus=menus_in_sub)

#Активация подписки
@app.route('/show_sub_details/<subid>', methods=['GET', 'POST'])
@login_required
def showSubDetails(subid):
    now = datetime.now()
    if request.method == 'POST':
        start_date = request.form['odate']
        print(start_date)
        weeks = int(request.form['summator'])
        end_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=7*weeks)).strftime('%Y-%m-%d')
        print("end date =", end_date)
        print(subid)
        price = Subscription.query.filter_by(idSub=subid).first().PriceSub*weeks
        try:
            db.session.add(
                ActSub(user_id=current_user.id, sub_id=subid, StartAct=start_date, EndAct=end_date, PriceSub=price))
            db.session.flush()
        except exc.IntegrityError:
            db.session.rollback()
            error = f"Same sub is already registered."
        else:
            db.session.commit()
        return redirect(url_for("showSubs"))
    elif request.method == 'GET':
            dishes = DishInMenu.query.filter_by(sub=subid).all()
            output = set()
            dict = {}
            eatsDict = {}
            days = Day.query.all()
            eats = Eating.query.all()
            for d in dishes:
                output.add(d.menuu)
            for o in output:
                dict[o] = DishInMenu.query.filter_by(menuu=o).all()
                for eat in eats:
                    eatList = []
                    for f in dict[o]:
                        if (f.eat_id == eat.idEat):
                            eatList.append(f)
                    eatsDict[eat.idEat] = eatList
                    print(eatsDict[eat.idEat])
            sub = Subscription.query.filter_by(idSub=subid).first().NameSub
    return render_template('show_sub_details.html', subid=subid, now=now, menus=output, dishes=dict, subname=sub, eatdict=eatsDict, days=days, eats=eats)
#Подписки пользователя
@app.route('/show_user_subscriptions', methods=['GET', 'POST'])
@login_required
def showUserSubs():
    if request.method == 'POST':
        subid = request.form['subid']
        return redirect(url_for("showSubDetails", subid=subid))
    elif request.method == 'GET':
        subs = ActSub.query.filter_by(user_id=current_user.id).all()
        menus_in_sub = {}
        subnames = {}
        for s in subs:
            dishes = DishInMenu.query.filter_by(sub=s.sub_id).all()
            menus = []
            cals = 0
            for d in dishes:
                menus.append(d.menuu)
                cals += Dish.query.filter_by(NameDish=d.dish).first().KcalDish
            print("diff = ", (s.EndAct - s.StartAct).days/7)
            cals = ((s.EndAct - s.StartAct).days/7)*cals
            print("cals = ", cals)
            subnames[s.idActSub] = [Subscription.query.filter_by(idSub=s.sub_id).first().NameSub, \
                                  Subscription.query.filter_by(idSub=s.sub_id).first().DescSub, cals]
            menus_in_sub[s.idActSub] = set(menus)

    return render_template('show_user_subscriptions.html', title='Подписки пользователя', subs=subs, menus=menus_in_sub, subnames=subnames)
#Показать блюда
@app.route('/show_dishes', methods=['GET', 'POST'])
@login_required
def showDishes():
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        dishes = Dish.query.all()
    return render_template('show_dishes.html', title='Список блюд', dishes=dishes)
#Показать меню Админ
@app.route('/adm_show_menus', methods=['GET', 'POST'])
@login_required
def admShowMenus():
    if request.method == 'POST':
        menu = request.form['menid']
        delete_q = DishInMenu.__table__.delete().where(DishInMenu.menuu==menu)
        db.session.execute(delete_q)
        db.session.commit()
        return redirect(url_for("admShowMenus"))
    elif request.method == 'GET':
            dishes = DishInMenu.query.all()
            menus = []
            for d in dishes:
                menus.append(d.menuu)
            all_menus = set(menus)
    return render_template('adm_show_menus.html', title='Созданные меню', menus=all_menus)
#Показать блюда Админ
@app.route('/adm_show_dishes', methods=['GET', 'POST'])
@login_required
def admShowDishes():
    if request.method == 'POST':
        dish = request.form['dishid']
        delete_q = Dish.__table__.delete().where(Dish.idDish == dish)
        db.session.execute(delete_q)
        db.session.commit()
        return redirect(url_for("admShowDishes"))
    elif request.method == 'GET':
        dishes = Dish.query.all()
    return render_template('adm_show_dishes.html', title='Созданные блюда', dishes=dishes)
#Показать подписик Админ
@app.route('/adm_show_subs', methods=['GET', 'POST'])
@login_required
def admShowSubs():
    if request.method == 'POST':
        sub = request.form['subid']
        print(sub)
        delete_q = Subscription.__table__.delete().where(Subscription.idSub == sub)
        db.session.execute(delete_q)
        db.session.commit()
        return redirect(url_for("admShowSubs"))
    elif request.method == 'GET':
        subs = Subscription.query.all()
    return render_template('adm_show_subs.html', title='Созданные подписки', subs=subs)