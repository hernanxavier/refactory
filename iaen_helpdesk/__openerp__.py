# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
{
    'name' : 'IAEN helpdesk',
    'version' : '1.0',
    'author' : 'IAEN',
    'category' : 'Modulo para Soporte',
    'description' : """
    Módulo que contendrá funciones para
    solventar necesidades del equipo de soporte el IAEN
    """,
    'website': 'http://www.iaen.edu.ec',
    'data': [
        'views/iaen_helpdesk_views.xml',
        'views/iaen_helpdesk_actions.xml',
        'views/iaen_helpdesk_menus.xml',
        'data/item_status_data.xml',
        ],
    'update_xml': [
        'sequence/head_assignment_sequence.xml',
        'reports/certificate_assignment/certificate_assignment.xml',
        'workflow/head_assignment_workflow.xml',
        ],
    'depends': [
        'account_asset',
        'iaen_base',
        'base',
        'report_aeroo',        
        'hr',    
        ],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
