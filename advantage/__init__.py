__version__ = "0.0.1"
import erpnext.crm.utils
from advantage.override.crmnote import AdvantageCRMNote
 
# This replaces the original class reference with your custom one
erpnext.crm.utils.CRMNote = AdvantageCRMNote