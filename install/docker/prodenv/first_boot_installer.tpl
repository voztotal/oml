#!/bin/bash

########################## README ############ README ############# README #########################
########################## README ############ README ############# README #########################
# El script first_boot_installer tiene como finalidad desplegar el componente sobre una instancia 
# de linux exclusiva. Las variables que utiliza son "variables de entorno" de la instancia que está
# por lanzar el script como acto seguido al primer boot del sistema operativo.
# Dichas variables podrán ser provisionadas por un archivo .env (ej: Vagrant) o bien utilizando este 
# script como plantilla de terraform. 
#
# En el caso de necesitar ejecutar este script manualmente sobre el user_data de una instancia cloud
# o bien sobre una instancia onpremise a través de una conexión ssh, entonces se deberá copiar
# esta plantilla hacia un archivo ignorado por git: first_boot_installer.sh para luego sobre 
# dicha copia descomentar las líneas que comienzan con la cadena "export" para posteriormente 
# introducir el valor deseado a cada variable.
########################## README ############ README ############# README #########################
########################## README ############ README ############# README #########################

# ************************************************************ SET ENV VARS **********************************************************************
# ************************************************************ SET ENV VARS **********************************************************************

# The infrastructure environment:
# onpremise | digitalocean | linode | vultr
#export oml_infras_stage=onpremise

# Component gitlab branch
#export oml_app_release=release-1.16.0
#export oml_app_img=latest

# OMniLeads tenant NAME
#export oml_tenant_name=onpremise

# BLOCK DEVICE or S3 BUCKET 
# values: local | s3 | nfs | disk
#export oml_callrec_device=s3

# S3 params when you select S3 like store for callrec
#export s3_access_key=
#export s3_secret_key=
#export s3url=
#export s3_bucket_name=

# NFS host netaddr
#export nfs_host=

#export oml_nic=enp0s3

# ******* ACD Asterisk VARS *******
# AMI conection from omlapp
#export oml_ami_user=omnileadsami
#export oml_ami_password=098098ZZZ

# ***********************  PGSQL Vars
# POSTGRESQL netaddr and port
# Values: NULL | IPADDR or FQDN
#export oml_pgsql_host=192.168.95.131
#export oml_pgsql_port=5432
# POSTGRESQL user, pass & DB params
#export oml_pgsql_db=omnileads
#export oml_pgsql_user=omnileads
#export oml_pgsql_password=098098ZZZ
# IF PGSQL run on cloud cluster set this to true
#export oml_pgsql_cloud=NULL

# ***********************  Dialer VARS
#export api_dialer_user=demoadmin
#export api_dialer_password=demo
# Values: NULL | IPADDR or FQDN
#export oml_dialer_host=NULL

# ***********************  WebRTC Bridge VARS
# Values: NULL | IPADDR or FQDN
#export oml_rtpengine_host=NULL


# Tell OMLApp web some params ******************************************************************************
#export oml_tz=America/Argentina/Cordoba
# Session Cookie Age (SCA) is the time in seconds that will last the https session when inactivity 
# is detected in the session (by default is 1 hour)                                                
#export oml_app_sca=3600
# Ephemeral Credentials TTL (ECTTL) is the time in seconds that will last the SIP credentials      
# used to authenticate a SIP user in the telephony system (by default 8 hours)                     
#export oml_app_ecctl=3600
# Login failure limit (LFM) is the attempts a user has to enter an incorrect password in login     
# Decrease it if paranoic reasons                                                                  
#export oml_app_login_fail_limit=10

# Values true | false
#export oml_app_init_env=true
#export oml_app_reset_admin_pass=true
#export oml_app_install_sngrep=true

# ************************************************************ SET ENV VARS **********************************************************************
# ************************************************************ SET ENV VARS **********************************************************************

PUBLIC_IPV4=$(curl -s http://169.254.169.254/metadata/v1/interfaces/public/0/ipv4/address)
PRIVATE_IPV4=$(curl -s http://169.254.169.254/metadata/v1/interfaces/private/0/ipv4/address)

COMPONENT_REPO=https://gitlab.com/omnileads/ominicontacto.git

SRC=/usr/src

echo "Checking if omnileads user/group exists"
existe=$(grep -c '^omnileads:' /etc/passwd)
if [ $existe -eq 0 ]; then
  echo "Creating omnileads group"
  groupadd omnileads
  echo "Creating omnileads user"
  mkdir -p /opt/omnileads
  useradd omnileads -d /opt/omnileads -s /bin/bash -g omnileads
  chown -R omnileads.omnileads /opt/omnileads
else
  echo "The user/group omnileads already exists"
fi

usermod -aG docker omnileads

cd /opt/omnileads
git clone $COMPONENT_REPO
cd ominicontacto
git checkout ${oml_app_release}
cd install/docker/prodenv
cp .env.template .env

sed -i "s/DOCKER_IP=X.X.X.X/DOCKER_IP=$PRIVATE_IPV4/g" .env
sed -i "s%\TZ=your_timezone_here%TZ=${oml_tz}%g" .env
sed -i "s/PGPASSWORD=my_very_strong_pass/PGPASSWORD=${oml_pgsql_password}/g" .env

if [ "${oml_app_img}" != "" ]; then
  sed -i "s/^OMLAPP_VERSION=.*/OMLAPP_VERSION=${oml_app_img}/g" .env
else
  OMLAPP_VERSION=$(cat ../../../.omnileads_version)
  sed -i "s/^OMLAPP_VERSION=.*/OMLAPP_VERSION=$OMLAPP_VERSION/g" .env
fi
if [ "${oml_acd_img}" != "" ]; then
  sed -i "s/^OMLACD_VERSION=.*/OMLACD_VERSION=${oml_acd_img}/g" .env
fi
if [ "${oml_redis_img}" != "" ]; then
  sed -i "s/^OMLREDIS_VERSION=.*/OMLREDIS_VERSION=${oml_redis_img}/g" .env
fi
if [ "${oml_kamailio_img}" != "" ]; then
  sed -i "s/^OMLKAM_VERSION=.*/OMLKAM_VERSION=${oml_kamailio_img}/g" .env
fi
if [ "${oml_nginx_img}" != "" ]; then
  sed -i "s/^OMLNGINX_VERSION=.*/OMLNGINX_VERSION=${oml_nginx_img}/g" .env
fi
if [ "${oml_ws_img}" != "" ]; then
  sed -i "s/^OMLWS_VERSION=.*/OMLWS_VERSION=${oml_ws_img}/g" .env
fi

if [[ "${oml_dialer_host}" != "NULL" ]]; then
  sed -i "s/WOMBAT_HOSTNAME=dialer/WOMBAT_HOSTNAME=${oml_dialer_host}/g" .env
fi
if [[ "${oml_pgsql_host}" == "NULL" ]]; then
  sed -i "s/PGHOST=postgresql/PGHOST=$PRIVATE_IPV4/g" .env
else
  sed -i "s/PGHOST=postgresql/PGHOST=${oml_pgsql_host}/g" .env
fi
if [[ "${oml_rtpengine_host}" == "NULL" ]]; then
  sed -i "s/RTPENGINE_HOSTNAME=rtpengine/RTPENGINE_HOSTNAME=$PRIVATE_IPV4/g" .env
else
  sed -i "s/RTPENGINE_HOSTNAME=rtpengine/RTPENGINE_HOSTNAME=${oml_rtpengine_host}/g" .env
fi

cp daemon.json /etc/docker
cp omnileads.service /etc/systemd/system/

systemctl restart docker
systemctl daemon-reload
systemctl enable omnileads
systemctl start omnileads

chown omnileads. -R /opt/omnileads
