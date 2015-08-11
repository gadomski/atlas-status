import site
site.addsitedir("/var/www/atlas-status/venv/lib/python2.6/site-packages")
from atlas_status import app as application
