echo "Building and pushing 'latest'"
docker-compose build
docker-compose push

$OPENMOXIE_VERSION = Get-Content -Path ".\site\VERSION"
echo "Building and pushing '$OPENMOXIE_VERSION'"
docker-compose build
docker-compose push
