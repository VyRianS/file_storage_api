# File Storage API

## Architecture
This project is a simple attempt to create a file storage system that is docker-portable with the following features:
  1. Add files via POST
  2. Add or modify files via PUT
  3. Retrieve file contents via GET
  4. Delete files via DELETE

- Developed on CentOS7 3.10 (released 2018-11-29).
- Core logic in `api.py` is written in Python3.6 and invokes the `Flask` module.
- Only accepts files with .txt, .json, or .xml extensions.
- Files uploaded are stored on the container's working directory in folders `_storage` and `_temp`.
- Running container exposes and maps port 5000 for external requests.

## Build
Clone this repository into the desired directory.
```
$ git clone https://github.com/VyRianS/file_storage_api/
```

Ensure that `docker` is installed and service is running.
```
$ sudo systemctl status docker
```

Check that there are no other processes listening on port 5000. The following command _should not return any set_.
```
$ netstat -antu | grep ":5000 " | grep "LISTEN"
```

To build, change directory to the file_storage_api directory where it was cloned/pulled, and run the following commands.
```
$ cd file_storage_api
$ docker build -t file_storage_api .
$ docker run -it -p 5000:5000/tcp file_storage_api
```

Flask server should immediately begin to run and accept external requests. 

## API Interactions

### POST 
**Objective**: Uploads a named file.<br />
**URL**:       `http://127.0.0.1:5000/upload`<br />
**Example**:   `curl -X POST -F "file=@textfile.txt" http://127.0.0.1:5000/upload`<br />
**Outcomes**:<br />
- `200` `File uploaded.`
- `400` `Empty filename.`
- `400` `Unrecognized file format.`
- `400` `Duplicate filename in storage.`

### PUT
**Objective**: Modifies an existing file or uploads if file is not found. No action done if file hash is the same.<br />
**URL**:       `http://127.0.0.1:5000/upload`<br />
**Example**:   `curl -X PUT -F "file=@textfile.txt" http://127.0.0.1:5000/upload`<br />
**Outcomes**:<br />
- `200` `File uploaded.`
- `200` `File updated.`
- `200` `No difference between file being uploaded and existing file.`
- `400` `File does not exist.`

### GET
**Objective**: Retrieves contents of named file.<br />
**URL**:       `http://127.0.0.1:5000/<filename>`<br />
**Example**:   `curl -X GET http://127.0.0.1:5000/textfile.txt`<br />
**Outcomes**:<br />
- `200` `<file_contents>`
- `400` `File does not exist.`

### DELETE
**Objective**: Deletes named file.<br />
**URL**:       `http://127.0.0.1:5000/<filename>`<br />
**Example**:   `curl -X DELETE http://127.0.0.1:5000/textfile.txt`<br />
**Outcomes**:<br />
- `200` `File deleted.`
