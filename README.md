The RossLog is a simple application to allow me to do daily logs in the style of a Star Trek captain.

### Components
- web service (Python/Flask)
    - RESTful
    - read, write logs
    - filter what we retrieve
    - make into docker container

- simple web interface for read/write.  runs parallel to web service

- cmd line tool for writing/retrieval (Python -> PE?)
    
- authenticate to service (API Key?)