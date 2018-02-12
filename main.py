#import PIL

#from PIL import Image
#import cStringIO
from flask import Flask
#from azure.storage.blob import BlockBlobService
#from azure.storage.blob import ContentSettings
from flask import render_template
from flask import request
#from mysql.connector import errorcode
import pyodbc


# Obtain connection string information from the portal
#config = {
server ='aishdb.database.windows.net'
username ='aish'
password ='Qwerty123'
database ='AishDb'
#driver= '{ODBC Driver 13 for SQL Server}'
#cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
#}

# Construct connection string

app = Flask(__name__)


@app.route('/')
def index():
    #print "Hello"
    return render_template('hellouser.html')

@app.route('/loginPage', methods=['get', 'post'])
def loginPage():
    return render_template('login.html')


@app.route('/uploadPage', methods=['get', 'post'])
def uploadPage():
    #print "Hello"
    return render_template('upload.html')

@app.route('/uploadImage', methods=['get', 'post'])
def upload1():
    f = request.files['upload_files']
    file_name = f.filename
    comm = request.form['comments']
    print (file_name)
    newfile = "D:/Cloud_Assignments/Assignment10_Azure/" + file_name
    print (newfile)
    # block_blob_service.create_blob_from_path('saipriya', file_name, newfile,
    #                                          content_settings=ContentSettings(content_type='image/png'))
    # imgUrl = 'https://mycloudassign.blob.core.windows.net/saipriya/' + file_name
    # insertQuery = "insert into Photo (img) values ('%s')" % (imgUrl)
    # #print insertQuery
    # cur = myConnection.cursor()
    # cur.execute(insertQuery)
    # query1 = 'select img from Photo'
    # cur.execute(query1)
    # res = cur.fetchall()
    # myConnection.commit()
    return 'File uploaded successfully'


@app.route('/viewImages' , methods=['get', 'post'])
def viewImages():
 return render_template('list.html')

@app.route('/list', methods=['get', 'post'])
def list():
    # list=[]
    # generator = block_blob_service.list_blobs('saipriya')
    # for blob in generator:
    #     print(blob.name)
    #     list.append("https://mycloudassign.blob.core.windows.net/saipriya/" + blob.name)
    # print list[1]
    return render_template('display.html', img=list)


@app.route('/show', methods=["GET"])
def showUserData():
    imageList = []
    query = "SELECT * FROM Photo where photo_id=23"
    # cur = myConnection.cursor()
    # cur.execute(query)
    # result = cur.fetchall()
    # for row in result:
    #     image = b64encode(row[3])
    #     imageList.append(image)
    #print datetime.now()
    return render_template("display.html", image=imageList)


if __name__ == '__main__':
    app.run()
