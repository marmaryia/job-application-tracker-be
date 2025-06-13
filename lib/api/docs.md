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

- `GET /api/users/:user_id/applications` \
  Accepts query parameters:
  order (asc or desc), sort_by (date_created, recent_activity), status (active, rejected, archived)\
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
