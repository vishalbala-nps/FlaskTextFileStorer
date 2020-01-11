from flask import *
from datetime import datetime
app = Flask(__name__)  
 
#Functions
def read_file(fname, ashtml=False):
    title = fname.split("@")[0]
    fcontent = open("./text_files/"+fname)
    content = fcontent.read()
    if ashtml == True:
        content = content.replace("\n","<br />")
    return (title,content)
    
#Main Program Starts Here
@app.route('/')  
def main():  
    return render_template("index.html")  

@app.route('/upload')  
def upload():  
    return render_template("upload_file.html")  
 
@app.route('/upload_success', methods = ['POST'])  
def uploadfile():  
    if request.method == 'POST':  
        f = request.files['file']
        title = request.form.get("fname")
        tstamp = datetime.now().timestamp()
        title = title.replace(" ","_")
        fname = title + "@" + str(int(tstamp))
        f.save("./text_files/"+fname) 

        content = read_file(fname)[1]
        return render_template("details.html", title=title, content=content)

@app.route('/view')
def viewfile():
    fname = request.args.get('fname')
    title = fname.split("@")[0]
    try:
        content = read_file(fname)[1]
    except:
        return "File Does not Exist!"
        
    return render_template("details.html", title=title, content=content)
  
if __name__ == '__main__':  
    app.run(debug=True, port=8080)  