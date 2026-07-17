from flask import Flask,request,jsonify,render_template
from db import getConnection

app = Flask("__name__")

# api for checking connection
@app.route("/")
def home():
     # d = {"message":"server running well"}
     # return jsonify(d)
     return render_template("index.html")


# api to insert customer data
@app.route("/insertData",methods=["POST"])
def insertData():

     data = request.get_json()
     
     cname = data["name"]
     cmobile = data["mob"]
     cemail = data["email"]
     caccno = data["accno"]
     cbalance = data["balance"]
     password = "Test@123"
     
     conn = getConnection()
     cmd = conn.cursor()
     cmd.execute('''
                 INSERT INTO CUSTOMER
                 (cname,cmobile,cemail,accno,balance,password) 
                 values 
                 (%s,%s,%s,%s,%s,%s);'''
                 ,(cname,int(cmobile),cemail,caccno,cbalance,password))
     conn.commit()
     conn.close()
     return jsonify({"message":f"{cname} is inserted to db"})

# api to delete customer data
@app.route("/deleteCustomer",methods=["POST"])
def deleteCustomer():
     
     data = request.get_json()
     
     caccno = data["accno"]
     
     conn = getConnection()
     cmd = conn.cursor()
     cmd.execute("DELETE FROM customer WHERE accno=%s",(caccno,))
     conn.commit()
     conn.close()
     return jsonify({"message":f"{caccno} person data deleted!!!!"})

# api to update the customer details
@app.route("/updateCustomer",methods=["POST"])
def updateCustomer():
     
     data = request.get_json()
     caccno = data["caccno"]
     uname = data["uname"]
     umobile = data["umobile"]
     uemail = data["uemail"]
     upassword = data["upassword"]
     

     conn = getConnection()
     cmd = conn.cursor(dictionary=True)
     cmd.execute("SELECT cname,cmobile,cemail,password FROM customer")
     d = cmd.fetchone()
     conn.close()
     
     cname = d["cname"]
     cmobile = int(d["cmobile"])
     cemail  = d["cemail"]
     cpassword = d["password"]
     
     if uname == "":
          uname = cname
          
     if umobile == "":
          umobile = cmobile
          
     if uemail == "":
          uemail = cemail
          
     if upassword == "":
          upassword = cpassword
     
     

     conn = getConnection()
     cmd = conn.cursor()
     cmd.execute('''
                 UPDATE CUSTOMER
                 SET
                 cname=%s,
                 cmobile=%s,
                 cemail=%s,
                 password=%s
                 where accno=%s''',
                 (uname,umobile,uemail,upassword,caccno))
     conn.commit()
     conn.close()
     
     return jsonify({"message":f"{caccno} i received data"})


# api for fetching all records from db
@app.route("/viewAllCustomers",methods=["GET"])
def viewAllCustomers():

     conn = getConnection()
     cmd = conn.cursor(dictionary=True)
     cmd.execute("SELECT sno,cname,cmobile,cemail,accno,balance FROM CUSTOMER")
     result = cmd.fetchall()
     conn.close()
     return jsonify({"data": result})
     
# api for athentication of admin
@app.route("/adminLogin",methods=["POST"])
def adminLogin():
     
     data = request.get_json()
     
     checkUser = data["username"]
     checkPassword = data["password"]
     
     conn = getConnection()
     cmd = conn.cursor()
     cmd.execute("SELECT * FROM ADMIN where username=%s and password=%s",(checkUser,checkPassword))
     result = cmd.fetchone()
     conn.close()
     
     if result == None:
          return jsonify({"message":"Login failed"})
     else:
          return jsonify({"message":"Login success"})
     
if __name__ == "__main__":
     app.run(debug=True)