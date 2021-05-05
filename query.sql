-- purchase order excel
select po.name as po_ref, pol.name as product, po.date_order, rp.name as partner, po.amount_total, 
dte.name as dterm, dti.name as dtime, apt.name as payment_term, po.state as state,sp.name as picking
from purchase_order_line pol
join purchase_order po on pol.order_id=po.id
join res_partner rp on po.partner_id=rp.id
join bi_delivery_term dte on po.delivery_term_id=dte.id
join bi_delivery_time dti on po.delivery_time_id=dti.id
join account_payment_term apt on po.payment_term_id=apt.id
join purchase_order_stock_picking_rel posp on po.id=posp.purchase_order_id
join stock_picking sp on posp.stock_picking_id=sp.id
;

-- raw material order     status
-- qty doneee noooooooooooooot
select po.name as po_ref, pol.name as product, po.date_order, rp.name as partner,
pol.product_qty, sp.scheduled_date ,sm.quantity_done
from purchase_order_line pol
join purchase_order po on pol.order_id=po.id
join res_partner rp on po.partner_id=rp.id
join purchase_order_stock_picking_rel posp on po.id=posp.purchase_order_id
join stock_picking sp on posp.stock_picking_id=sp.id
join stock_move sm on sp.id=sm.picking_id
;