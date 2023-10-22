### Local Development


#### Configuring the Environment

If docker directory doesn't contain environment files you can copy it manually from ```env.examples``` directory:
```bash
$ cp envs.example/app.env docker/app/.env
$ mkdir docker/db/ && cp envs.example/db.env docker/db/.env
```

#### Run the Stack
This brings up all services together. The first time it is run it might take a while to get started, but subsequent runs will occur quickly.

Open a terminal at the project root and run the following for local development
```bash
$ docker-compose -f local.yml up --build
```
This command starts the containers in the background and leaves them running.

In case you want to aggregate the output of each container use following command
```bash
$ docker-compose -f local.yml up
```

#### Stop the Stack
To stop, just
```bash
$ docker-compose -f local.yml stop
```

#### Start the Stack
To start the stack in case containers are existing use this command
```bash
$ docker-compose -f local.yml start
```

#### Destroy the Stack
To stop containers and remove containers and networks
```bash
$ docker-compose -f local.yml down
```
To stop containers and remove containers, networks and local images
```bash
$ docker-compose -f local.yml down --rmi local
```  
To stop containers and remove containers, networks, local images and volumes:
```bash
$ docker-compose -f local.yml down --rmi local -v
```
More information: https://docs.docker.com/compose/reference/down/


