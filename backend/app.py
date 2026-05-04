from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# CLASS
class Student:
    def __init__(self, id, name, course=None):
        self.id = id
        self.name = name
        self.course = course

    def to_dict(self):
        return {"id": self.id, "name": self.name, "course": self.course}

# data holder
students = [
    Student(1, "Akida Mwaura", "Software Development"),
    Student(2, "Mike John", "Cyber Security"),
]


# GET all students
@app.route('/students', methods=['GET'])
def fetch_students():
    all_students = []
    for student in students:
        all_students.append(student.to_dict())
    return jsonify(all_students)


# GET single student by ID
@app.route('/students/<int:id>', methods=['GET'])
def fetch_student(id):
    for student in students:
        if student.id == id:
            return jsonify(student.to_dict())
    return jsonify({"error": "Student not found"}), 404


# CREATE a new student
@app.route('/students', methods=['POST'])
def create_student():
    data = request.json

    # check if ID already exists
    for student in students:
        if student.id == data["id"]:
            return jsonify({"error": "ID already exists"}), 400

    new_student = Student(id=data["id"], name=data["name"], course=data["course"])
    students.append(new_student)
    return jsonify(new_student.to_dict()), 201


# UPDATE an existing student
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.json
    for student in students:
        if student.id == id:
            student.name = data["name"]
            student.course = data["course"]
            return jsonify(student.to_dict())
    return jsonify({"error": "Student not found"}), 404


# DELETE a student
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    for student in students:
        if student.id == id:
            students.remove(student)
            return jsonify({"message": "Student deleted"}), 200
    return jsonify({"error": "Student not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
