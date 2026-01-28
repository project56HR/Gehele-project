# RemoteFrontend Project56
---

The remote front-end for Project 5/6. This front-end is a live monitor for the Windgenerator for Project 5/6.

---
## Features
- Connects to a python websockets and displays live data
- Connects to the windgenerators database to display stats over a longer time

## Requirements
- Docker

## Install instructions
- Pull the repository
```bash
git clone https://github.com/project56HR/remoteFrontend.git
```

- Build the docker container
```bash
docker build -t ui-project56 .
```

- Run the docker container, exposing port 3000
```bash
docker run -name ui-project56 -p 3000:3000 ui-project56
```