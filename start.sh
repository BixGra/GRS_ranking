echo "docker build . -t grsapi"

docker build . -t grsapi

echo "docker compose up -d --remove-orphans"

docker compose up -d --remove-orphans

echo "docker image prune -a"

docker image prune -a