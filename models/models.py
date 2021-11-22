# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class Partner(models.Model):
    _inherit = 'res.partner'

    noktp = fields.Char(string="No KTP")   
    gender = fields.Selection([('ml', 'Male'),('fm', 'Female')], string="Gender")
    dadname = fields.Char(string="Father's Name")
    momname = fields.Char(string="Mother's Name")
    job = fields.Char(string="Job")
    plbirth = fields.Char(string="Place Of Birth")
    dtbirth = fields.Date(string="Date Of Birth")
    bloodtype = fields.Selection([('a', 'A'),('b', 'B'),('ab', 'AB'),('o', 'O')], string="Blood Type")
    maritalstatus = fields.Selection([('j', 'Joness'),('m', 'Married'),('putus', 'Divorce')], string="Marital Status")
    education = fields.Selection([('sd', 'Elementary'),('smp', 'Junior'),('sma', 'High/Vocational'),('d3', 'D3'),('s1', 'S1'),('s2', 'S2'),('s3', 'S3')], string="Education")
    age = fields.Integer(readonly=True)
class TravelPackage(models.Model):
    _name = 'travel.package'
    _description = 'Package Record'
    # many2one = id
    # one2many = line
    # many2many = ids

    name = fields.Char(string="Reference",default="/", readonly=True)
    product_id = fields.Many2one('product.product', 'Sale',readonly=True, states={'draft': [('readonly', False)]})
    departuredate = fields.Date(string="Departure Date",readonly=True, states={'draft': [('readonly', False)]})
    returndate = fields.Date(string="Return Date",readonly=True, states={'draft': [('readonly', False)]})
    quota = fields.Integer(string="Quota",readonly=True, states={'draft': [('readonly', False)]})
    quotaprogress = fields.Float(string="Quota Progress", compute="quotaprog",readonly=True, states={'draft': [('readonly', False)]})
    totalcost = fields.Char(string="Total Cost",readonly=True, states={'draft': [('readonly', False)]})
    status = fields.Char(string="Status",readonly=True, states={'draft': [('readonly', False)]})
    package_id = fields.Many2one('product.template', 'Package',readonly=True, states={'draft': [('readonly', False)]})
    seats = fields.Integer(string="Remaining Seats",readonly=True, states={'draft': [('readonly', False)]})
    amount = fields.Integer(string="Amount",readonly=True, states={'draft': [('readonly', False)]})
    product2_id = fields.Many2one('product.template', 'Product',readonly=True, states={'draft': [('readonly', False)]})
    total_cost = fields.Float(string='Total Cost', readonly=True, compute='func_total_cost', states={'draft': [('readonly', False)]})
    note = fields.Text(string='Note', placeholder="Note..",readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Confirmed'),
        ('done', 'Done'),
    ], string='Status', readonly=True, copy=False, default='draft', track_visibility='onchange')

    
    hotellines = fields.One2many('hotel.lines', 'hotel2_id', string='Hotel Lines',readonly=True, states={'draft': [('readonly', False)]})
    airlinelines = fields.One2many('airline.lines', 'airlines2_id', string='Airline Lines',readonly=True, states={'draft': [('readonly', False)]})
    schedulelines = fields.One2many('schedule.lines', 'schedule2_id', string='schedule Lines',readonly=True, states={'draft': [('readonly', False)]})
    manifestlines = fields.One2many('travel.manifest', 'manifest2_id', string='Manifest',readonly=True, states={'draft': [('readonly', False)]})
    hpplines = fields.One2many('hpp.lines', 'hpplines2_id', string='HPP Lines',readonly=True, states={'draft': [('readonly', False)]})
    commissionlines = fields.One2many('commission.lines', 'commission2_id', string='Commission Lines',readonly=True, states={'draft': [('readonly', False)]})

    @api.depends('quota', 'quotaprogress')
    def quotaprog(self):
        for r in self:
            if not r.quota:
                r.quotaprogress = 0.0
            else:
                r.quotaprogress = 100.0 * r.quota / 100.0



    
    @api.model
    def create(self, vals):
        # Override the original create function for the res.partner model
        vals['name'] = self.env['ir.sequence'].next_by_code('travel.package')
        return super(TravelPackage, self).create(vals)

    @api.onchange('quota')
    def onchange_seats(self):                
        for rs in self:
            if rs.quota:    
                return {
                        'value': {
                            'seats': rs.quota                      
                        }
                }
    
 
    @api.onchange('package_id')
    def onchange_package(self):                
        travelpackage = self
        nilai = []
        for t in travelpackage.package_id.bom_ids.bom_line_ids:
            nilai.append({'producthpp_id' : t.product_id.id, 'quantity' : t.product_qty, 'uom_id' : t.product_id.uom_id})
        if travelpackage.package_id:    
            return {
                    'value': {
                        'hpplines': nilai                       
                    }
            }

    

    @api.multi
    def action_confirm(self):
        self.write({'state' : 'open'})
        print ("##############################")
        print ("masuk confirm")
        print ("##############################")
    @api.multi
    def action_cancel(self):
        self.write({'state' : 'draft'})
        print ("##############################")
        print ("masuk cancel")
        print ("##############################")
    @api.multi
    def action_close(self):
        self.write({'state' : 'done'})
        print ("##############################")
        print ("masuk close")
        print ("##############################")  

    @api.multi
    def action_updatejamaah(self):
        updatejamaah = self.env['sale.order'].search([('travelpackage', '=', self.id)])
        if updatejamaah:
            self.manifestlines.unlink()
            for o in updatejamaah:
                for x in o.saleorderlines:
                    self.env['travel.manifest'].create({
                            'manifest2_id': self.id,
                            'jamaah_id': x.jamaah_id.id,
                            'passportno': x.passportno,
                            'passportname': x.passportname,
                            'dateissued': x.dateissued,
                            'dateexpiry': x.dateexpiry,
                            'imigration': x.imigration,
                            'age': x.age,
                            'roomtype': x.roomtype,
                            'mahram_id': x.mahram_id.id,
                    })

    # Compute harus di tulis woyyy
    @api.depends('hpplines')
    def func_total_cost(self):
        for x in self:
            a = []
            for y in x.hpplines:
                a.append(y.subtotal)
            x.total_cost = (sum(a))
    
    @api.multi
    def print_manifest(self):
        return self.env.ref("travelumroh.print_manifest").report_action(self)
class HotelLines(models.Model):
    _name = 'hotel.lines'
    _description = 'Hotel Lines'

    
    hotel_id = fields.Many2one('res.partner', string='Hotel')
    hotel2_id = fields.Many2one('travel.package', string='Hotel') 
    startdate = fields.Date(required= True)
    enddate = fields.Date()
    city    = fields.Char(
    related='hotel_id.city',
    readonly=True,
    store=True
    )
class AirlineLines(models.Model):
    _name = 'airline.lines'
    _description = 'Airline Lines'

    airlines_id = fields.Many2one('res.partner', string='Airline')
    airlines2_id = fields.Many2one('travel.package', string='Airline')

    departuredate = fields.Date()
    departurecity = fields.Char()
    arrivalcity = fields.Char(required= True)
class ScheduleLines(models.Model):
    _name = 'schedule.lines'
    _description = 'Schedule Lines'
   
    schedule2_id = fields.Many2one('travel.package', string='Schedule')
    schedule_id = fields.Char(string="Name", required= True)
    date = fields.Date()   
class Manifest(models.Model):
    _name = 'travel.manifest'
    _description = 'Manifest'
    
    manifest2_id   =   fields.Many2one('travel.package', string='Manifest')
    manifestsalder_id = fields.Many2one('sale.order', string="Manifest")
    jamaah_id = fields.Many2one('res.partner', string="Jamaah")

    title_id   =   fields.Many2one('res.partner.title' ,related='jamaah_id.title', string="Title") 
    gender  =   fields.Selection(related='jamaah_id.gender', string="Gender")
    passportname    =   fields.Char(string="Passport Name")
    passportno  =   fields.Char(string="Passport No")
    ktpno   =   fields.Char(related='jamaah_id.noktp' , string="KTP No")
    birthdate   =   fields.Date(related='jamaah_id.dtbirth', string="Date Of Birth")
    birthplace  =   fields.Char(related='jamaah_id.plbirth', string="Place Of Birth")
    dateissued  =   fields.Date(string="Date Issued")
    dateexpiry  =   fields.Date(string="Date Of Expiry")
    imigration  =   fields.Char(string="Imigrasi")
    age     =   fields.Integer(string="Age")
    roomtype    =   fields.Selection([('s', 'Single'), ('d', 'Double'), ('q', 'Quad')], string="Room Type")
    mahram_id =   fields.Many2one('res.partner', string="Mahram")
    agent   =   fields.Char(string="Agent")
    foto = fields.Binary(string='Photo')

    
    @api.onchange('jamaah_id')
    def get_age(self):
        dateLahir = self.jamaah_id.dtbirth
        dateNow = date.today()
        self.age = relativedelta(dateNow, dateLahir).years            
class saleorder(models.Model):
    _inherit = 'sale.order'

    saleorderlines = fields.One2many('travel.manifest', 'manifestsalder_id', string='Passport Lines')
    doclines = fields.One2many('document.lines','doclines_id', string='Document Lines')
    travelpackage = fields.Many2one('travel.package', string='Travel Packages', domain=[('state', '=', 'open')])

    @api.onchange('travelpackage')
    def func_orderline(self):
        x = {}
        if self.travelpackage:
            tp = self.travelpackage
            x['value'] = {
                'order_line': [{
                    'product_id': tp.product_id.id,
                    'name':  tp.product_id.name,
                    'product_uom_qty': 1,
                    'product_uom': tp.product_id.uom_id.id,
                    'price_unit': tp.product_id.list_price
                }]
            }
        return x
class stockpicking(models.Model):
    _inherit = 'stock.picking'

    

    @api.multi
    def button_suratjalan(self):
        print("assdfghjghfgdfs-------------------")
        print("assdfghjghfgdfs-------------------")
        return self.env.ref("travelumroh.button_suratjalan").report_action(self)    
class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    @api.multi
    def button_invoice(self):
        print("***********************************")
        print("***********************************")
        return self.env.ref("travelumroh.button_invoice").report_action(self)
class documentlines(models.Model):
    _name = 'document.lines'
    _description = 'document lines'

    
    # cuman yg diconfirm doang yg bisa di....
    # onchange di travel package
    # harus update sesuai dgn di video

    name = fields.Char(string="Name", 
    required=True
    )
    foto = fields.Binary(
        string='Photo',
    )
    doclines_id = fields.Many2one('sale.order', string='doclines') 
class HPPLines(models.Model):
    _name = 'hpp.lines'
    _description = 'HPP Lines'

    hpplines2_id   =   fields.Many2one('travel.package', string='HPP Lines')
    producthpp_id =   fields.Many2one('product.product', string="Product")
    quantity    =   fields.Float(string="Quantity")
    uom_id =   fields.Many2one('uom.uom', string="UoM")
    unitprice   =   fields.Float(string="Unit Price", required= True)
    subtotal    =   fields.Float(string="Subtotal")

    @api.onchange('unitprice')
    def onchange_subtotal(self):                
        for st in self:
            if st.unitprice:    
                print ("#######SUBTOTAL#######")
                return {
                        'value': {
                            'subtotal': st.unitprice * st.quantity                       
                        }
                }
class CommissionLines(models.Model):
    _name = 'commission.lines'
    _description = 'Commission Lines'

    commission2_id   =   fields.Many2one('travel.package', string='Commission Lines')
    vendor  = fields.Char(string="Vendor")
    billdate    = fields.Char(string="Bill Date")
    number  = fields.Char(string="Number")
    vendorreference = fields.Char(string="Vendor Reference")
    duedate = fields.Char(string="Due Date")
    sourcedocument  = fields.Char(string="Source Document")
    total   = fields.Char(string="Total")
    topay   = fields.Char(string="To Pay")
    status  = fields.Char(string="Status")

    

    
        
    

    
    
    
   