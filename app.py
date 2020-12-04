from flask import Flask,jsonify, request,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret key"

# SqlAlchemy Database Configuration With Mysql

app.config.from_object('user_crud.task.config.Config')  #path
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Creating model table for our CRUD database
class Book(db.Model):
    __tablename__= 'book_details'
    id= db.Column(db.Integer, primary_key=True)
    bname = db.Column(db.String(100))
    aname = db.Column(db.String(100))

    def __init__(self,bname, aname):
        self.bname = bname
        self.aname = aname

    @staticmethod
    def serialize(id,bname,aname):
        return {"id":id,
                "book_name":bname.strip(),
                "author_name":aname.strip() }

@app.route('/create', methods=['POST'])
def create_book():
    if request.method=='POST':
        bname = request.form['bname']
        aname = request.form['aname']

        new_book = Book(bname,aname)
        db.session.add(new_book)
        db.session.commit()
        return 'Book Created Successfully'


@app.route('/', methods=['GET'])
def get_all_books():
    if request.method == 'GET':
        books= Book.query.all()
        #print(books)
        res=[]
        for book in books:
            res.append(Book.serialize(book.id, book.bname, book.aname))
        return jsonify(res)

@app.route('/update', methods=['PUT'])
def update():
    if request.method == 'PUT':
        book = Book.query.get(request.form['id'])
        book.bname = request.form['bname']
        book.aname = request.form['aname']

        db.session.commit()
        flash("Book Updated Successfully")
        return jsonify(Book.serialize(book.id,book.bname,book.aname))

# This route is for deleting our book
@app.route('/delete/<id>/', methods=['DELETE'])
def delete(id):
    book= Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
   # flash("Book Deleted Successfully")
    return "book deleted "


if __name__ == "__main__":
    app.run(port=8002)



