# (Reworked)
# fast_food_fast V2
A food delivery web application aimed at testing my understanding of HTML, CSS and Javascript... Languages necessary fro the web development challenges

This is the first of a four part series of tests aimed at gauging the level of understanding and the willingness to understand key concepts necessary for web apps development.

# Necessary Guidelines
### User signup and signin pages.
### A page where a user should be able to order for food.
### A page where the Admin can do the following:
### See a list of orders.
### Accept and decline orders.
### Mark orders as completed.
### A user should be able to see a history of ordered food.
No usage of web frameworks in the project. All ideas born from the root.

### For the second piece of this project:
Required to implement API end points that would serve the front end templates. The end points should be as:
#### (GET)      .../v1/orders     Get all orders
#### (GET)      .../v1/orders/1   get specific order
#### (POST)     .../v1/orders     Post new order
#### (PUT)      .../v1/orders/1   Edit a specific order
#### (DELETE)   .../v1/orders/1   Delete a specific order

For testing, access the different API enspoints using Postman from the link:
http://fast-food-fast-v2.herokuapp.com/

Swagger, A restplus gui has been implemented which documents the API and supports testing. Alternatively, you can fork the repo to your local machine and run the run.py file to start the flask server. You can then access the different end points using the url:
http://localhost:5000/

And use postman for the testing.
P.S The data is not maintained as the project implements a simple data structure that only holds data but does not save.

#### Pivotal tracker:
https://www.pivotaltracker.com/n/projects/2198167

#### Screenshots:
#### API Endpoints
![screenshot 73](https://user-images.githubusercontent.com/41139653/46023503-70f9c780-c0ed-11e8-926c-c5ebb157053d.png)

#### Required Models
![screenshot 74](https://user-images.githubusercontent.com/41139653/46023518-76efa880-c0ed-11e8-8614-77b8499fca47.png)

