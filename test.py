PL_include = {'/var/log/httpd/accesslog', '/etc/rc.d/rc.local', '/proc/self/net/arp', 'proc/self/stat',
              '/opt/nginx/logs/access.log', '/etc/php.ini', '/var/www/html/', '/etc/apache2/mods-available/dir.conf',
              '/proc/self/status', '/proc/self/net/route', '/var/log/access_log', '/etc/inetd.conf',
              '/tmp/sess_SESSIONID', '/var/log/apache/access.log', '/usr/local/apache2/conf/httpd.conf', '/etc/hosts',
              '/etc/init.d/httpd', '/usr/local/apache/conf/httpd.conf', '/proc/self/cwd', '/var/log/apache/access_log',
              '/var/log/apache2/access.log', '/usr/local/etc/apache22/httpd.conf', '/etc/httpd/logs/access_log',
              '/proc/self/environ', '/etc/my.cnfmysql', '/var/log/nginx/access.log', '/etc/nginx/nginx.conf',
              '/proc/version', '/etc/httpd/conf/http.conf', '/etc/httpd/httpd.conf', '/etc/apache2/httpd.conf',
              '/usr/local/app/php5/lib/php.ini', '/etc/httpd/conf/httpd.conf', '/usr/pkg/etc/httpd/httpd.conf',
              '/proc/self/cmdline', '/etc/apache2/apache2.conf', '/proc/self/maps', '/usr/local/etc/nginx/nginx.conf',
              '/var/log/apache2/error.log', '/usr/local/app/apache2/conf/http.conf', '/var/log/nginx/error.log',
              '/etc/apache2/envvars', '/usr/local/nginx/logs/access.log', '/var/www/logs/access_log', '/proc/self/fd/3',
              '/etc/apache/httpd.conf', '/usr/local/etc/apache/httpd.conf', '/usr/local/etc/apache2/httpd.conf',
              '/etc/passwd', '/proc/self/exe', '/etc/nginx/conf.d/default.conf', '/var/log/apache/error.log'}

for i in PL_include:
    print(i)
