# class SampleReportPrint(models.Model):
# 	_name = 'report.bi_report.print_sample_report'
# 	@api.model
# 	def _get_report_values(self, docids, data):
#     	bi_report = data['bi_report']
#         value = []
#         query = """SELECT *
#                         FROM sale_order as s_l
#                         JOIN sale_order_line AS s_o_l ON s_l.id = s_o_l.sale_order_id
#                         WHERE s_l.id = %s"""
#         value.append(model_id)
#         self._cr.execute(query, value)
#         record = self._cr.dictfetchall()
#         return {
#                     'docs': record,
#                     'date_today': fields.Datetime.now(),
#                 }