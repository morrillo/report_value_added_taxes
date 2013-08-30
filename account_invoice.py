# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-today OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)

class account_invoice(osv.osv):
    """ Account Invoice """
    _name = "account.invoice"
    _inherit = "account.invoice"

    def action_move_report_sales(self, cr, uid, ids, context=None):
	""" Creates VAT sales report lines """
	invoice_ids = self.search(cr,uid,[('id','=',ids[0])])
	for invoice in self.browse(cr,uid,invoice_ids):
		tax_ids = self.pool.get('account.invoice.tax').search(cr,uid,[('invoice_id','=',invoice.id)])
		for tax_line in self.pool.get('account.invoice.tax').browse(cr,uid,tax_ids):	
			vals_create = {
				'invoice_date': invoice.date_invoice,
				'journal_name': invoice.journal_id.name,
				'invoice_name': invoice.number,
				'partner_name': invoice.partner_id.name,
				'period_code': invoice.period_id.code,
				'vat': invoice.partner_id.vat,
				'iibb': invoice.partner_id.iibb,
				'net_amount': invoice.amount_untaxed,
				'amount_total': invoice.amount_total,
				'name': tax_line.name,
				'type': invoice.type,
				'active': True
				}
			if invoice.partner_id.responsability_id.id == 1:
				# Consumidor Final
				vals_create['amount_vat_end_consumer'] = tax_line.tax_amount
			else:
				vals_create['amount_vat_end_consumer'] = 0
			if invoice.partner_id.responsability_id.id == 5:
				# No responsable	
				vals_create['amount_vat_not_responsible'] = tax_line.tax_amount
			else:
				vals_create['amount_vat_responsible'] = 0
			if invoice.partner_id.responsability_id.id == 3:
				# Responsable inscripto
				vals_create['amount_vat_responsible'] = tax_line.tax_amount
			else:
				vals_create['amount_vat_responsible'] = 0
			
			report_sales_id = self.pool.get('account.invoice.report_vat').create(cr,uid,vals_create)
		# TODO check error on report_sales_id	
	return None

account_invoice()

class account_invoice_report_vat(osv.osv):
    """ Account Invoice """
    _name = "account.invoice.report_vat"
    _description = "VAT Report line"

    def download_vat_report_file(self,cr,uid,context=None):
	""" creates file with VAT report """
	import csv

	download_directory_id = self.pool.get('ir.config_parameter').search(cr,uid,[('key','=','download_directory')])
	if not download_directory_id:
		logging.getLogger(__name__).info('VAT Report Line: No download directory present at ir.config_parameter')
		return None
	for parameter in self.pool.get('ir.config_parameter').browse(cr,uid,download_directory_id):
		directory = parameter.value
	if directory[len(directory)-1:] <> '/':
		directory = directory + '/'

	ofile  = open(directory+'report.csv', "wb")
	writer = csv.writer(ofile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)

	vat_report_line_ids = self.pool.get('account.invoice.report_vat').search(cr,uid,[('active','=',True)])
	for vat_report_line in self.pool.get('account.invoice.report_vat').browse(cr,uid,vat_report_line_ids):
		row = []
		partner_name = unicode(vat_report_line.name)
		row.append(str(vat_report_line.type))
		row.append(str(vat_report_line.invoice_date))
		row.append(str(vat_report_line.journal_name))
		row.append(str(vat_report_line.invoice_name))
		try:
			row.append(partner_name)
		except:
			import pdb;pdb.set_trace()
		row.append(str(vat_report_line.vat))
		row.append(str(vat_report_line.iibb))
		row.append(str(vat_report_line.net_amount))
		row.append(str(vat_report_line.tax_description))
		row.append(str(vat_report_line.amount_vat_responsible))
		row.append(str(vat_report_line.amount_vat_not_responsible))
		row.append(str(vat_report_line.amount_vat_end_consumer))
		row.append(str(vat_report_line.amount_total))
    		writer.writerow(','.join(row))

	ofile.close()

        return None	

    _columns = {
	'name': fields.char('Name'),
	'invoice_name': fields.char('Invoice Name'),
	'invoice_date': fields.date('Invoice date'),
	'journal_name': fields.char('Journal Name'),
	'partner_name': fields.char('Partner Name'),
	'period_code': fields.char('Fiscal Period'),
	'vat': fields.char('VAT'),
	'iibb': fields.char('IIBB'),
	'net_amount': fields.float('Net invoice amount'),
	'tax_description': fields.char('Tax Description'),
	'amount_vat_responsible': fields.float('VAT Responsible Amount'),
	'amount_vat_not_responsible': fields.float('VAT Not Responsible Amount'),
	'amount_vat_end_consumer': fields.float('VAT End Consumer Amount'),
	'amount_total': fields.float('Total Amount'),
	'invoice_id': fields.many2one('account.invoice','Invoice'),
	'type': fields.char('Invoice Type'),
        'active': fields.boolean('Active', help="If the active field is set to False, it will allow you to hide the vat report line without removing it."),
	}

    _default = {
	'active': 1
	}

account_invoice_report_vat()
