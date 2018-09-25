
# Fast Food Fast

A food delivery web application aimed at testing my understanding of HTML, CSS and Javascript... Languages necessary fro the web development challenges.
Required to create web templates and API endpoints to serve the web templates while implementing pure HTML and CSS (No Libraries or frameworks) and for the server implement a flask server.  
This is the first of a four part series of tests aimed at gauging the level of understanding and the willingness to understand key concepts necessary for web apps development.

## Installation
- The project can be forked from the repo. 
- Install all packages from the requirements.txt file
- From your command line, run the run.py file to start the server.

## Usage
- Access the application from a browser through:
#### http://127.0.0.1:5000/   For the swagger GUI 
- Using post man, or the provided swagger gui test the endpoints.
#### Get:  . . ./v1/orders   Returns all entries present in the list
#### Post: . . ./v1/orders  Adds a new entry to the list.
#### Get:  . . ./v1/orders/id  Gets a specific item by id(an integer)
#### Put:  . . ./v1/orders/id  Updates details for a specific item by id(an integer)
#### Delete:  . . ./v1/orders/id  Delete a specific item by id(an integer) Requires admin access

## Tests
Once the server is running, tests can be performed from the implemented swagger gui:
#### All end Points
![screenshot 73](https://user-images.githubusercontent.com/41139653/46023503-70f9c780-c0ed-11e8-926c-c5ebb157053d.png)
#### Get
![screenshot 75](https://user-images.githubusercontent.com/41139653/46030223-449a7700-c0fe-11e8-97dd-4c4c932126b4.png)
#### Post
![screenshot 76](https://user-images.githubusercontent.com/41139653/46030240-511ecf80-c0fe-11e8-92d1-f44097620236.png)
#### Get (Specific)
![screenshot 77](https://user-images.githubusercontent.com/41139653/46030242-51b76600-c0fe-11e8-9c70-360b808e7708.png)
#### Put (Specific)
![screenshot 78](https://user-images.githubusercontent.com/41139653/46030245-51b76600-c0fe-11e8-8f15-8b65f99389cc.png)
#### Delete (Specific)
![screenshot 79](https://user-images.githubusercontent.com/41139653/46030249-524ffc80-c0fe-11e8-9035-17e3ef718d9d.png)

### Models to guide you during the testing:
![screenshot 74](https://user-images.githubusercontent.com/41139653/46030215-3e0bff80-c0fe-11e8-9d70-ae60e32f2ae1.png)

## Credits

Flask by <br>
Flask Restplus

## License
TODO: Write license
