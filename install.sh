# curl -L https://raw.githubusercontent.com/aitoroses/NIXus/master/install.sh

NIXUS_HOME=~/.nixus

echo "Wait while installing the NIXus Platform \n"

git clone https://github.com/aitoroses/NIXus $NIXUS_HOME

cd $NIXUS_HOME

chmod +x nixus.sh
ls -s nixus.sh /usr/local/bin/nixus

# Build the containers
echo "We are building the docker images for you :) \n"
nixus build

echo "\n\n# Now you can run NIXus:"
echo "$ nixus start \n"

echo "# Test the platform is working correctly"
echo "# By running this hello world docker image:"
echo "$ docker run -it -p :8000 -e NIXUS_8000=whoami-app jwilder/whoami"
echo "# Visit the following link http://<your-docker-host>/whoami-app"
