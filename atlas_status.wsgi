import site
import sys

site.addsitedir("/var/www/atlas-status/venv/lib/python2.6/site-packages")
sys.path.insert(0, "/var/www/atlas-status")
from atlas_status import app as application
