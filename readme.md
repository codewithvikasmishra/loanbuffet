1. First Create an Virtual Environment
   
    a. All commands need to run in cmd

    b. to install the virtual environment
    pip install virtualenv

    c. to create a virtual environment by name env
        virtualenv loanbuffet_env

    d.to activate the environment
    loanbuffet_env\scripts\acivate.bat

3. Set up connection with MongoDB
    You need to create an account on https://www.mongodb.com/ with Try free. You will create there id, password, name space and database.

    a. Create New Project
        i. Name your Project
        ii. next
        iii. add members (skip that part) and click on "Create Project"
    b. select your project creted in step 1
        i. Create Cluster or build a cluster
        ii. Go with the "Shared Clusters" as its only a free one
        iii. Cloud Provider and Region
            1. select any one AWS, Google or Azure (I selected AWS)
        iv. Recommended Region
            1. Select Mumbai
        v. Cluster Tier
            1. Select "MO Sandbox", that is only free
        vi.Then click on create (if you do not wish to change Cluster name)
        vii. It will take 3-5 min approx to create
    c. Once cluster is created click on "connect" under your created cluster
        i. First read and then only connect (its a disclaimer)
        ii. Under "Add a connection IP address"
            1. Allow access from anywhere
            2. Add IP address
        iii.Create a database User
            1. Remember id and Pwd which you fill below
        iv. choose a connection method
        v. connect your application
            1.Driver - select python
            2.version - the version which you have in your machine
        vi. Add your connection string into your application code
            1. Check box "Include full driver code example"
            2. Copy the link below
    d. Also, need to install pymongo in your local
    pip install pymongo[srv]
    e. Click on "collections"/"browse collection"

4. Issues while creating HTML forms
    1. How to change background colour and make header, footer?
    2. How to give image on social media names?
    3. How to pass data from HTML forms to Database?
    4. How to validate login credentials from Db?
    5. How to pass "email" from one function to another another function?
        a. https://vegibit.com/how-to-use-sessions-in-python-flask/
        b. https://www.geeksforgeeks.org/how-to-use-flask-session-in-python-flask/
        c. Both links helps me a lot and I get to know about session.
    6. I get to know about secret_key while validating in login page

5. I understand after creating db in mongodb, that pwd should inserted in DB as hash value

6. Libraries I installed
    1. pip install Flask-Session
    2. pip install passlib
    3. pip install pymongo[srv]

7. I used Google Colab for my hit and trial methods.
