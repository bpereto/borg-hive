# Install borg-hive on k8s

helm repo add bitnami https://charts.bitnami.com/bitnami
helm dep update

kubectl create namespace borg-hive

helm install mariadb bitnami/mariadb --namespace borg-hive -f values.db.yaml
helm upgrade --install borg-hive . -f values.yaml --namespace borg-hive       
