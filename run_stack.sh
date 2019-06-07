docker build -t rs_server RS/.

docker build -t p0_server P0/.

docker run -itd --name rs_run rs python3 /RS.py

docker run -itd --name p0_run p0 python3 /P0.py

docker run -itd --name p0_run1 p0 python3 /P0.py

docker exec -it p0_run python3 /imports/client.py
