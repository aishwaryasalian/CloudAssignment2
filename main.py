#import PIL

#from PIL import Image
#import cStringIO
from flask import Flask
from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings
from flask import render_template
from flask import request
import mysql.connector
from mysql.connector import errorcode
#import pyodbc
#import pymysql
import base64
import datetime
import time
#import uuid
#from azure.storage.blob import PublicAccess
#import pymysql
from flask import Flask, render_template, session, request, flash, redirect, url_for

# Obtain connection string information from the portal
#config = {
server ='aishdb.database.windows.net'
username ='aish'
password ='Qwerty123'
database ='AishDb'
#driver= '{ODBC Driver 13 for SQL Server}'
#cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
#}
db = mysql.connector.connect(user="aishdblogin@aishdbserver", password="Qwerty123", host="aishdbserver.mysql.database.azure.com", port=3306, database="apsdb")
cursor = db.cursor()
cursor1 = db.cursor()
cursor2 = db.cursor()
#print (db)
#print ("connection successful")
block_blob_service = BlockBlobService(account_name='aishlogs',
                                      account_key='VnKALk8wpTyN+cgBLwdH6b6mZ/XDYbvCeg5UlBfrdSV37JsaoE+tgo+YQcI1myxdkqB2+wL1h76/BWBVxVsjpA==')
print(block_blob_service)
#block_blob_service.set_container_acl('aishimgcontainer', public_access=PublicAccess.Container)
print ('Blob connected')
newfile = "C:/Users/aishw/Downloads/Cloud computing/Assignment2/Assignment8_Azure-master/images/cat.jpg"
print (newfile)

block_blob_service.create_blob_from_path('aishimgcontainer', 'cat.jpg', newfile,content_settings=ContentSettings(content_type='image/jpg'))
#imgUrl = 'https://mycloudassign.blob.core.windows.net/saipriya/'
app = Flask(__name__)
app.secret_key = "super secret key"

ts = time.time()
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
uid=100
userid=100
uname="aish"


@app.route('/', methods=['POST', 'GET'])
@app.route('/login.html')
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        uname = request.form['Username']
        sql = "select first_name, last_name from user where user_name = '" + uname + "'"
        #print (sql)
        cursor.execute(sql)
        #print(cursor.rowcount)
        results = cursor.fetchall()
        if cursor.rowcount == 1:

            #print(results)
            for row in results:

                return render_template('uploadFiles.html', username=uname, fname=row[0])
        return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/registerPage', methods=['POST', 'GET'])
def registerPage():
    return render_template('register.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
        # check if user is already in session



        uname = request.form['Username']
        fname = request.form['Firstname']
        lname = request.form['Lastname']
        #print(uname)
        #print(lname)
        #sql = "select user_name from user where user_name='" + uname + "'"
        #print(sql)
        #cursor.execute(sql)
        #res=cursor.fetchall();
        #print(res)
        if uname == '' or fname == '' or lname == '':
            flash('Fields cannot be empty')
            return render_template('register.html')

        sql = "insert into user values ('" + uname + "','" + fname + "','" + lname + "')"
        #print(sql)
        cursor.execute(sql)
        #res = cursor.fetchall()
        #print(res)
        db.commit()
        #db.close()
        return '<h1>User Registration successful</h1><br><form action="../"><input type="Submit" value="Login to continue"></form>'


# logout
@app.route('/logout', methods=['POST', 'GET'])
def logout():
    flash('You have been successfully logged out')
    return redirect(url_for('login'))


@app.route('/createAlbum', methods=['POST', 'GET'])
def createAlbum():

    if request.method == 'POST':
        #uname = request.form['Username']
        #fname = request.form['Firstname']
        #lname = request.form['Lastname']
        album_name = request.form['album']
        sql = "select * from album where user_name = '" + uname + "' and Album_name ='" + album_name + "'"
        cursor.execute(sql)
        if cursor.rowcount == 0:
            try:
                sql = "INSERT INTO album (user_name, Album_name, Album_creation_date) values ('" + uname + "','" + album_name + "','" + timestamp + "')"
                cursor.execute(sql)
                db.commit()
                return render_template('upload.html')
            except:
                db.rollback()
        else:
            return '<h1>Album ' + album_name + ' already exists on cloud. Please provide some other album name. </h1><br><form"><input type="button" value="Lets go back" onclick="history.go(-1)"></form>'
    else:
        return render_template('login.html')


def allowed_file(filename):

    #print(filename.rsplit('.', 1)[1].lower())
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploadFiles', methods=['POST', 'GET'])
@app.route('/uploadFiles.html', methods=['POST', 'GET'])
def uploadFiles():
    if request.method == 'POST':
        file_name = request.files['file_upload']
        file_title = request.form['title']
        filename = file_name.filename
        #print(filename)
        #sql = "select * from Image where user_name = '" + uname + "' and Image_name ='" + filename + "'"
        #print(sql)
        #cursor.execute(sql)
        #print(cursor.rowcount)
        newfile = "C:/Users/aishw/Downloads/Cloud computing/Assignment2/Assignment8_Azure-master/images/" + filename
        print(newfile)
        block_blob_service.create_blob_from_path('aishimgcontainer', filename, newfile,
                                                 content_settings=ContentSettings(content_type='image/jpg'))

        # print(file_contents)
        url = "https://aishlogs.blob.core.windows.net/aishimgcontainer/" + filename
        # if len(file_contents) > 1024 * 1024:
        #    return '<h1>File size greater than 1MB</h1><br><form action="../"><input type="Submit" value="Lets go back"></form>'
        #sql = "INSERT into Image(user_name, Title, Image_name, Data, Date_created) VALUES(%s,%s,%s,%s,%s)", uname, file_title, filename, url, timestamp
        sql = "INSERT INTO Image VALUES('" + str(uname) + "','" + str(file_title) + "','" + str(filename) + "','" + str(url) + "','" + str(timestamp) + "')"
        print(sql)
        cursor.execute(sql)
        db.commit()
        return '<h1>Files have been uploaded<h1><br><form"><input type="button" value="Lets go back" onclick="history.go(-1)"></form>'
        # if allowed_file(filename):
        #     file_contents = file_name.read()
        #
        #
        # elif cursor.rowcount > 0:
        #     return '<h1>File ' + filename + '  exists on cloud.  upload other file.</h1><br><form"><input type="button" value="Lets go back" onclick="history.go(-1)"></form>'
        # else:
        #     return '<h1>Incorrect file extension</h1><br><form"><input type="button" value="Lets go back" onclick="history.go(-1)"></form>'
        #return '<h1>Files have been uploaded<h1><br><form"><input type="button" value="Lets go back" onclick="history.go(-1)"></form>'
    #return render_template('login.html')


@app.route('/viewPhotos', methods=['POST', 'GET'])
def viewPhotos():
    # list=[]
    # generator = block_blob_service.list_blobs('aishimgcontainer')
    # for blob in generator:
    #      print(blob.name)
    #      list.append("https://aishlogs.blob.core.windows.net/aishimgcontainer/" + blob.name)
    # print(list[1])
    # return render_template('display.html', img=list)

    sqlQuery = "select  Title, Image_name, Data, Date_created from Image"
    cursor.execute(sqlQuery)
    list = cursor.fetchall();
    print(list)
    return render_template('display.html', list=list)
    # if request.method == 'POST':
    #     photos_array = []
    #     #sql2 = "select Image_ID, Data, Title, Date_Created from Image where Image_ID not in (select Image_ID from rating)"
    #     #print(sql2)
    #     #cursor2.execute(sql2)
    #     #list = cursor2.fetchall()
    #     #print(list)
    #     #print(cursor2.rowcount)
    #     if cursor2.rowcount > 0:
    #         for ind2 in cursor2:
    #             photos_array.append([ind2[0], ind2[1], ind2[2], ind2[3], 0])
    #
    #     sql = "select Image_ID,Data,Title,Date_Created from Image order by Image_ID desc"
    #     #print(sql)
    #     cursor.execute(sql)
    #     res = cursor.fetchall()
    #     #print(res)
    #     # photos_array = []
    #     for ind in cursor:
    #         sql1 = "select image_id, avg(rating) from rating group by %d" % (1)
    #         cursor1.execute(sql1)
    #         for ind1 in cursor1:
    #             if ind1[1] != 0 and ind[0] == ind1[0]:
    #                 photos_array.append([ind[0], ind[1], ind[2], ind[3], ind1[1]])
    #             elif ind1[1] == 0:
    #                 photos_array.append([ind[0], ind[1], ind[2], ind[3], 0])
    #     # print photos_array
    #     return render_template('viewphotos.html', photos=photos_array)


@app.route('/giveRatings/<image_id>', methods=['POST', 'GET'])
def giveRatings(image_id):

    if request.method == 'POST':
        rating = request.form['rating']
        comments = request.form['comments']
        sql = "select * from rating where user_name ='" + uname + "' and image_id ='" + image_id + "'"
        cursor.execute(sql)
        if cursor.rowcount == 0:
            try:
                sql = "insert into rating (user_name,image_id,rating,comments) values('" + uname + "','" + image_id + "','" + rating + "','" + comments + "')"
                cursor.execute(sql)
                db.commit()
                return '<h1>Rating submitted!</h1><br><form><input type="button" value="Lets go back" onclick = "history.go(-2)"></form>'
            except:
                db.rollback()
        else:
            try:
                sql = "update rating set rating ='" + rating + "', comments='" + comments + "' where uid ='" + userid + "' and image_id='" + image_id + "'"
                cursor.execute(sql)
                db.commit()
                return '<h1>Rating updated!</h1><br><form><input type="button" value="Lets go back" onclick = "history.go(-2)"></form>'
            except:
                db.rollback()
    return render_template('giveRatings.html', image_id=image_id)


if __name__ == '__main__':
    app.debug = True
    app.run()
