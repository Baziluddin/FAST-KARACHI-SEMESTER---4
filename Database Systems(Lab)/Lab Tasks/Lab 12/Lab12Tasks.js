// Q1
use SchoolDB

// Q2
db.createCollection("Students")
db.createCollection("Courses")

// Q3
db.Students.insertMany([
{
    _id: 1,
    name: "Alice",
    age: 20,
    scores: { math: 85, science: 90 }
},
{
    _id: 2,
    name: "Bob",
    age: 22,
    scores: { math: 78, science: 82 }
},
{
    _id: 3,
    name: "Charlie",
    age: 21,
    scores: { math: 92, science: 88 }
},
{
    _id: 4,
    name: "Daisy",
    age: 23,
    scores: { math: 68, science: 74 }
}
])

// Q4
db.Courses.insertMany([
{
    _id: 101,
    courseName: "Mathematics",
    instructor: "Dr. Smith",
    studentsEnrolled: [1, 2, 3]
},
{
    _id: 102,
    courseName: "Science",
    instructor: "Dr. Adams",
    studentsEnrolled: [2, 3, 4]
}
])

// Q5
db.Students.findOne({
    "scores.math": { $gte: 85 },
    age: { $lte: 22 }
})

db.Courses.findOne({
    studentsEnrolled: 3,
    instructor: "Dr. Adams"
})

// Q6
db.Students.find({
    "scores.math": { $gte: 80 },
    "scores.science": { $lt: 90 }
})

db.Students.find({
    $or: [
        { age: { $lt: 23 } },
        { "scores.math": { $gte: 85 } }
    ]
})

db.Students.find({
    "scores.science": { $gte: 80 },
    $or: [
        { "scores.math": { $lt: 75 } },
        { age: { $gt: 22 } }
    ]
})

// Q7
db.Students.updateOne(
{
    name: "Bob",
    "scores.math": { $gte: 75 }
},
{
    $inc: { "scores.science": 1 }
}
)

// Q8
db.Students.updateMany(
{
    "scores.science": { $lt: 80 },
    age: { $gt: 22 }
},
{
    $inc: { "scores.math": 5 }
}
)

// Q9
db.Students.deleteOne({
    name: "Daisy",
    "scores.science": { $lt: 80 }
})

// Q10
db.Courses.deleteMany({
    $or: [
        { studentsEnrolled: 2 },
        { instructor: "Dr. Smith" }
    ]
})

// Q11
db.Students.drop()

// Q12
db.Courses.drop()

// Q13
db.dropDatabase()
