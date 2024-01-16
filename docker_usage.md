# Run app using docker

Kindly visit this [link](https://docs.docker.com/engine/install/) to install docker engine on your machine.
Also install docker-compose plugin from this [link](https://docs.docker.com/compose/install/)

### 1. Manually create the image and run the container

1. Create a docker image by running below command in project root directory
```bash
docker image build -t {your_image_name} .
```

2. Run the container using,
```bash
docker run -p 7755:7755 -d {your_image_name}
```



### 2. Using docker-compose.yml
With docker-compose we don't need to remember very long commands to build or run containers, making it easier to run applications. You can build and start the container using,
```bash
docker-compose up
```
<br/>
In both cases you can access the application on <a>http://localhost:7755</a>
<br/>

##### Populate `.dockerignore` with almost same content from `.gitignore` to keep the image lightweight.

##### You can also publish your docker image and share it. Refer [link](https://docs.docker.com/get-started/04_sharing_app/)
