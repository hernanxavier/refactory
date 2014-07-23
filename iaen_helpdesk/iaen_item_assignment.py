# -*- coding: utf-8 -*-
# #############################################################################
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

import openerp
from openerp.osv import fields, osv, expression
from openerp.tools.translate import _
from openerp.tools.float_utils import float_round as round
import openerp.addons.decimal_precision as dp
import openerp.tools.image as imageoerp
from datetime import date
import pdb


class item_type(osv.osv):
    _name = "item.type"
    _description = "Tipos de items (Portatiles, Proyectores, Bolsos... )"
    _order = "name"
    _sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe n item con el mismo nombre'))]
    _columns = {
        "name": fields.char("Nombre", size=255, required=True),
        "description": fields.char("Descripción", size=100),
    }


class item_brand(osv.osv):
    _name = "item.brand"
    _description = "Almacena las diferentes marcas de los items"
    _order = "name"
    _sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe una marca con el mismo nombre'))]
    _columns = {
        "name": fields.char("Nombre", size=255, required=True),
    }


class location(osv.osv):
    _name = "location"
    _description = "Para almacenar todos los locales o edificios de la institusion"
    _order = "name"
    _sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe un local con el mismo nombre'))]
    _columns = {
        "name": fields.char("Nombre", size=255, required=True),
        "address": fields.char("Direccion", size=255),
        "observations": fields.text("Observaciones", help="Observaciones adicionales sobre el edificio."),
    }


class dependence(osv.osv):
    _name = "dependence"
    _description = "Almancena aulas, oficinas, auditorios de la institucion"
    _order = "name"
    _sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe una dependencia con el mismo nombre'))]
    _columns = {
        "name": fields.char("Nombre", size=255, required=True),
        "observations": fields.text("Observaciones"),
        "location_ids": fields.many2one("location", "Edificio", required=True)
    }


class item_status(osv.osv):
    _name = "item.status"
    _description = "Almacena el listdo de estados de un equipo informatico"
    _order = "name"
    _sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe un estado con el mismo nombre'))]
    _columns={
        "name": fields.char("Estado del item", size=40, required=True),
        "description": fields.text("Descripción"),
    }


class head_assignment(osv.osv):

    def count_detail(self, cr, uid, ids, context=None):
        """
        :param cr: Conexión Base de datos
        :param uid: Usuario logueado
        :param ids: id de la cabecera
        :param context:
        :return: True or false
        description: Función verifica que en el detalle del acta
                     existan elementos  y que no se repitan en el detalle del acta
        """
        global flag, repeat
        read = self.browse(cr, uid, ids)[0]
        if read.detail_assignment_ids:  #<-- Verifica eistencia de items en detalle
            for x in read.detail_assignment_ids:    #<-- Verifica items repetidos en el detalle
                repeat = 0
                flag = False
                for y in read.detail_assignment_ids:
                    if x == y:
                        repeat += 1
                if repeat == 0:
                    flag = True
                else:
                    return False
            if flag:
                return True
            else:
                return False
        else:
            return False

    def change_state(self, cr, uid, ids, state, context=None):
        """
        :param cr:
        :param uid:
        :param ids:
        :param state:
        :param context:
        :return:
        """
        if state == 'assignment':
            name = self.pool.get("ir.sequence").get(cr, uid, "head.assignment")
            read = self.browse(cr, uid, ids)[0]
            for x in read.detail_assignment_ids:
                record = self.pool.get("detail.assignment").browse(cr, uid, x.id)
                self.pool.get("account.asset.asset").write(cr, uid, record.cod_item_id['id'],
                                                           {'assignment': True}, context=None)
            self.write(cr, uid, ids, {'state': state, 'name': name})
        else:
            self.write(cr, uid, ids, {'state': state})

        """
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'head.assignment',
            'views': [(False, 'tree'), (ids[0], 'form')],
            'res_id': ids[0],
        }
        """
        """
            read = self.browse(cr, uid, ids)[0]
            det_ids = []
            for x in read.detail_assignment_ids:
                det_ids.append(x.id)
            record = {
                "name": name,
                "date": read.date,
                "deliv_employ_id": read.deliv_employ_id['id'],
                "assig_employ_id": read.assig_employ_id['id'],
                "observations": read.observations,
                "detail_assignment_ids": det_ids,
                "state": state,
            }
            print record
            #self.create(cr, uid, record, context=context)
        """

    _name = "head.assignment"
    _description = "Cabecera actas entrega/recepcion"
    _order = "deliv_employ_id"
    #_sql_constraints = [('name_unique', 'unique(name)', _(u'Ya existe un estado con el mismo nombre'))]
    _columns = {
        "name": fields.char("Código", size=20, required=False, readonly=True),
        "date": fields.date("Fecha", required=True),
        "deliv_employ_id": fields.many2one("hr.employee", "Entrega", required=True),
        "assig_employ_id": fields.many2one("hr.employee", "Recibe", required=True),
        "observations": fields.text("Observaciones"),
        "detail_assignment_ids": fields.one2many("detail.assignment", "head_assignment_id", required=True),
        'state': fields.selection([
                      ('draft', 'Nueva'),
                      ('assignment', 'Asignada'),
                      ('discharge', 'Descargada'),
                      ('partial', 'Parcial'),
                      ('cancel', 'Cancelada'),
                      ('finished', 'Finalizada')], "Estado", readonly=True)
    }
    _constraints = [(count_detail, _(u"El detalle del acta, debe tener items que no se repitan."), ['Detalle'])]
    _defaults = {
        #'name': lambda obj, cr, uid, context: obj.pool.get("ir.sequence").get(cr, uid, "head.assignment"),
         'name': 'DRAFT',
         'date': date.today().strftime('%Y-%m-%d'),
         'state': 'draft',
    }


class detail_assignment(osv.osv):
    def on_change_fill_data_item(self, cr, uid, ids, code_item_id=None, context=None):
        """
        Busca información pertinente del item (activo) seleccionado
        en la tabla de activos fijos
        """
        if context is None:
            context = {}
        if not code_item_id:
            return []
        read = self.pool.get("account.asset.asset").browse(cr, uid, code_item_id) #<- Busqueda
        record = {"name_item": read.name, "serial_number": read.serial_number, "category": read.category_id.name,
                  "brand": read.brand.name, "model": read.model, "status": read.status_id.name} #<- Armamos el diccionario para rellenar los campos pertinentes del detalle
        return {"value": record}

    def on_change_fill_data_dependence(self, cr, uid, ids, dependence_id=None, context=None):
        """
        Busca información de las oficinas seleccionadas y autorellena campos
        """
        if context is None:
            context = {}
        if not dependence_id:
            return []
        read = self.pool.get("location").browse(cr, uid, dependence_id) #<- Busqueda
        record = {"location_id": read.id, } #<- Armamos el diccionario para rellenar los campos pertinentes del detalle
        return {"value": record}

    def create(self, cr, uid, vals, context=None):
        #Busqueda campos producto que son readonly de la forma
        read = self.pool.get("account.asset.asset").browse(cr, uid, vals['cod_item_id'])
        record = {"name_item": read.name, "serial_number": read.serial_number, "category": read.category_id.name,
                  "brand": read.brand.name, "model": read.model, "status": read.status_id.name}
        vals = dict(record.items() + vals.items())
        #Busqueda del nombre de edificio de una dependencia que es readonly en la forma
        read = self.pool.get("location").browse(cr, uid, vals['dependence_id'])
        record = {"location_id": read.id}
        vals = dict(record.items() + vals.items())
        return super(detail_assignment, self).create(cr, uid, vals, context=context)


    _name = "detail.assignment"
    _description = "Detalle acta entrega/recepcion"
    _columns = {
        "head_assignment_id": fields.many2one("head.assignment", "detail_assignment_id"),
        "quantity": fields.integer("Cant."),
        "cod_item_id": fields.many2one("account.asset.asset", "Código"),
        "name_item": fields.char("Nombre", size=255),
        "serial_number": fields.char("Num. Serie", size=255),
        "category": fields.char("Categoria", size=255),
        "brand": fields.char("Marca", size=255),
        "model": fields.char("Modelo", size=255),
        "dependence_id": fields.many2one("dependence", "Dpto."),
        "location_id": fields.many2one("location", "Edificio"),
        "floor": fields.char("Piso"),
        "city_id": fields.many2one("canton", "Ciudad"),
        "status": fields.char("Estado", size=255),
    }
    _defaults = {
        "quantity": 1,
    }


class account_asset_asset(osv.osv):
    """
    Sobreescribe la clase account_asset_asset agrega campos
    Sobreescribe fuciónes name_get y name_search
    """
    _inherit = "account.asset.asset"

    def name_get(self, cr, uid, ids, context=None):
        """
        :param cr: Conexion Base de datos
        :param uid: id usuario logueado
        :param ids: id temporal de registro
        :param context: contexto
        :return: retorna un lista vacia o una tupla con el código y nombre del producto
        """
        if context is None:
            context = {}
        if not ids:
            return []
        res = []
        reads = self.browse(cr, uid, ids, context=context)
        for record in reads:
            name = record.name
            code = record.code
            res.append((record.id, "%s - %s" % (code, name)))
        return res

    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        """
        :param cr: Conexión Base de datos
        :param uid: id usuario logueado
        :param ids: id temporal de registro
        :param context: contexto
        :param limit: caracteres para la busqueda
        :param name: caracteres digitados para la busqueda
        :param args:
        :param operator: operador para la busqueda de registro
        :return: retorna resultado de funcion name_get
        """
        if not args:
            args = []
        if not context:
            context = {}
        if name:
            ids = self.search(cr, uid, [('name', operator, name), ('assignment', '=', False)] + args, limit=limit, context=context)
            if not ids:
                ids = self.search(cr, uid, [('code', operator, name), ('assignment', '=', False)] + args, limit=limit, context=context)
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
        return self.name_get(cr, uid, ids, context)

    _columns = {
        "serial_number": fields.char("Num. Serie", size=255),
        "brand": fields.many2one("item.brand", "Marca", size=255),
        "model": fields.char("Modelo", size=255),
        "status_id": fields.many2one("item.status", "Estado del equipo"),
        "assignment": fields.boolean("Asignado", defatult=True),

    }