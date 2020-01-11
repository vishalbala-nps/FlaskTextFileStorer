from flask import *
from datetime import datetime
import json
import time

app = Flask(__name__)  
 
#Functions
def read_file(fname):
    title = fname.split("@")[0]
    fcontent = open("./text_files/"+fname)
    content = fcontent.read()
    return (title,content)

def add_in_json(fname, title, tstamp):
    with open("./text_files/files.json", 'r+') as f:
        flist = json.load(f)
    print(flist)
    date_pub = datetime.fromtimestamp(tstamp)
    date_pub = date_pub.strftime("%Y-%m-%d %H:%M:%S")
    print(date_pub)
    flist.append({"name":fname,"title":title,"url":"/view?fname="+fname,"date":date_pub})
    with open("./text_files/files.json", 'w') as f:
        json.dump(flist, f)

#Main Program Starts Here
@app.route('/')  
def main(): 
    with open("./text_files/files.json", 'r+') as f:
        flist = json.load(f)
    return render_template("index.html", flist=flist)  
 
@app.route('/upload', methods = ['POST'])  
def uploadfile():  
    if request.method == 'POST':  
        f = request.files['file']
        title = request.form.get("fname")
        print(title)
        tstamp = datetime.now().timestamp()
        fname = title + "@" + str(int(tstamp))
        f.save("./text_files/"+fname)
        add_in_json(fname, title,tstamp)

        return redirect("/view?fname="+fname)


@app.route('/view')
def viewfile():
    fname = request.args.get('fname')
    title = fname.split("@")[0]
    try:
        content = read_file(fname)[1]
    except:
        return "File Does not Exist!"
        
    return render_template("details.html", title=title, content=content, downloadurl="/download_file?fname="+fname)

@app.route('/download_file')
def downloadfile():
    fname = request.args.get('fname')
    title = fname.split("@")[0]
    try:
        return send_file("./text_files/"+fname, attachment_filename=title+".txt", as_attachment=True)
    except:
        return "File Does not Exist!"


  
if __name__ == '__main__':  
    app.run(debug=True, port=8080)  