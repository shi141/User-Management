from flask import Flask,render_template,request,redirect,url_for,session,jsonify,make_response
from flask_mysqldb import MySQL
import re
from logging import FileHandler,WARNING
from flask_cors import CORS,cross_origin


app = Flask(__name__,template_folder="template")
CORS(app,methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"])

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'hello@123'
app.config['MYSQL_DB'] = 'user'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
 
mysql = MySQL(app)

# CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000/"}})


@app.route('/')  
def get_data():
    # if request.method=="POST":
    cursor=mysql.connection.cursor()
    cursor.execute("select * from user_data ;")
    userss=cursor.fetchall()
    users=[]
    for x in userss:
        dict={}
        dict.update({'id':x[0]})
        dict.update({'name':x[1]})
        dict.update({'department':x[2]})
        dict.update({'email':x[3]})
        dict.update({'role':x[4]})
        dict.update({'contact':x[5]})
        users.append(dict)
    response=jsonify(users)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@app.route('/delete_user/<int:id>',methods=['DELETE'])
def delete_user(id):
    print(id)
    cursor=mysql.connection.cursor()
    query = "delete from user_data where id=%s"
    cursor.execute(query, (id,))
    mysql.connection.commit() 
    cursor.close()
    response=make_response("User deleted")
    response.headers.add("Access-Control-Allow-Methods", "DELETE, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    data=response.data.decode('utf-8')
    return jsonify({'message': data})

@app.route('/add_user',methods=['POST'])
def add_user():
    data=request.get_json()
    # print(data)
    name = data["name"]
    email = data['email']
    department = data['department']
    role = data['role']
    contact = data['numb']
    # print(name,email,department,role,contact)
    cursor=mysql.connection.cursor()
    query = "INSERT INTO user_data (name, email, department, role, contact) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (name, email, department, role, contact))
    mysql.connection.commit() 
    cursor.close()
    cursor=mysql.connection.cursor()
    query = "select * from user_data where name=%s AND email=%s AND department=%s AND role=%s AND contact=%s"
    cursor.execute(query, (name,email,department,role,contact,))
    result=cursor.fetchall()
    # print(result)
    mysql.connection.commit() 
    cursor.close()
    
    dictionary={}
    for i in result:
        dictionary['id']=i[0]
        dictionary['name']=i[1]
        dictionary['department']=i[2]
        dictionary['email']=i[3]
        dictionary['role']=i[4]
        dictionary['contact']=i[5]
    print(dictionary)
    response=make_response(dictionary)
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    return response

@app.route('/edit_user/<int:user_id>',methods=['PUT'])
@cross_origin()
def edit_user(user_id):
    data=request.get_json()
    print("edit user")
    print(data)
    id=user_id
    name = data["name"]
    email = data['email']
    department = data['department']
    role = data['role']
    contact = data['contact']
    cursor=mysql.connection.cursor()
    query = "UPDATE user_data SET name = %s, email = %s,department=%s,role=%s,contact=%s where id=%s;"
    cursor.execute(query, (name, email, department, role, contact,id))
    mysql.connection.commit() 
    updated_dict={'id':id,'name':name,'email':email,'department':department,'role':role,'contact':contact}
    print("query")
    cursor.close()
    # return jsonify({updated_dict}),200
    response = make_response(updated_dict)
    response.headers.add("Access-Control-Allow-Methods", "PUT, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    return response



# @app.route('/')
# def form():
#     return render_template('doc.html')

# @app.route('/')
# def dash():
#     return render_template('new.html')



# @app.route('/view')
# def view_detail():
#     return render_template('view.html')
    
# @app.route("/")
# def index():
#     cursor=mysql.connection.cursor()
#     cursor.execute("select name from user_data where department='development';")
#     users=cursor.fetchall()
#     cursor.close()
#     return render_template('dif.html',users=users)

# @app.route('/')
# def index():
#     return render_template("button.html")





# @app.route('/')
# def rolpage():
#     return render_template('role.html')

# @app.route('/role')
# def role():
#     pass


# @app.route('/update')
# def update():
#     user_data = user_list()
#     role_data = role()
#     return render_template('update.html',user_data=user_data,role_data=role_data)

# @app.route('/show_detail')
# def show_detail():
#     users=user_list()
#     return render_template('index.html',users=users)

# @app.route('/show_data')
# def show_data():
#     data = request.args.get('data')
#     data = json.loads(data)  # Convert the data from JSON to a Python object
#     print(data)
#     roles=role()
#     return render_template('update.html', data=data,roles=roles)

# @app.route('/new_data',methods=['POST'])
# def new_data():
#     data = request.get_json()
#     user_id = data['userId']
#     selected_value = data['selectedValue']
#     print(user_id,selected_value)
#     cursor = mysql.connection.cursor()
#     cursor.execute("UPDATE user_data SET role = %s WHERE id = %s", (selected_value, user_id))
#     mysql.connection.commit()
#     cursor.close()

    # Return a response indicating success or failure
#     return jsonify({'status': 'success'})



# @app.route('/update_list', methods=['GET'])
# def update_list():
#     try:
#         user_id = request.args.get('user')
#         # Check if both parameters are present
#         if not user_id:
#             return jsonify({'status': 'error', 'message': 'Missing parameters'}), 400
#         cursor=mysql.connection.cursor()
#         cursor.execute("select * from user_data where id=%s ;",(user_id,))
#         update_user_data=cursor.fetchone()
        
#         print(update_user_data)
        
#         return jsonify(update_user_data)
#     except Exception as e:
#         print(f'Error: {e}')
#         return jsonify({'status': 'error', 'message': 'Internal server error'}), 500
    

        




# # _______________________________________________ROLE________________________________________________________
 
# def user_list():
#     cursor=mysql.connection.cursor()
#     cursor.execute("select * from user_data ;")
#     userss=cursor.fetchall()
#     users=[]
#     for i in userss:
#         users.append(i)
#     return list(users)

# def role():
#     cursor=mysql.connection.cursor()
#     cursor.execute("select * from role ;")
#     roles=cursor.fetchall()
#     data=[]
#     for role in roles:
#         data.append(role)
#     return data
# # render_template("up.html",roles=data)

# @app.route('/dashboard')
# def show_database():
#     user_data = user_list()
#     role_data = role()
#     return render_template('dashboard.html',user_data=user_data,role_data=role_data)


        
@app.route('/update_database', methods=['GET'])
def update_database():
    try:
        user_id = request.args.get('userId')
        selected_value = request.args.get('selectedValue')
        print(user_id,selected_value)
        print("recieved recieved")

        # Check if both parameters are present
        if not user_id or not selected_value:
            return jsonify({'status': 'error', 'message': 'Missing parameters'}), 400

        cursor=mysql.connection.cursor()
        cursor.execute("update user_data set role=(%s) where id=(%s) ",(selected_value,user_id))
        mysql.connection.commit()
        cursor.close()

        

        # Respond with success
        return jsonify({'status': 'success'})
    except Exception as e:
        # Print the exception and return a 500 error
        print(f'Error: {e}')
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

if __name__=="__main__":
    app.run(debug=True,port=80)