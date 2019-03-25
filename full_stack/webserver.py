from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant , MenuItem

engine = create_engine("sqlite:///restaurantmenu.db")

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()




class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        try:

            if self.path.endswith("/delete"):

                restaurantId = self.path.split("/")[2]

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()


                output = ""
                output += "<html><body>"

                output += '''<form method='POST' enctype='multipart/form-data' action="/restaurant/%s/delete"><h2> Sure to delete?</h2><input type="submit" value="Submit"> </form>''' % restaurantId

             

                output += "</body></html>"


                self.wfile.write(output)
                print output



            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"

                self.wfile.write(output)
                print output

                return

            if self.path.endswith("/yu"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"

                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants"):
                """List all of the restaurants!"""
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurants = session.query(Restaurant).all()

                output = ""
                output += "<html><body>"
                for r in restaurants:
                    print r.name


                    output += "<p>" + r.name + "</p>"
                    output += '<p><a href=/restaurant/'+str(r.id)+'/edit>Edit</a></p>'
                    output += '<p><a href="/restaurant/%s/delete">Delete</a></p>' % str(r.id)
                    output += " </br>"



                output += "</body></html>"


                self.wfile.write(output)
                print output

            if self.path.endswith("/restaurants/new"):

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurants = session.query(Restaurant).all()

                output = ""
                output += "<html><body>"

                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>What is the name of the new Restaurant?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''

             

                output += "</body></html>"


                self.wfile.write(output)
                print output

            if self.path.endswith("/edit"):


                restaurantId = self.path.split("/")[2]

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()


                output = ""
                output += "<html><body>"

                ## 一下按submit 按钮后，会走到action中的URL ，然后到 do_POST 里

                output += '''<form method='POST' enctype='multipart/form-data' action="/restaurant/%s/edit"><h2>What is the name of the new name?</h2><input name="new_name" type="text" ><input type="submit" value="Submit"> </form>''' % restaurantId

             

                output += "</body></html>"


                self.wfile.write(output)
                print output






            
   
            
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


    def do_POST(self):

        try:


            if self.path.endswith("/delete"):

                delete_restaurant_id = self.path.split("/")[2]

                restaurant_chosen = session.query(Restaurant).filter_by(id=delete_restaurant_id).one()

                session.delete(restaurant_chosen)
                session.commit()
                self.send_response(301)
                self.send_header('Location','/restaurants')
                self.end_headers()



            if self.path.endswith("restaurants/new"):

                self.send_response(301)
                self.send_header('Content-type','text/html')
                self.end_headers()
                ctype,pdict =cgi.parse_header(self.headers.getheader('Content-type'))

                if ctype =='multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile,pdict)
                    messagecontent = fields.get('message')


                output = ""
                output += "<html><body>"
                output += "<html><body>"
                output += " <h2> Okay, following restaurant has been added! </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]

                if messagecontent[0]:

                    new_restaurant = Restaurant(name=messagecontent[0])
                    session.add(new_restaurant)
                    session.commit()
        



                output += '''Check for it! <a href="/restaurants">All Restaurants</a>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output

            if self.path.endswith("/edit"):

                restaurantId = self.path.split("/")[2]

                restaurant_chosen = session.query(Restaurant).filter_by(id=restaurantId).one()

            
                ctype,pdict =cgi.parse_header(self.headers.getheader('Content-type'))

                if ctype =='multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile,pdict)
                    messagecontent = fields.get('new_name')

                if messagecontent[0]:
                    restaurant_chosen.name = messagecontent[0]
                    session.add(restaurant_chosen)
                    session.commit()

                self.send_response(301)
                self.send_header('Location','/restaurants')
                self.end_headers()


        except:

            pass






def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
