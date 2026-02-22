# Copyright (c) 2026, ItsPrivate and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.defaults import add_default,_clear_cache
from frappe.cache_manager import clear_defaults_cache,clear_user_cache


class AdvantageDefault(Document):
	def on_update(self):
		reference_doctype = frappe.scrub(self.doc_type)
		frappe.db.delete("DefaultValue", {"defkey": reference_doctype, "parent": self.usr})
		frappe.db.commit()
		add_default(reference_doctype,self.value,self.usr)
		_clear_cache( self.usr)
		clear_defaults_cache(self.usr)
		clear_user_cache(self.usr)
	
	
	def on_trash(self):
		reference_doctype = frappe.scrub(self.doc_type)
		frappe.db.delete("DefaultValue", {"defkey": reference_doctype, "parent": self.usr})		 
		frappe.db.commit()
		_clear_cache( self.usr)
		clear_defaults_cache(self.usr)
		clear_user_cache(self.usr)
		