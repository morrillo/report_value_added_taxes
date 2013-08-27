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

    def action_move_create(self, cr, uid, ids, context=None):
	import pdb;pdb.set_trace()
	res = super(account_invoice,self).action_move_create(cr,uid,ids,context)
	return res

account_invoice()

