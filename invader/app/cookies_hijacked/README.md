For running a sqlite db into a clean firefox you can launch a docker container like that :
```
sudo docker run -d \
                -v $HOME/Downloads:/home/firefox/Downloads:rw \
                -v /tmp/www.deezer.com.sqlite:/home/firefox/.mozilla/firefox/cookies.sqlite \
                -v /tmp/.X11-unix:/tmp/.X11-unix \
                -v /dev/snd:/dev/snd \
                -e uid=$(id -u) \
                -e gid=$(id -g) \
                -e DISPLAY=unix$DISPLAY \
                --privileged \
                --name firefox-cookies \
                chrisdaish/firefox
```

Don't forget to change the path for the sqlite db