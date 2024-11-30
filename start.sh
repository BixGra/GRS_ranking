echo "docker build . -t grsrankinghost"

docker build . -t grsrankinghost

echo "docker compose up -d --remove-orphans"

docker compose up -d --remove-orphans

echo "docker image prune -a"

docker image prune -a