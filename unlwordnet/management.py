
import os
import urllib2
import sys
from pyunpack import Archive

class UNLWordNetCfg():
    stdout = sys.stdout

    def _download(self, url, filename):
        u = urllib2.urlopen(url)
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])

        # Check file and filesize
        if os.path.isfile(filename) and os.path.getsize(filename) == file_size:
            return

        f = open(filename, 'wb')
        self.stdout.write("\tDownloading: %s Bytes: %s" % (filename, file_size))
        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            self.stdout.write('\t' + status)
        self.stdout.write('\n\tdownloaded to file %r' % filename)
        f.close()

    def _safe_create(self, directory, safe=True):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def install(self, tmp_dir=None, reinstall=False):
        me = os.path.dirname(__file__)

        # Create work directory
        tmp_dir = tmp_dir or os.path.join(me, 'tmp')
        self._safe_create(tmp_dir)
        self.stdout.write("\n")

        # Install dependencies
        self.install_dependencies(os.path.join(me, 'utils'))
        self.stdout.write("\n")

        # Install database
        self.install_database(tmp_dir)
        self.stdout.write("\n")


    def install_database(self, tmp_dir):
        self.stdout.write("Installing database\n")

        # Download database
        filename = os.path.join(tmp_dir, 'unlwn21.rar')
        url = 'http://www.ronaldomartins.pro.br/unlwordnet/database/unlwn21.rar'
        self._download(url, filename)

        # Uncompress file
        mdb_file = os.path.join(tmp_dir, 'unlwn21.mdb')
        if not os.path.isfile(mdb_file):
            self.stdout.write("\tUncompressing file...\n")
            self.stdout.flush()
            Archive(filename).extractall(tmp_dir)

        # Populate sqlite.db
        if not os.path.isfile('unlwn21.db'):
            self.stdout.write("\tMigrating database to sqlite3...\n")
            self.stdout.flush()
            os.system('MDB_JET3_CHARSET="cp1255" python utils/AccessDump.py %s | sqlite3 %s' % (mdb_file, 'unlwn21.db'))



    def install_dependencies(self, path):
        self.stdout.write("Installing dependencies\n")

        # AccessDump.py: utility to convert .mdb files to .sqlite3
        #   gist at https://gist.github.com/mywarr/9908044
        filename = os.path.join(path, 'AccessDump.py')
        if not filename:
            url = 'https://gist.githubusercontent.com/mywarr/9908044/raw/f8cc70731634f44c94506106844094ac4baaf911/AccessDump.py'
            self._download(url, filename)



if __name__ == '__main__':
    unlwordnet = UNLWordNetCfg()
    unlwordnet.install()