# API

- `POST /api/auth/login` \
  Accepts requests with "email" and "password". \
  Example response:

```
 {
	"access_token": "some_string",
	"user": {
		"email": "user1@email.com",
		"id": 1,
		"name": "user1"
	}
}
```

- `POST /api/auth/login` \
  Accepts requests with "name", "email" and "password". \
  Example response:

```
{
	"user": {
		"email": "best_emaidfsl53@email.com",
		"id": 8,
		"name": "ABC"
	}
}
```

- `DELETE /api/auth/logout`
  Adds authentication token to blocklist \
  Authentication token required \
  Example response:

```
{
	"message": "Logged out successfully"
}
```

- `GET /api/users/:user_id/applications` \
  Accepts query parameters:
  order (asc or desc), sort_by (date_created, recent_activity), status (active, rejected, archived)\
  Authentication token required \
   Example response:

```
{
	"applications": [
		{
			"application_id": 7,
			"company": "LinkedIn",
			"date_created": "2025-05-25T14:15:00",
			"job_url": null,
			"latest_event": {
				"date": "2025-05-28T09:30:00",
				"event_id": 18,
				"title": "Team Interview"
			},
			"position": "Frontend Engineer",
			"status": "In review"
		},
    ]
}
```

- `PATCH /api/applications/:application_id` \
  Request body:
  {new_status: "valid status"}\
  Authentication token required \
   Example response:

```
{
	"application": {
		"application_id": 1,
		"company": "OpenAI",
		"date_created": "2025-05-12T14:30:00",
		"events": [
			{
				"date": "2025-06-23T14:15:41",
				"event_id": 27,
				"notes": null,
				"title": "Status change to Rejected"
			},

			{
				"date": "2025-05-10T09:00:00",
				"event_id": 1,
				"notes": "Sent resume through company portal.",
				"title": "Initial Resume Sent"
			}
		],
		"job_url": "https://openai.com/careers/ml-engineer",
		"notes": "Reached out to recruiter on LinkedIn.",
		"position": "Machine Learning Engineer",
		"status": "Rejected",
		"user_id": 1
	}
}
```

- `POST /api/applications` \
   Request body params: user_id, company, position, status, *job_url, *notes, *date_created, *allow_duplicates

  If date_created is not provided, it defaults to the current timestamp

  If the given user already has an application with the job_url provided, the request will return error, listing applications with the same url, unkess "allow_duplicates" is set to "true".

  Authentication token required

  Example response:

```
{
	"application": {
		"application_id": 36,
		"company": "ABC Company",
		"date_created": "2025-06-25T14:31:32",
		"events": [
			{
				"date": "2025-06-25T14:31:32",
				"event_id": 51,
				"notes": null,
				"title": "Application created"
			}
		],
		"job_url": "www.google.com",
		"notes": "Some notes",
		"position": "Tester",
		"status": "Rejected",
		"user_id": 1
	}
}
```

- `DELETE /api/applications/:application_id` \
   Authentication token required

  No reponse

- `GET /api/applications/:application_id` \
   Authentication token required

  Example response:

  ```
  {
  	"application": {
  		"application_id": 4,
  		"company": "ABC Company",
  		"date_created": "2025-05-18T11:00:00",
  		"events": [

  			{
  				"date": "2025-05-19T09:00:00",
  				"event_id": 5,
  				"notes": "Full day onsite with 4 interviewers.",
  				"title": "Onsite Interview"
  			}
  		],
  		"job_url": "https://jobs.netflix.com/positions/backend-engineer",
  		"notes": "Negotiating compensation.",
  		"position": "Backend Engineer",
  		"status": "Offer received",
  		"user_id": 1
  	}
  }
  ```
