## Install packages
```
yum install -y epel-release
yum install -y httpd mod_wsgi
yum install -y python-pip gcc python-devel
pip install virtualenv
```

## Install MariaDB 10.2
```
cat > /etc/yum.repos.d/MariaDB.repo << EOF
[mariadb]
name = MariaDB
baseurl = http://yum.mariadb.org/10.2/centos7-amd64
gpgkey=https://yum.mariadb.org/RPM-GPG-KEY-MariaDB
gpgcheck=1
EOF

yum install -y MariaDB-server MariaDB-client
systemctl start mariadb
systemctl enable mariadb
```

Firewall Setting
```
firewall-cmd --permanent --add-service=mysql
firewall-cmd --permanent --add-port=3306/tcp
firewall-cmd --reload
```

## Create project
```
cd /opt
git clone http://172.16.100.91/cc-iaas/cc-iaas-sdnms.git
cd cc-iaas-sdnms
virtualenv python_env
source python_env/bin/activate

pip install -r requirements.txt -c upper-constraints-pike.txt
pip install -r requirements.txt
```

## Start dev http server
```
python sdnms_api/app/server.py --config=etc/sdnms_api/sdnms_api_dev.ini
```

## Test dev http server
```
curl http://localhost:8000/health
```