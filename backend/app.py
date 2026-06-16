from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this


@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    students = db.get_all_students()
    return jsonify(students), 200


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """
    student_data = request.json

    if student_data is None:
        return jsonify({"error": "Missing request body"}), 404

    name = student_data.get("name")
    course = student_data.get("course")
    mark = student_data.get("mark", 0)

    if name is None or name == "":
        return jsonify({"error": "Missing student name"}), 404

    if course is None or course == "":
        return jsonify({"error": "Missing course"}), 404

    try:
        mark = int(mark)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid mark"}), 404

    created_student = db.insert_student(name, course, mark)
    return jsonify(created_student), 200


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    student_data = request.json

    if student_data is None:
        return jsonify({"error": "Missing request body"}), 404

    name = student_data.get("name")
    course = student_data.get("course")
    mark = student_data.get("mark")

    if mark is not None:
        try:
            mark = int(mark)
        except (TypeError, ValueError):
            return jsonify({"error": "Invalid mark"}), 404

    updated_student = db.update_student(student_id, name, course, mark)

    if updated_student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(updated_student), 200


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    deleted_student = db.delete_student(student_id)

    if deleted_student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(deleted_student), 200


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    students = db.get_all_students()
    marks = [student["mark"] for student in students]

    if len(marks) == 0:
        return jsonify({
            "count": 0,
            "average": None,
            "min": None,
            "max": None
        }), 200

    return jsonify({
        "count": len(marks),
        "average": sum(marks) / len(marks),
        "min": min(marks),
        "max": max(marks)
    }), 200


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)