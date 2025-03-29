from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    dob = db.Column(db.String(10))  # YYYY-MM-DD
    amount_due = db.Column(db.Float)

with app.app_context():
    db.create_all()

@app.route('/student', methods=['POST'])
def create_student():
    data = request.json
    new_student = Student(**data)
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'message': 'Student created successfully'}), 201

@app.route('/student/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = Student.query.get_or_404(student_id)
    return jsonify({
        'student_id': student.student_id,
        'first_name': student.first_name,
        'last_name': student.last_name,
        'dob': student.dob,
        'amount_due': student.amount_due
    })

@app.route('/student/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = Student.query.get_or_404(student_id)
    data = request.json
    for key, value in data.items():
        setattr(student, key, value)
    db.session.commit()
    return jsonify({'message': 'Student updated successfully'})

@app.route('/student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted successfully'})

@app.route('/students', methods=['GET'])
def get_all_students():
    students = Student.query.all()
    return jsonify([
        {
            'student_id': s.student_id,
            'first_name': s.first_name,
            'last_name': s.last_name,
            'dob': s.dob,
            'amount_due': s.amount_due
        } for s in students
    ])

if __name__ == '__main__':
    app.run(debug=True)