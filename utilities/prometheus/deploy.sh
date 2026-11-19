ln -s /root/myfirstvps/utilities/prometheus/prometheus.yml /etc/prometheus/prometheus.yml

docker run \
  --name=prometheus \
  --detach \
  --network=host \
  --volume=/etc/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml \
  --volume=/home/user/prometheus/:/prometheus/ \
  --restart=always ubuntu/prometheus \
  --config.file=/etc/prometheus/prometheus.yml
