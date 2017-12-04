# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from sql import Null
from sql.aggregate import Max
from sql.operators import Concat

from trytond.model import Workflow, ModelView, fields
from trytond.pyson import Eval
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond import backend

from trytond.modules.product import price_digits

__all__ = ['ShipmentIn', 'ShipmentInReturn', 'Move', 'Location']


class ShipmentIn:
    __metaclass__ = PoolMeta
    __name__ = 'stock.shipment.in'

    @classmethod
    def __setup__(cls):
        super(ShipmentIn, cls).__setup__()
        add_remove = [
            ('supplier', '=', Eval('supplier')),
            ]
        if not cls.incoming_moves.add_remove:
            cls.incoming_moves.add_remove = add_remove
        else:
            cls.incoming_moves.add_remove = [
                add_remove,
                cls.incoming_moves.add_remove,
                ]
        if 'supplier' not in cls.incoming_moves.depends:
            cls.incoming_moves.depends.append('supplier')

        cls._error_messages.update({
                'reset_move': ('You cannot reset to draft move "%s" because '
                    'it was generated by a purchase.'),
                })

    @classmethod
    def write(cls, *args):
        pool = Pool()
        Purchase = pool.get('purchase.purchase')
        PurchaseLine = pool.get('purchase.line')

        super(ShipmentIn, cls).write(*args)

        actions = iter(args)
        for shipments, values in zip(actions, actions):
            if values.get('state') not in ('received', 'cancel'):
                continue
            purchases = []
            move_ids = []
            for shipment in shipments:
                move_ids.extend([x.id for x in shipment.incoming_moves])

            purchase_lines = PurchaseLine.search([
                    ('moves', 'in', move_ids),
                    ])
            if purchase_lines:
                for purchase_line in purchase_lines:
                    if purchase_line.purchase not in purchases:
                        purchases.append(purchase_line.purchase)

            with Transaction().set_context(_check_access=False):
                purchases = Purchase.browse([p.id for p in purchases])
                Purchase.process(purchases)

    @classmethod
    @ModelView.button
    @Workflow.transition('draft')
    def draft(cls, shipments):
        PurchaseLine = Pool().get('purchase.line')
        for shipment in shipments:
            for move in shipment.incoming_moves:
                if (move.state == 'cancel'
                        and isinstance(move.origin, PurchaseLine)):
                    cls.raise_user_error('reset_move', (move.rec_name,))

        return super(ShipmentIn, cls).draft(shipments)


class ShipmentInReturn:
    __metaclass__ = PoolMeta
    __name__ = 'stock.shipment.in.return'

    @classmethod
    def __setup__(cls):
        super(ShipmentInReturn, cls).__setup__()
        cls._error_messages.update({
                'reset_move': ('You cannot reset to draft a move generated '
                    'by a purchase.'),
                })

    @classmethod
    def __register__(cls, module_name):
        pool = Pool()
        Move = pool.get('stock.move')
        PurchaseLine = pool.get('purchase.line')
        Purchase = pool.get('purchase.purchase')
        cursor = Transaction().connection.cursor()
        sql_table = cls.__table__()
        move = Move.__table__()
        line = PurchaseLine.__table__()
        purchase = Purchase.__table__()

        # Migration from 3.8: New supplier field
        cursor.execute(*sql_table.select(sql_table.supplier,
                where=sql_table.supplier == Null, limit=1))
        if cursor.fetchone():
            value = sql_table.join(move, condition=(
                    Concat(cls.__name__ + ',', sql_table.id) == move.shipment)
                ).join(line, condition=(
                        Concat(PurchaseLine.__name__ + ',', line.id)
                        == move.origin)
                ).join(purchase,
                    condition=(purchase.id == line.purchase)
                ).select(Max(purchase.party))
            cursor.execute(*sql_table.update(
                    columns=[sql_table.supplier],
                    values=[value]))
        super(ShipmentInReturn, cls).__register__(module_name)

    @classmethod
    def write(cls, *args):
        pool = Pool()
        Purchase = pool.get('purchase.purchase')
        PurchaseLine = pool.get('purchase.line')

        super(ShipmentInReturn, cls).write(*args)

        actions = iter(args)
        for shipments, values in zip(actions, actions):
            if values.get('state') != 'done':
                continue
            move_ids = []
            for shipment in shipments:
                move_ids.extend([x.id for x in shipment.moves])

            purchase_lines = PurchaseLine.search([
                    ('moves', 'in', move_ids),
                    ])
            purchases = set()
            if purchase_lines:
                for purchase_line in purchase_lines:
                    purchases.add(purchase_line.purchase)

            with Transaction().set_context(_check_access=False):
                purchases = Purchase.browse([p.id for p in purchases])
                Purchase.process(purchases)

    @classmethod
    @ModelView.button
    @Workflow.transition('draft')
    def draft(cls, shipments):
        PurchaseLine = Pool().get('purchase.line')
        for shipment in shipments:
            for move in shipment.moves:
                if (move.state == 'cancel'
                        and isinstance(move.origin, PurchaseLine)):
                    cls.raise_user_error('reset_move')

        return super(ShipmentInReturn, cls).draft(shipments)


class Move:
    __metaclass__ = PoolMeta
    __name__ = 'stock.move'
    purchase = fields.Function(fields.Many2One('purchase.purchase', 'Purchase',
            states={
                'invisible': ~Eval('purchase_visible', False),
                },
            depends=['purchase_visible']), 'get_purchase',
        searcher='search_purchase')
    purchase_quantity = fields.Function(fields.Float('Purchase Quantity',
            digits=(16, Eval('unit_digits', 2)),
            states={
                'invisible': ~Eval('purchase_visible', False),
                },
            depends=['purchase_visible', 'unit_digits']),
        'get_purchase_fields')
    purchase_unit = fields.Function(fields.Many2One('product.uom',
            'Purchase Unit', states={
                'invisible': ~Eval('purchase_visible', False),
                }, depends=['purchase_visible']), 'get_purchase_fields')
    purchase_unit_digits = fields.Function(fields.Integer(
        'Purchase Unit Digits'), 'get_purchase_fields')
    purchase_unit_price = fields.Function(fields.Numeric('Purchase Unit Price',
            digits=price_digits, states={
                'invisible': ~Eval('purchase_visible', False),
                }, depends=['purchase_visible']), 'get_purchase_fields')
    purchase_currency = fields.Function(fields.Many2One('currency.currency',
            'Purchase Currency', states={
                'invisible': ~Eval('purchase_visible', False),
                }, depends=['purchase_visible']), 'get_purchase_fields')
    purchase_visible = fields.Function(fields.Boolean('Purchase Visible'),
        'on_change_with_purchase_visible')
    supplier = fields.Function(fields.Many2One('party.party', 'Supplier'),
        'get_supplier', searcher='search_supplier')
    purchase_exception_state = fields.Function(fields.Selection([
        ('', ''),
        ('ignored', 'Ignored'),
        ('recreated', 'Recreated'),
        ], 'Exception State'), 'get_purchase_exception_state')

    @classmethod
    def __register__(cls, module_name):
        TableHandler = backend.get('TableHandler')
        cursor = Transaction().connection.cursor()
        sql_table = cls.__table__()

        super(Move, cls).__register__(module_name)

        table = TableHandler(cls, module_name)

        # Migration from 2.6: remove purchase_line
        if table.column_exist('purchase_line'):
            cursor.execute(*sql_table.update(
                    columns=[sql_table.origin],
                    values=[Concat('purchase.line,', sql_table.purchase_line)],
                    where=sql_table.purchase_line != Null))
            table.drop_column('purchase_line')

    @classmethod
    def _get_origin(cls):
        models = super(Move, cls)._get_origin()
        models.append('purchase.line')
        return models

    @classmethod
    def check_origin_types(cls):
        types = super(Move, cls).check_origin_types()
        types.add('supplier')
        return types

    def get_purchase(self, name):
        PurchaseLine = Pool().get('purchase.line')
        if isinstance(self.origin, PurchaseLine):
            return self.origin.purchase.id

    @classmethod
    def search_purchase(cls, name, clause):
        return [('origin.' + clause[0],) + tuple(clause[1:3])
            + ('purchase.line',) + tuple(clause[3:])]

    def get_purchase_exception_state(self, name):
        PurchaseLine = Pool().get('purchase.line')
        if not isinstance(self.origin, PurchaseLine):
            return ''
        if self in self.origin.moves_recreated:
            return 'recreated'
        if self in self.origin.moves_ignored:
            return 'ignored'

    def get_purchase_fields(self, name):
        PurchaseLine = Pool().get('purchase.line')
        if isinstance(self.origin, PurchaseLine):
            if name[9:] == 'currency':
                return self.origin.purchase.currency.id
            elif name[9:] in ('quantity', 'unit_digits', 'unit_price'):
                return getattr(self.origin, name[9:])
            else:
                return getattr(self.origin, name[9:]).id
        else:
            if name[9:] == 'quantity':
                return 0.0
            elif name[9:] == 'unit_digits':
                return 2

    @fields.depends('from_location', 'to_location')
    def on_change_with_purchase_visible(self, name=None):
        if self.from_location:
            if self.from_location.type == 'supplier':
                return True
        elif self.to_location:
            if self.to_location.type == 'supplier':
                return True
        return False

    def get_supplier(self, name):
        PurchaseLine = Pool().get('purchase.line')
        if isinstance(self.origin, PurchaseLine):
            return self.origin.purchase.party.id

    @property
    def origin_name(self):
        pool = Pool()
        PurchaseLine = pool.get('purchase.line')
        name = super(Move, self).origin_name
        if isinstance(self.origin, PurchaseLine):
            name = (self.origin.purchase.reference
                or self.origin.purchase.rec_name)
        return name

    @classmethod
    def search_supplier(cls, name, clause):
        return [('origin.purchase.party' + clause[0].lstrip(name),)
            + tuple(clause[1:3]) + ('purchase.line',) + tuple(clause[3:])]

    @classmethod
    @ModelView.button
    @Workflow.transition('cancel')
    def cancel(cls, moves):
        pool = Pool()
        Purchase = pool.get('purchase.purchase')
        PurchaseLine = pool.get('purchase.line')

        super(Move, cls).cancel(moves)
        purchase_lines = PurchaseLine.search([
                ('moves', 'in', [m.id for m in moves]),
                ])
        if purchase_lines:
            purchase_ids = list(set(l.purchase.id for l in purchase_lines))
            purchases = Purchase.browse(purchase_ids)
            Purchase.process(purchases)

    @classmethod
    def delete(cls, moves):
        pool = Pool()
        Purchase = pool.get('purchase.purchase')
        PurchaseLine = pool.get('purchase.line')

        purchases = set()
        purchase_lines = PurchaseLine.search([
                ('moves', 'in', [m.id for m in moves]),
                ])

        super(Move, cls).delete(moves)

        if purchase_lines:
            for purchase_line in purchase_lines:
                purchases.add(purchase_line.purchase)
            if purchases:
                with Transaction().set_context(_check_access=False):
                    purchases = Purchase.browse([p.id for p in purchases])
                    Purchase.process(purchases)


class Location:
    __metaclass__ = PoolMeta
    __name__ = 'stock.location'

    supplier_return_location = fields.Many2One(
        'stock.location', 'Supplier Return',
        states={
            'invisible': Eval('type') != 'warehouse',
            'readonly': ~Eval('active'),
            },
        domain=[
            ('type', '=', 'storage'),
            ('parent', 'child_of', [Eval('id', -1)]),
            ],
        depends=['type', 'active', 'id'],
        help='If empty the Storage location is used')
