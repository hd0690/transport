# -*- coding: utf-8 -*-
# Copyright (c) 2018, FinByz Tech Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import db
from frappe.model.document import Document

class Trip(Document):
	def on_submit(self):
		if self.status == "On Trip" and self.ending_datetime:
			self.db_set('status', 'Completed')
			db.commit()

		frappe.db.set_value("Truck Master", self.truck_no, 'status', 'On Trip')
		frappe.db.set_value("Driver Master", self.driver, 'status', 'On Trip')
		frappe.db.set_value("Khalasi Master", self.khalasi, 'status', 'On Trip')

	def on_cancel(self):
		if self.status == "Completed":
			self.db_set('status', 'Cancelled')
			db.commit()

		frappe.db.set_value("Truck Master", self.truck_no, 'status', 'Available')
		frappe.db.set_value("Driver Master", self.driver, 'status', 'Available')
		frappe.db.set_value("Khalasi Master", self.khalasi, 'status', 'Available')
