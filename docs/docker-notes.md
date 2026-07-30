--docker is a service to create containerized applications

--An image is the rules or a template for the container

--a container is similar to a vm however it uses the host machines kernel to run
and isolates the applications hosted within

--a volume is a persistent data storage medium that docker manages, they remain
independent of the container it is stored on the docker host

--a bind mount is a way to mount a specific file or directory from host machine
into a container.

--docker options must come before image name
--exit code of 127 often indicates command not found
--docker exec executes a program inside the container (e.g docker exec -it name \
/bin/bash)
-- docker inspect tells you EVERYTHING ABOUT A CONTAINER



-- docker compose reads a compose.yaml file to launch and run a container
-- you specify your rules names etc from the compose.yaml file
-- restart policies are rules for when the container should and shouldnt restart
-- bind mounts tell the container where to look for files and information
-- volumes are docker controlled persistent storage you mount them to a container using -v volumename:desiredcontainerfile
