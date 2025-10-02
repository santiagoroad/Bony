SELECT
  pt.name->>'es_ES' AS "Nombre Producto",
  ptmp.name->>'es_ES' AS "Nombre Materia Prima",
  bl.product_qty AS "Ficha Técnica: Cantidad"
FROM mrp_bom AS b
JOIN product_template AS pt ON b.product_tmpl_id = pt.id
LEFT JOIN product_product AS pp_default
  ON pp_default.product_tmpl_id = pt.id AND b.product_id IS NULL
JOIN mrp_bom_line AS bl ON bl.bom_id = b.id
JOIN product_product AS pp ON bl.product_id = pp.id
JOIN product_template AS ptmp ON pp.product_tmpl_id = ptmp.id
JOIN uom_uom AS uom ON bl.product_uom_id = uom.id
ORDER BY pt.name;

