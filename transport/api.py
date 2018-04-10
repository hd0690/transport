import frappe
from frappe import _, msgprint, db, get_list, delete_doc, get_doc
from frappe.utils import get_url_to_form


@frappe.whitelist()
def payment_on_submit(self, method):
	po_payments(self, method)

@frappe.whitelist()
def pi_on_submit(self, method):
	create_part_tool(self, method)

@frappe.whitelist()
def pi_on_cancel(self, method):
	cancel_part_tool(self, method)
	
def create_part_tool(self, method):
	parts = []
	for row in self.items:
		if row.item_group == "Truck Part":
			part_tool = frappe.new_doc("Part Creation Tool")
			part_tool.truck_part = row.item_code
			part_tool.part_company = row.part_company
			part_tool.number_of_parts = int(row.qty)
			part_tool.warehouse = row.part_warehouse
			part_tool.purchase_invoice = self.name
			part_tool.supplier = self.supplier
			part_tool.purchase_date = self.posting_date
			part_tool.purchase_rate = row.rate
			part_tool.save()
			db.commit()
			link = get_url_to_form("Part Creation Tool", part_tool.name)
			parts.append("<b><a href='{0}'>{1}</a></b>".format(link.replace('localhost', 'localhost:8081'),row.item_code))
			
	if parts:
		msgprint(_("Part Creation Tool updated for parts '%s'. Please submit the document to create parts."%(",".join(parts))))


def cancel_part_tool(self, method):
	result = get_list("Part Creation Tool", filters={'purchase_invoice': self.name}, fields='name')
				
	for row in result:
		delete_doc("Part Creation Tool", row.name)
			
#Update PO payments on Submit
def po_payments(self, method):
	for row in self.references:
		if row.reference_doctype == "Purchase Order":
			target_po = get_doc("Purchase Order", row.reference_name)
			
			target_po.append("payments", {
				"reference_date": self.reference_date,
				"mode_of_payment": self.mode_of_payment,
				"reference_no": self.reference_no,
				"paid_amount" : row.allocated_amount,
				"payment_entry" : self.name,
				"difference_amount" : self.difference_amount
			})
		target_po.save()
		db.commit()