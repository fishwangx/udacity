from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello , this is new."

@app.route('/restaurants')
def allRestaurants():

    return render_template("restaurants.html")

@app.route('/restaurants/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):

    return "edit a restaurant."

@app.route('/restaurants/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
    return "Delete a restaurant"

@app.route('/restaurants/create')
def createRestaurant():

    return "Create a restaurant."



@app.route('/restaurants/<int:restaurant_id>/')
def listRestaurantMenu(restaurant_id):

    return "List menus in a restaurant"

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit')
def editRestaurantMenu(restaurant_id,menu_id):

    return "edit a restaurant menu."

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete')
def deleteRestaurantMenu(restaurant_id,menu_id):
    return "Delete a restaurant menu"

@app.route('/restaurants/<int:restaurant_id>/create')
def createRestaurantMenu(restaurant_id,menu_id):

    return "Create a menu in a restaurant."


if __name__ =="__main__":
    app.debug = True
    app.run(host='0.0.0.0',port=5001)
