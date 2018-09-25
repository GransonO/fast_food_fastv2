
# Fast Food Fast

A food delivery web application aimed at testing my understanding of **HTML, CSS** and **Javascript**... Languages necessary fro the web development challenges. <br>
Required to create web templates and API endpoints to serve the web templates while implementing pure HTML and CSS **(No Libraries or frameworks)** and for the server implement a **flask server**. <br>
This is a four part series of tests aimed at gauging the level of understanding and the willingness to understand key concepts necessary for web apps development.

## Installation
- Ensure you have python installed in your development environment
- The project can be forked from the repo into a local folder.
##### From the bash:
- Create a virtual environment to house all the packages
> ` $ pip install virtualenv`
- create the environment:
> ` $ virtualenv my-env`
- Start the newly created virtual environment:

###### For windows:
> `$ source my-env/Scripts/activate`

###### For unix:
> `$ source my-env/bin/activate`

- Install all packages from the requirements.txt file
> `$ pip install -r requirements.txt`

- From your command line, cd into server and run the run.py file to start the server
> `$ python run.py`

## Usage
- Access the application from a browser through:
>>> http://127.0.0.1:5000/   
- The index page is an implementation of the swagger GUI from RestPlus
- Using post man, or the provided swagger gui test the endpoints.

| EndPoint | Https Request | Description |
| --- | --- | --- |
| `.../v1/orders` | GET | Retrieves all items |
| `.../v1/orders` | POST | Adds a new item |
| `.../v1/orders/int` | GET | Retrieves a specific item by id |
| `.../v1/orders/int` | PUT | Updates details for a specific item by id |
| `.../v1/orders/int` | DELETE | Delete a specific item by id |

## Tests
While the server is running, tests can be performed from the implemented swagger gui:
#### All end Points
![screenshot 73](https://user-images.githubusercontent.com/41139653/46023503-70f9c780-c0ed-11e8-926c-c5ebb157053d.png)
#### Get
##### Retrieves all items from the list.
![screenshot 75](https://user-images.githubusercontent.com/41139653/46030223-449a7700-c0fe-11e8-97dd-4c4c932126b4.png)
#### Post
##### Adds a new item into the list.
![screenshot 76](https://user-images.githubusercontent.com/41139653/46030240-511ecf80-c0fe-11e8-92d1-f44097620236.png)
#### Get (Specific)
##### Retrieves specific items from the list.
![screenshot 77](https://user-images.githubusercontent.com/41139653/46030242-51b76600-c0fe-11e8-9c70-360b808e7708.png)
#### Put (Specific)
##### Updates specific items in the list.
![screenshot 78](https://user-images.githubusercontent.com/41139653/46030245-51b76600-c0fe-11e8-8f15-8b65f99389cc.png)
#### Delete (Specific)
##### Deletes an item from the list.
![screenshot 79](https://user-images.githubusercontent.com/41139653/46030249-524ffc80-c0fe-11e8-9035-17e3ef718d9d.png)

### Models to guide you during the testing:
![screenshot 74](https://user-images.githubusercontent.com/41139653/46030215-3e0bff80-c0fe-11e8-9d70-ae60e32f2ae1.png)

## Credits
- [Flask](http://flask.pocoo.org/docs/1.0/)
- [Flask Restplus](https://flask-restplus.readthedocs.io/en/stable/)

## License
This is an Andela Project created ny Me!
