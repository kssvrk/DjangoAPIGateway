# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask,request
import time

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
port=5496
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/beat')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    #print(app.config)
    #time.sleep(10)
    return f'Hello World on {port}'
 
# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(host='0.0.0.0',port=port)
