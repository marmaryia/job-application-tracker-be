users = [{"name": "user1", "email": "user1@email.com", "password": "123456"},
         {"name": "user2", "email": "user2@email.com", "password": "123456"},
         {"name": "user3", "email": "user3@email.com", "password": "123456"}]

applications = [
    {
        "user_id": 1,
        "company": "OpenAI",
        "position": "Machine Learning Engineer",
        "status": "Application sent",
        "date_created": "2025-05-12 14:30:00",
        "job_url": "https://openai.com/careers/ml-engineer",
        "notes": "Reached out to recruiter on LinkedIn."
    },
    {
        "user_id": 2,
        "company": "Google",
        "position": "Software Engineer",
        "status": "In review",
        "date_created": "2025-05-10 09:00:00",
        "job_url": "https://careers.google.com/jobs/results/123456-software-engineer/",
        "notes": "Completed online assessment."
    },
    {
        "user_id": 3,
        "company": "Meta",
        "position": "Data Scientist",
        "status": "Rejected",
        "date_created": "2025-04-22 16:45:00",
        "job_url": None,
        "notes": "Received rejection email after final round."
    },
    {
        "user_id": 1,
        "company": "Netflix",
        "position": "Backend Engineer",
        "status": "Offer received",
        "date_created": "2025-05-18 11:00:00",
        "job_url": "https://jobs.netflix.com/positions/backend-engineer",
        "notes": "Negotiating compensation."
    },
    {
        "user_id": 2,
        "company": "Airbnb",
        "position": "Product Manager",
        "status": "Archived",
        "date_created": "2025-03-15 10:20:00",
        "job_url": None,
        "notes": None
    },
    {
        "user_id": 3,
        "company": "Stripe",
        "position": "Infrastructure Engineer",
        "status": "Offer accepted",
        "date_created": "2025-05-01 08:30:00",
        "job_url": "https://stripe.com/jobs/infrastructure",
        "notes": "Start date set for July 1st."
    },
    {
        "user_id": 1,
        "company": "LinkedIn",
        "position": "Frontend Engineer",
        "status": "In review",
        "date_created": "2025-05-25 14:15:00",
        "job_url": None,
        "notes": "Waiting to hear back after phone interview."
    },
    {
        "user_id": 2,
        "company": "Twitter",
        "position": "DevOps Engineer",
        "status": "Offer declined",
        "date_created": "2025-05-05 09:30:00",
        "job_url": "https://careers.twitter.com/positions/devops-engineer",
        "notes": "Declined due to better offer."
    },
    {
        "user_id": 3,
        "company": "Salesforce",
        "position": "QA Engineer",
        "status": "Application sent",
        "date_created": "2025-06-01 13:50:00",
        "job_url": None,
        "notes": "Submitted application via company portal."
    },
    {
        "user_id": 1,
        "company": "Dropbox",
        "position": "Site Reliability Engineer",
        "status": "Rejected",
        "date_created": "2025-04-29 10:00:00",
        "job_url": "https://jobs.dropbox.com/sre",
        "notes": None
    }
]

events = [
    {
        "user_id": 1,
        "application_id": 1,
        "title": "Initial Resume Sent",
        "date": "2025-05-10 09:00:00",
        "notes": "Sent resume through company portal."
    },
    {
        "user_id": 1,
        "application_id": 1,
        "title": "Phone Interview Scheduled",
        "date": "2025-05-12 15:00:00",
        "notes": "Scheduled via recruiter email."
    },
    {
        "user_id": 2,
        "application_id": 2,
        "title": "Online Assessment Completed",
        "date": "2025-05-11 10:30:00",
        "notes": "Completed coding assessment in HackerRank."
    },
    {
        "user_id": 2,
        "application_id": 2,
        "title": "Recruiter Follow-Up",
        "date": "2025-05-13 14:45:00",
        "notes": "Recruiter asked for availability for next week."
    },
    {
        "user_id": 1,
        "application_id": 4,
        "title": "Onsite Interview",
        "date": "2025-05-19 09:00:00",
        "notes": "Full day onsite with 4 interviewers."
    },
    {
        "user_id": 1,
        "application_id": 4,
        "title": "Offer Discussion",
        "date": "2025-05-20 17:00:00",
        "notes": "Discussed initial offer details with HR."
    },
    {
        "user_id": 2,
        "application_id": 5,
        "title": "Application Archived",
        "date": "2025-03-20 10:00:00",
        "notes": "User decided to pause the application."
    },
    {
        "user_id": 2,
        "application_id": 5,
        "title": "Company Newsletter Signup",
        "date": "2025-03-22 11:15:00",
        "notes": "Signed up for product updates to stay informed."
    },
    {
        "user_id": 1,
        "application_id": 7,
        "title": "Phone Screen",
        "date": "2025-05-26 13:00:00",
        "notes": "Spoke with engineering manager."
    },
    {
        "user_id": 1,
        "application_id": 7,
        "title": "Feedback Received",
        "date": "2025-05-27 16:00:00",
        "notes": "Positive feedback. Moving to next round."
    },
    {
        "user_id": 2,
        "application_id": 8,
        "title": "Offer Made",
        "date": "2025-05-06 10:30:00",
        "notes": "Received offer via email."
    },
    {
        "user_id": 2,
        "application_id": 8,
        "title": "Offer Declined",
        "date": "2025-05-07 14:00:00",
        "notes": "Politely declined due to better opportunity."
    },
    {
        "user_id": 1,
        "application_id": 10,
        "title": "Interview Scheduled",
        "date": "2025-04-25 11:00:00",
        "notes": "Scheduled for April 29."
    },
    {
        "user_id": 1,
        "application_id": 10,
        "title": "Rejection Email",
        "date": "2025-04-30 09:00:00",
        "notes": "Received generic rejection email."
    },
    {
        "user_id": 1,
        "application_id": 1,
        "title": "Follow-Up Email Sent",
        "date": "2025-05-14 08:30:00",
        "notes": "Thanked interviewer and asked for update."
    },
    {
        "user_id": 2,
        "application_id": 2,
        "title": "Technical Interview",
        "date": "2025-05-15 13:30:00",
        "notes": "Live coding and system design."
    },
    {
        "user_id": 2,
        "application_id": 5,
        "title": "Informational Interview",
        "date": "2025-03-18 15:00:00",
        "notes": "Talked with former employee about role."
    },
    {
        "user_id": 1,
        "application_id": 7,
        "title": "Team Interview",
        "date": "2025-05-28 09:30:00",
        "notes": "Spoke with 2 engineers and 1 designer."
    },
    {
        "user_id": 2,
        "application_id": 8,
        "title": "Compensation Negotiation",
        "date": "2025-05-06 16:00:00",
        "notes": "Requested equity adjustment."
    },
    {
        "user_id": 1,
        "application_id": 10,
        "title": "Interview Prep",
        "date": "2025-04-24 12:00:00",
        "notes": "Reviewed system design and behavior questions."
    }
]