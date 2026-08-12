-- 2026-07-29

installed docker CE on fedora 44

Learned
- images are rules for containers and are read-only
- containers have writable layers, to store container specific files and information(will delete when container deleted)
- docker ps only shows running containers
- docker ps -a shows all containers
- exit code 127 usually indicates a command couldnt be executed
- port publishing maps a host to the container port( -p 8080:80 HOST_PORT:CONTAINER_PORT)
- docker inspect tells you everything about  a container

mistakes: 
- put docker options after image name. docker options must be before image name

-- 2026-07-30

Used docker compose to create and launch an nginx container

Learned 
- compose.yaml syntax,
- learned docker compose commands


mistakes: 
- struggled to name container
- messed up syntax for name
- forgot restart policy
- put ports in without quotes


Learned to mount volumes and how persistent data work

Learned:s
- learned the command for mounting volumes and its syntax (-v plex-data:targetdir)
- learned about the --rm option for docker run command
- learned how commands work for docker arguments and where to position them in the command
- learned about docker volume ls, docker volume inspect
- learned anonymous volumes
- learned how to prune containers(deletes all closed containers)

mistakes:
- incorrectly inputted command causing docker to not know wherei was telling it to go
- attempted to write the txt file from fedora shell  instead  of from the container
- forgot --rm option and created many containers

Set up samba server for file sharing

Learned: 
- permissions required for file systems
- more docker compose, used it to start the samba server and to set port etc
- how to configure samba server

mistakes
- many typos
- permission issues

2026-08-02

Set up plex server

 Learned:
- group permissions and file permissions
- learned more about compose syntax

mistakes:
- used wrong image at first
- spelling errors
