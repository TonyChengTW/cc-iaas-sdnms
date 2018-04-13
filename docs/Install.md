## Install packages
sudo yum install epel-release
sudo yum install httpd mod_wsgi
sudo pip install python-pip virtualenv


## Create project
cd /opt
git clone http://172.16.100.91/cc-iaas/cc-iaas-sdnms.git
cd cc-iaas-sdnms
virtualenv python_env
source python_env/bin/activate


## Apache configuration file
vi /etc/httpd/conf.d/sdnms.conf

<Directory /opt/cc-iaas-sdnms/cc_iaas_sdnms/app>
    <Files wsgi.py>
        Require all granted
    </Files>
</Directory>

WSGIDaemonProcess sdnms
WSGIProcessGroup sdnms
WSGIScriptAlias /sdnms /opt/cc-iaas-sdnms/cc_iaas_sdnms/app/wsgi.py
