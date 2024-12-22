from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_scss import Scss



app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myappdatabase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)

class myTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, default=datetime.today)
    complete = db.Column(db.Integer, default=0)
    
        
    def __repr__(self) -> str:
        return f"Task {self.id}"
        
with app.app_context():
        db.create_all()   
    
    
    
@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        current_task = request.form["content"]
        newTask = myTask(content=current_task)
        try:
            db.session.add(newTask)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"
    else:
        tasks = myTask.query.order_by(myTask.created).all()
        return render_template("index.html", tasks=tasks)
 
 
 
    
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = myTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f"ERROR:{e}")
        return f"ERROR:{e}"

    
    
@app.route("/update/<int:id>",methods=["POST", "GET"])
def update(id:int):
    task = myTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form["content"]
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
         print(f"ERROR:{e}")
         return f"ERROR:{e}"
    else:
        return render_template("update.html", task=task)




if __name__ == "__main__":  
      
    app.run(debug=True)

