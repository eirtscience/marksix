
<div align="center" style="">

  <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQIE1D67CNstDLqGPwAPiz6mo6RPeOsG9gEsGAwkQB0-mrfzx2z&s"><br><br>
</div>

# `Marksix-Deployment`

This document highligth the manual or automatic deployment and installation of the marksix applications. The user of this guide should be familiar with the Linux environment,have basic understanding of Python, git, docker. 


## `Structure of the Project`
The Marksix project is comprised with 3 type of applications, the betting server, web server, chat application:

  - `Betting server`:
     It is Standalone python application that handle any marksix betting data. 8080.


  - `Web server`:
    - `blackcreek-admin_service`        : It is Django application for the admin web portal usualy running on the port 8080.
    - `blackcreek-data_provider_client` : It is Django application for the DP or DC web portal usualy running on the port 8081.

  - `Chat application`:
    - `blackcreek-mobile_collection_tool` : It is Flutter application for the surveyor to collect estate data.
     


## `Requirement`

- `Environment`
  - `Operating System` : GNU/Linux Ubuntu 18.04
  - `CPU`              : 4 core 3693 MHz
  - `Memory`           : 10GB or more

- `Software packages`

  | **Packages** | **Version** |
  |:-------------|:--------------------------------|
  | docker       | 18.09.7                         |
  | docker-compose   | 1.24.1                    |
  | python   | 3.6.9             |
  | git      | 2.17.1 |




## `Installation Guide`

sudo curl -L "https://raw.githubusercontent.com/eirtdev/shell/master/marksix" -o /usr/local/bin/marksix

sudo chmod +x /usr/local/bin/marksix

- `Preparing the environment`

  - `Install all the require packages`

    - `Install docker`
        ```sh
        ~$ sudo apt-get install docker.io
        ```

    - `Install docker-compose`
        ```sh
        ~$ sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        ```
        Make the `docker-compose` file executable

        ```sh
        ~$ sudo chmod +x /usr/local/bin/docker-compose
        ```
    - `Install Pyyaml`

        Before proceeding to install the pyyaml package, make sure you have the  `pip3` installed in your local environment.


        - `Install pip3 when not installed`

            In case pip3 is not installed use the below command to install it. 

            ```sh
            ~$ sudo apt-get install -y python3-pip
            ```
              

        ```sh
        ~$  pip3 install pyyaml
        ```

    - `Checking the pre-requisite packages installation`
      
        ```sh
        ~$ python --version
        Python 3.6.9
        ```

        ```sh
        ~$ docker --version
        Docker version 19.03.6, build 369ce74a3c
        ```

        ```sh
        ~$ docker-compose --version

        docker-compose version 1.24.1, build 4667896b
        ```

        ```sh
        ~$ git --version
        git version 2.17.1
        ```


  - `Create a project directory`

      Create a directory called project on your home directory as showing below

      ```sh
      ~$ mkdir project && cd project
      ```

  - `Clone all the repositories`

      Clone all the applications bitbucket repositories.

      ```sh
      ~/project$ sudo git clone https://evaristblackcreek@bitbucket.org/blackcreek_tech/blackcreek-admin_service.git

      ```

      ```sh
      ~/project$ sudo git clone https://evaristblackcreek@bitbucket.org/blackcreek_tech/blackcreek-api.git
      ```

      ```sh
      ~/project$ sudo git clone https://evaristblackcreek@bitbucket.org/blackcreek_tech/blackcreek-blockchain.git
      ```

      ```sh
      ~/project$ sudo git clone https://evaristblackcreek@bitbucket.org/blackcreek_tech/blackcreek-chaincode.git
      ```

      ```sh
      ~/project$ sudo git clone https://evaristblackcreek@bitbucket.org/blackcreek_tech/blackcreek-compose.git
      ```

      ```sh
      ~/project$ sudo git clone https://evaristblackcreek@bitbucket.org/blackcreek_tech/blackcreek-data_provider_client.git
      ```

      ```sh
      ~/project$ sudo git clone https://evaristblackcreek@bitbucket.org/blackcreek_tech/blackcreek-email_service.git
      ```

      ```sh
      ~/project$ sudo git clone https://evaristblackcreek@bitbucket.org/blackcreek_tech/blackcreek-shell.git
      ```

      ```sh
      ~/project$ sudo git clone https://evaristblackcreek@bitbucket.org/blackcreek_tech/env.git
      ```

      ```sh
      ~/project$ sudo git clone https://evaristblackcreek@bitbucket.org/blackcreek_tech/blackcreek-standalone.git
      ```
    
   - `Switting to the latest branch`

        The below cloning demonstration involve the latest branch push to the repo. At this stage the latest branch name is `blockchain`.
        If everything is ok, let change the below repo to the `blockchain` branch.

      - `Load the latest admin-service branch`
        ```sh
        ~/project$ cd blackcreek-admin_service/ && sudo git fetch origin blockchain && sudo git checkout blockchain
        ```

      - `Load the latest blackcreek-api branch`
        ```sh
        ~/project$ cd blackcreek-api/ && sudo git fetch origin blockchain && sudo git checkout blockchain
        ```

      - `Load the latest blackcreek-compose branch`
        ```sh
        ~/project$ cd blackcreek-compose/ && sudo git fetch origin blockchain && sudo git checkout blockchain
        ```

      - `Load the latest blackcreek-data_provider_client branch`
        ```sh
        ~/project$  cd blackcreek-data_provider_client/ && sudo git fetch origin blockchain && sudo git checkout blockchain
        ```

      - `Load the latest blackcreek-email_service branch`
        ```sh
        ~/project$ cd blackcreek-email_service/ && sudo git fetch origin blockchain && sudo git checkout blockchain
        ```

    - `Changing the project directory ownership`

        Change the ownership of the project directory.

        ```sh
        ~/project$ sudo chown -R `whoami`:`whoami` .
        ```

    - `Creating the Environment variable`
        
        Create the below environment variable.

        `BLACKCREEK_ENV`:
          Use to identify which mode, all the blackcreek application are running in.

        `DOCKER_CLIENT_TIMEOUT`:
          Allow the docker executable client to wait for the specify time before cancelling the connexin to the docker server, the time is specify in milli-seconds.

        `COMPOSE_HTTP_TIMEOUT`:
          Same as `DOCKER_CLIENT_TIMEOUT`, but it is apply to a `docker-compose`.
        
        `FABRIC_PATH`:
          Allow allow the automaci tools to know the location of the HF(Hyperldger Fabric) for different raisons.


        ```sh
        ~/project$ export BLACKCREEK_ENV="SIT"
        ~/project$ export DOCKER_CLIENT_TIMEOUT=1000
        ~/project$ export COMPOSE_HTTP_TIMEOUT=1000
        ~/project$ export FABRIC_PATH=$PWD/blackcreek-blockchain/hyperledger-fabric
        ```

    - `Deploying docker container`

        At this stage I assume that there is no issue with above installation and everything went well. If so we will start deploying the application into our docker container. There is two ways to perform the deployment, use individual deployment or bulk deployment. If you are new to docker deployment I encourage you to do the individual deployment otherwise use the bulk deployment. One problem about bulk deployment is that, when one service fail to be deploy is not easy to locate it. 


      - `List of services in compose file`

        | **Service Name** | **Location** |
        |:-------------|:--------------------------------|
        | user-api     | ~project/blackcreek-api/blackcreek-api_service_new/ui_service/ |
        | admin-api    |  ~project/blackcreek-api/blackcreek-api_service_new/admin_service/ |
        | email-service    |  ~project/blackcreek-email_service/ |
        | data_collection_tool_api | ~project/blackcreek-api/blackcreek-api_service_new/data_collection_service/ |
        | elastic-api  | ~project/blackcreek-api/blackcreek-api_service_new/elastic_service/ |
        | admin-service | ~project/blackcreek-admin_service/ |
        | user-service  | ~project/blackcreek-data_provider_client/ |
        | celery_email_server | ~project/blackcreek-email_service/ |
        | admin_db  | --- |
        | user_db |  --- |
        | blockchain_gateway | ~project/blackcreek-api/blackcreek-api_service_new/celery_service/ | 
        | celery_beat  | --- |
        | blockchain_network_service  | ~project/blackcreek-api/blackcreek-api_service_new/blockchain_network_service/ |
        | elastic-server    | --- |
        | schedule_server | ~project/blackcreek-standalone/ |
        | xci | ~project/env/xci/xci/ |



      - `Individual service deployment`

          We will be deploying each service manually and monitor the deployment.

          - `Deploy user-api service`

              The user service is the heart of the platform, because it performs a lot of actions. The various function perform by this service is as follow, it perform the CRUD(Create Read Update Delete) operations against the `user_db` service/container.

              ```sh
              ~/project$ sudo docker-compose -f blackcreek-compose/docker-compose.yml up -d --build user-api
              ```

          - `Deploy admin-api service`

              The main operation perform by this service, is to handle CRUD operation against the `admin_db` database and a conextion to other service such the email, user services and others. 
             
              ```sh
              ~/project$ sudo docker-compose -f blackcreek-compose/docker-compose.yml up -d --build admin-api
              ```

          - `Deploy email-service service`

              This service is responsible to asynchronously send an email to the request email address send by any service.

              ```sh
              ~/project$ sudo docker-compose -f blackcreek-compose/docker-compose.yml up -d --build email-service
              ```

          - `Deploy data_collection_tool_api service`

              This service , is to use by the DP surveyor data collection's mobile application , to 

              ```sh
              ~/project$ sudo docker-compose -f blackcreek-compose/docker-compose.yml up -d --build data_collection_tool_api
              ```
          
          - `Deploy elastic-api service`

              A gateway application that communicate with the elastic-server.

              ```sh
              ~/project$ sudo docker-compose -f blackcreek-compose/docker-compose.yml up -d --build elastic-api
              ```

          - `Deploy admin-service service`

              Represents the admin portal for the admin management.

              ```sh
              ~/project$ sudo docker-compose -f blackcreek-compose/docker-compose.yml up -d --build admin-service
              ```

          - `Deploy user-service service`

               This represent the DP and DC web portal for data and user managment.

              ```sh
              ~/project$ sudo docker-compose -f blackcreek-compose/docker-compose.yml up -d --build user-service
              ```

          - `Deploy celery_email_server service`
            ```sh
            ~/project$ sudo docker-compose -f blackcreek-compose/docker-compose.yml up -d --build celery_email_server
            ```

          - `Deploy admin_db service`

             Store all information related to the admin web portal.

            ```sh
            ~/project$ sudo docker-compose -f blackcreek-compose/docker-compose.yml up -d --build admin_db
            ```

          - `Deploy user_db service`

              Store informations related to the user data.

            ```sh
            ~/project$ sudo docker-compose -f blackcreek-compose/docker-compose.yml up -d --build user_db
            ```

          - `Deploy blockchain_gateway service`

              Asynchronous gateway to send request to the blockchain Node application.

              ```sh
              ~/project$ sudo docker-compose -f blackcreek-compose/docker-compose.yml up -d --build blockchain_gateway
              ```

          - `Deploy celery_beat service`
            ```sh
            ~/project$ sudo docker-compose -f blackcreek-compose/docker-compose.yml up -d --build celery_beat
            ```
                  
          - `Deploy blockchain_network_service service`

              NodeJs application gateway to communicate with Hyperledger Fabric network.

              ```sh
              ~/project$ sudo docker-compose -f blackcreek-compose/docker-compose.yml up -d --build blockchain_network_service
              ```

          - `Deploy elastic-server service`

            ```sh
            ~/project$ sudo docker-compose -f blackcreek-compose/docker-compose.yml up -d --build elastic-server
            ```

          - `Deploy schedule_server service`

              Standalone time server acting like Linux Cron command

            ```sh
            ~/project$ sudo docker-compose -f blackcreek-compose/docker-compose.yml up -d --build schedule_server
            ```

          - `Deploy xci service`

              CI server to implements the continus integration.

              ```sh
              ~/project$ sudo docker-compose -f blackcreek-compose/docker-compose.yml up -d --build xci
              ```
            
      - `Bulk service deployment`

          Deploying each service manually take time, however `docker-compose` provide a short command to deploy all the service once.

          ```sh
          ~/project$ sudo docker-compose -f blackcreek-compose/docker-compose.yml up --build 
          ```

      - `Run blockchain network`

          To bring the blockchain, there is one shell script that was created to help briging the network up called `network`.
          This shell script is located in the blackcreek-blockchain directory on the project root folder.
          Go to the blackcreek-blockchain directory.

          To run the blockchain network make sure all the services are up and running by running the below command

          ```sh
          ~/project$ sudo docker-compose -f docker-compose.yml ps

                              Name                         Command               State                    Ports                 
          -------------------------------------------------------------------------------------------------------------
          admin-api                    ./start                          Up      8000/tcp                               
          admin-website                python manage.py runserver ...   Up      0.0.0.0:8080->8000/tcp                 
          admin_db                     docker-entrypoint.sh mongo ...   Up      27017/tcp                              
          blockchain_gateway           ./start                          Up      0.0.0.0:8000->8000/tcp                 
          blockchain_network_service   docker-entrypoint.sh npm r ...   Up      0.0.0.0:8088->8000/tcp                 
          celery-email-server          /bin/sh -c celery -A email ...   Up                                             
          celery_beat                  sh -c python manage.py mak ...   Up      8000/tcp                               
          celery_worker                sh -c python manage.py mak ...   Up      8000/tcp                               
          ci-server                    python manage.py runserver ...   Up      0.0.0.0:7000->8000/tcp                 
          elastic-api                  ./start                          Up      0.0.0.0:8086->8000/tcp                 
          elastic-server               /usr/local/bin/docker-entr ...   Up      0.0.0.0:9200->9200/tcp, 9300/tcp       
          email-api                    python manage.py runserver ...   Up      8000/tcp                               
          mobile-collection-tool-api   ./start                          Up      0.0.0.0:8085->8000/tcp                 
          rabbit                       docker-entrypoint.sh rabbi ...   Up      25672/tcp, 4369/tcp, 5671/tcp, 5672/tcp
          rabbit_worker                docker-entrypoint.sh rabbi ...   Up      25672/tcp, 4369/tcp, 5671/tcp, 5672/tcp
          schedule_server              sh start.sh                      Up                                             
          user-api                     ./start                          Up      8000/tcp                               
          user-website                 python manage.py runserver ...   Up      0.0.0.0:8081->8000/tcp                 
          user_db                      docker-entrypoint.sh mongo ...   Up      27017/tcp 
          ```
          Once your command display the above output, you are good to run the blockchain network.

          ```sh
          ~/project$ cd blackcreek-blockchain/
          ```

          Once you are in that directory, run the below script.

          ```sh
          ~/project/blackcreek-blockchain$ sudo ./network up -a -y 
          ```


      - `Login into a service`

         There will be a time you will have an issue or want to get some information about some service and you have to login into the service
         to perform some action.
         Let say you would like to login into a service called `admin-api`
         
         - `Login using docker command`

            ```sh
            ~$ docker exec -it admin-api /bin/bash
            ```
         - `Login using the blackcreek shell script`

            To login into the  `admin-api` you have to position yourself in the `blackcreek-shell` directory 

            ```sh
            ~/project/blackcreek-shell$ ./blackcreek service admin-api login
            ```

      - `Apply Django migration`

        Apply Django migrations to all the containers running django framework
          
          ```sh
          $ python manage.py makemigrations

          $ python manage.py migrate
          ```

      - `Note`

          To check if a container/service is running , you must run the below command. 

          ```sh
          ~/project$ sudo docker-compose -f docker-compose.yml ps
          ```
          In the output , look at the column `State` to identify the `Up` for running or `Exit` for not running.

      - `Error Handling`
          
          - `COPY LOCALIZATION DIRECTORY FROM REPO TO APPLICATION`

            Make sure to copy all the localization integration from their respective bitbucket repo into the container locale folder.

            Implement this in the DockerFile
            Remove the docker-compose volumes mounting implementation for all the localization.


          - `INCREASE MEMORY FOR ESLASTIC-SERVER CONTAINER`
          
          Sometime , the elastic server service will failed to start so, make sure to increase your environment memory.
          - Increase the eslatic-server container service

            ```sh
            $ ./blackcreek elastic inc_mem
            ```
            The above script will be run from the blackcreek-shell folder


          - `CLONE LOCALIZATION REPO FOR EACH SERVICE`

             Clone localization repo. Make sure to clone each localization repo into respective docker container folder


          - `Blockchain gateway issue`

            - `Nodejs grpc package issue`
            
            ```sh
            cd node_modules/grpc/src/ && npm --unsafe-perm install
            ```

              ```sh
              cd node_modules/fabric-client/node_modules/grpc/src/ && npm --unsafe-perm install
              ```
      
              There is an issue
              The file can be seen in the below folder
              /home/node/app/node_modules/fabric-client/node_modules/grpc/src/node/extension_binary/node-v64-linux-x64-musl/grpc_node.node(OK available)

              The file cannot be seen in the below file
              /home/node/app/node_modules/fabric-network/node_modules/grpc/src/node/extension_binary/node-v64-linux-x64-musl/grpc_node.node(NOT OK not avaible)

            - `Solution`

              * Run the container without starting the nodejs server. which means that comment this line "CMD ["npm", "run", "prod"]".
              * Login into the container.
              * Go to the following directory "/home/node/app/node_modules/fabric-network/node_modules"
              * Run the following script.

              ```sh
              mv grpc/ grpc_old
              ln -s /home/node/app/node_modules/fabric-client/node_modules/grpc grpc
              cd /home/node/app/
              npm run prod
              ```
          


