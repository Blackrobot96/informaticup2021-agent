# AlphaBetaAgent

Contains: Alpha Beta Agent Game-Structure GameState-Structure Astar algorithm
Note: requirements from requirements.txt must be installed

## Docker image ready to go
Run `docker run -v ${PWD}:/app/logs -it -e "URL=<URL>" -e "KEY=<API_KEY>" --rm robertkerzel/informaticup2021-agent`. If you dont care about the json logfile you can leave `-v ${PWD}:/app/logs` out of the command. Replace `<URL>` and `<API_KEY>` with the right values.

## Docker image build & push
To build the container run `docker build --tag robertkerzel/informaticup2021-agent .` and push it to dockerhub `docker push robertkerzel/informaticup2021-agent`. 