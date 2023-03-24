# Loads .env if exists, means localhost will have right env variables and in cloud use secrets manager
if [ -f .env ]; then
  export $(echo $(cat .env | sed 's/#.*//g'| xargs) | envsubst)
fi

echo

docker build -t simulation-processing-backend --build-arg GOOGLE_MAPS_API_KEY=$GOOGLE_MAPS_API_KEY -f run.Dockerfile .

pack build simulator-backend-final-build --builder gcr.io/buildpacks/builder:v1 --run-image simulation-processing-backend