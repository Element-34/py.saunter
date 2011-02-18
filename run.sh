export PYTHONPATH=./modules
export NOWNAME=`date '+%Y-%m-%d-%H-%M-%S'`

# check for a selenium server, and if there isn't one then start it
python modules/SeleniumServer.py --check
if [ $? = 1 ]; then
  python modules/SeleniumServer.py --start
fi

# run the scripts
nosetests -s -w scripts -m="*.py$" --testmatch=".*" -a $* --with-xunit --xunit-file=logs/$NOWNAME.xml
cp logs/$NOWNAME.xml logs/latest.xml

# kill the server (if it was started by us then a pid file will exist)
python modules/SeleniumServer.py --stop