__version__ = "0.0.1"
import erpnext.crm.utils
from advantage.override.crmnote import AdvantageCRMNote
import erpnext.selling.doctype.quotation.quotation
#import   erpnext.crm.doctype.prospect.prospect       
#from advantage.utils import advantage_make_customer_prospect
from advantage.utils import advantage_make_customer
# This replaces the original class reference with your custom one
erpnext.crm.utils.CRMNote = AdvantageCRMNote
erpnext.selling.doctype.quotation.quotation._make_customer=advantage_make_customer
#erpnext.crm.doctype.prospect.prospect.make_customer=advantage_make_customer_prospect