__version__ = "0.0.1"
import erpnext.crm.utils
from advantage.override.crmnote import AdvantageCRMNote
import erpnext.selling.doctype.quotation.quotation

from advantage.utils import advantage_make_customer

erpnext.crm.utils.CRMNote = AdvantageCRMNote
erpnext.selling.doctype.quotation.quotation._make_customer=advantage_make_customer
