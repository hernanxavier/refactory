# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2008-2010 SIA "KN dati". (http://kndati.lv) All Rights Reserved.
#                    General contacts <info@kndati.lv>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from report import report_sxw
import time 
import tools
import pdb
from lxml import etree
from datetime import datetime

class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            "divide_date": self._divide_date

                })


    def _divide_date(self, date_str):
        """
        :param date_str: Fecha con formato de string
        :return retorna una tupla con dia, mes, año
        """
        if not date_str:
            return []
        day_list = [
            "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete",
            "ocho", "nueve", "diez", "once", "doce", "trece", "catorce",
            "quince", "dieciseis", "diecisiete", "dieciocho", "dieciocho",
            "diecinueve", "veinte", "veintiuno", "veintidos", "veintitres",
            "vienticuatro", "veinticinco", "veintiseis", "veintisiete", "veintiocho",
            "veintinueve", "treinta", "treinta y uno",
            ]

        month_list = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio","julio",
            "agosto", "septiembre", "octubre", "noviembre", "diciembre",
            ]

        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        day = date.day
        month = date.month
        year = date.year
        phrase = (u'a los %s días del mes de %s del año %s') %(day_list[day-1], month_list[month-1], year)
        return phrase