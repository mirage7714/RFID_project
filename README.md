# RFID_project
Simple web page build with Flask. It contains login/register page, user admin, user edit and delete function.  

- To run the app, first install required packages:  
  ```
  pip install -r requirements.txt
  ```
  After packages are installed, then execute the app:  
  ```
  python app.py
  ```  

- Or can use docker to run the app:   
  First build docker images
  ```
  docker build -t webservice .
  ```
  Then run docker containers:  
  ```
  docker run --rm -p 5000:5000 -it webservice
  ```
