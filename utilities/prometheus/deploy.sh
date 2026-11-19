ln -s /root/myfirstvps/utilities/prometheus/prometheus.yml /etc/prometheus/prometheus.yml

docker run \
  --name=node_exporter \
  --detach \
  --network=host \
  --volume=/proc:/host/proc:ro \
  --volume=/sys:/host/sys:ro \
  --volume=/:/rootfs:ro \
  --pid=host \
  --restart=always \
  prom/node-exporter:latest \
  --path.procfs=/host/proc \
  --path.sysfs=/host/sys \\
  --path.rootfs=/rootfs \
  '--collector.filesystem.ignored-mount-points=^/(dev|proc|sys|var/lib/docker/.+|var/lib/containers/.+)($|/)'

docker run \
  --name=prometheus \
  --detach \
  --network=host \
  --volume=/etc/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml \
  --volume=/home/user/prometheus/:/prometheus/ \
  --restart=always \
  ubuntu/prometheus \
  --config.file=/etc/prometheus/prometheus.yml
