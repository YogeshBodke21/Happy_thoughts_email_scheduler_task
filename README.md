#1. POST Method -- http://localhost:8000/schedule_task
   body --->
    {
  "sent_to": "ybodke123@gmail.com",
  "subject": "Hello from Django",
  "message": "This is a test scheduled email.",
  "sent_at": "2026-03-27T13:30:00+05:30"
}


#2. POST Method --->
   http://localhost:8000/reschedule_task/id
   body -- > {
     "sent_at": "2026-03-27T13:60:00+05:30"
    }

   
