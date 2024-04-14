import os
import time
import glob
import shutil
from flask import Flask, redirect, render_template, request, send_file

# Configure Application
app = Flask(__name__)

global filename
global ftype

@app.route("/")
def home():

    # Delete old files
    filelist = glob.glob("uploads/*")
    for f in filelist:
        os.remove(f)
    filelist = glob.glob("downloads/*")
    for f in filelist:
        os.remove(f)
    return render_template("home.html")

app.config["FILE_UPLOADS"] = "C:/Users/16047/Downloads/python-project/uploads"

@app.route("/compress", methods=["GET", "POST"])
def compress():

    if request.method == "GET":
        return render_template("compress.html", check=0)

    else:
        up_file = request.files["file"]

        if len(up_file.filename) > 0:
            global filename
            global ftype
            filename = up_file.filename
            print(up_file.filename)
            up_file.save(os.path.join(app.config["FILE_UPLOADS"], filename))
            
            
            os.system("g++ huffcompress.cpp -o huffcompress")
            os.system("huffcompress uploads/{}".format(filename))
            
            # os.system("huffcompress.cpp uploads/{}".format(filename))
            
            
            filename = filename[:filename.index(".",1)]
            ftype = "-compressed.bin"
            while True:
                    print("shooter")
                    # os.system("mv uploads/{}-compressed.bin downloads/".format(filename))
                    source_path = "uploads/{}-compressed.bin".format(filename)
                    destination_path = "downloads/"
                    shutil.move(source_path, destination_path)
                    break
                
            print("3r3r")
            return render_template("compress.html", check=1)

        else:
            print("ERROR")
            return render_template("compress.html", check=-1)

@app.route("/decompress", methods=["GET", "POST"])
def decompress():

    if request.method == "GET":
        return render_template("decompress.html", check=0)

    else:
        up_file = request.files["file"]

        if len(up_file.filename) > 0:
            global filename
            global ftype
            filename = up_file.filename
            print(up_file.filename)
            up_file.save(os.path.join(app.config["FILE_UPLOADS"], filename))
            print("shooter2")
            
            

            # os.system("./d uploads/{}".format(filename))
            os.system("g++ huffdecompress.cpp -o huffdecompress")
            os.system("huffdecompress uploads/{}".format(filename))
            print("shooter3")

            f = open("uploads/{}".format(filename), 'rb')
            ftype = "-decompressed." + (f.read(int(f.read(1)))).decode("utf-8")
            filename = filename[:filename.index("-",1)]
            

            while True:
                    print("shooter")
                    # os.system("mv uploads/{}-compressed.bin downloads/".format(filename))
                    source_path = "uploads/{}-decompressed.txt".format(filename)
                    destination_path = "downloads/"
                    shutil.move(source_path, destination_path)
                    break
       
            print("3r3r")
            return render_template("decompress.html", check=1)

        else:
            print("ERROR")
            return render_template("decompress.html", check=-1)






@app.route("/download")
def download_file():
    global filename
    global ftype
    path = "downloads/" + filename + ftype
    return send_file(path, as_attachment=True)




# Restart application whenever changes are made
if __name__ == "__main__":
    app.run(debug = True)