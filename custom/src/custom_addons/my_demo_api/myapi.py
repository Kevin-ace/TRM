# from odoo import fields, models
#
# class FastapiEndpoint(models.Model):
#
#     _inherit = "fastapi.endpoint"
#
#     app: str = fields.Selection(
#         selection_add=[("demo", "Demo Endpoint")], ondelete={"demo": "cascade"}
#     )