from database_setup import Base, Restaurant, MenuItem
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask import Flask, render_template, request, redirect, url_for , flash ,jsonify
app = Flask(__name__)


engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine



@app.route("/restaurants/<int:restaurant_id>/")
def restaurantMenu(restaurant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()


    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)

    return render_template('menu.html', restaurant=restaurant, items=items)

# Task 1: Create route for newMenuItem function here


@app.route("/restaurants/<int:restaurant_id>/new_menu", methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()


 
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item << %s >> created!" % newItem.name)

        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))

    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)
# Task 2: Create route for editMenuItem function here


@app.route("/restaurants/<int:restaurant_id>/<int:menu_id>/edit_menu", methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()

    if request.method == 'POST':
            if request.form['name']:
                old_name = editedItem.name
                editedItem.name = request.form['name']
            session.add(editedItem)
            session.commit()
            flash(" menu item << %s >> edited to %s !" % (old_name,editedItem.name))

            return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
            # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
            # SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
            return render_template(
                'editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)

# Task 3: Create a route for deleteMenuItem function here

@app.route("/restaurants/<int:restaurant_id>/<int:menu_id>/delete_menu",methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    item = session.query(MenuItem).filter_by(id=menu_id).one()

    if request.method=="POST":
        session.delete(item)
        session.commit()
        flash("new menu item << %s >> deleted!" % item.name)

        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))

    else:
        return render_template('deletemenuitem.html',restaurant_id=restaurant_id,menu_id=menu_id,item=item)


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJson(restaurant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()
    return jsonify(MenuItems=[i.serialize for i in items])





if __name__ =="__main__":
    app.secret_key = 'super_secret_key'

    app.debug = True
    app.run(host='0.0.0.0',port=5000)
