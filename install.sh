# curl -L https://raw.githubusercontent.com/aitoroses/NIXus/master/install.sh | bash

NIXUS_HOME=~/.nixus

echo ""
echo "Wait while installing the NIXus Platform"
echo ""

git clone https://github.com/aitoroses/NIXus $NIXUS_HOME

cd $NIXUS_HOME
chmod +x ./nixus
cp ./nixus /usr/local/bin/nixus

# Build the containers
echo ""
echo ""
echo "We are building the docker images for you :)"
echo ""
nixus build

echo ""
echo ""
echo "# Now you can run NIXus:"
echo "$ nixus start"
echo ""

echo "# Test the platform is working correctly"
echo "# by running this hello world docker image:"
echo ""
echo "$ docker run -it --rm -p :8000 -e NIXUS_8000=whoami-app jwilder/whoami"
echo ""
echo "# Visit the following link http://<your-docker-host>/whoami-app"
