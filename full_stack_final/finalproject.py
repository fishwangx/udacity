
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base , Restaurant, MenuItem
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

@app.route('/')
def hello():
    return "Hello , this is new."
    
@app.route('/restaurants/')
@app.route('/restaurants')
def allRestaurants():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    restaurants = session.query(Restaurant).all()

        
    return render_template("restaurants.html",restaurants=restaurants)

@app.route('/restaurants/<int:restaurant_id>/edit',methods=['GET','POST'])
def editRestaurant(restaurant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    myRestaurant= session.query(Restaurant).filter_by(id=restaurant_id).one()

    if request.method=='POST':
        myRestaurant.name= request.form['name']
        session.add(myRestaurant)
        session.commit()
        return redirect('/restaurants')


    return render_template('editrestaurants.html',restaurant=myRestaurant)

@app.route('/restaurants/<int:restaurant_id>/delete',methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    myRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    if request.method=='POST':

        session.delete(myRestaurant)
        session.commit()

        return redirect(url_for('allRestaurants'))
    else:
         return render_template('deleterestaurants.html',restaurant = myRestaurant)

@app.route('/restaurants/create',methods=['GET','POST'])
def createRestaurant():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    if request.method == 'POST':

        new_restaurant = Restaurant(name=request.form['name'])
        session.add(new_restaurant)
        session.commit()
        return redirect(url_for('allRestaurants'))

    else:

        return render_template("createrestaurants.html")



@app.route('/restaurants/<int:restaurant_id>/')
def listRestaurantMenu(restaurant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    myRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)

    return render_template('listrestaurantmenus.html',restaurant=myRestaurant, items=items)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit',methods=['GET','POST'])
def editRestaurantMenu(restaurant_id,menu_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    myMenu = session.query(MenuItem).filter_by(id=menu_id).one()
    myRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()



    if request.method=='POST':
        myMenu.name = request.form['name']
        session.add(myMenu)
        session.commit()

        return redirect(url_for('listRestaurantMenu',restaurant_id = restaurant_id))

    else:
         return render_template("editrestaurantmenus.html",restaurant=myRestaurant,menu=myMenu)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete',methods=['GET','POST'])
def deleteRestaurantMenu(restaurant_id,menu_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    myMenu = session.query(MenuItem).filter_by(id=menu_id).one()
    myRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method=='POST':
        pass
        
    else:


        return render_template("deleterestaurantsmenus.html")

@app.route('/restaurants/<int:restaurant_id>/create')
def createRestaurantMenu(restaurant_id,menu_id):

    return "Create a menu in a restaurant."


if __name__ =="__main__":
    app.debug = True
    app.run(host='0.0.0.0',port=5001)
