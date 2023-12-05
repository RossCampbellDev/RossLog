The RossLog is a simple application to allow me to do daily logs in the style of a Star Trek captain.

### Components
- web service (Python/Flask)
    - RESTful
    - read, write logs
    - filter what we retrieve
    - make into docker container

- simple web interface for read/write.  runs parallel to web service (same docker ctr?)

- cmd line tool for writing/retrieval (Python -> PE?)
    - CLI handles hashing of API key/password before making request
    
- authenticate to service with API Key?

### DB
- LogEntry
    - datestamp,title,body,tags

### web front end
- log in screen
- home screen
    - list of dates (defaults to last week?)
        - can click on a day to see all entries for that day?
    - filter list
    - write new entry

### Docker
remember to add the env vars such as FLASK APP