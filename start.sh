echo "docker build . -t grsranking"

docker build . -t grsranking

echo "docker compose up -d --remove-orphans"

docker compose up -d --remove-orphans

echo "docker image prune -a"

docker image prune -a