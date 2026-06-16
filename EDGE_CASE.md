# Edge Case

For `POST /students`, the primer says that `mark` is optional, but it does not specify what should happen when `mark` is not provided.

I chose to set the student's mark to `0` when `mark` is missing. This keeps every student record consistent because each student still has an integer mark in the database.

For `GET /stats`, if there are no students in the database, I return:

```json
{
  "count": 0,
  "average": null,
  "min": null,
  "max": null
}