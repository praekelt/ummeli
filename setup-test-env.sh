# We must do a custom build of pysqlite
wget http://pysqlite.googlecode.com/files/pysqlite-2.6.0.tar.gz
tar xzf pysqlite-2.6.0.tar.gz
cd pysqlite-2.6.0
echo "[build_ext]\

#define=\

include_dirs=/usr/local/include\

library_dirs=/usr/local/lib\

libraries=sqlite3\

#define=SQLITE_OMIT_LOAD_EXTENSION" > setup.cfg
../ve/bin/python setup.py install
sudo /sbin/ldconfig
cd ..
