SELECT
    700000 + ROW_NUMBER() OVER (ORDER BY name) AS "Código",
    name->>'es_ES' AS materia_prima,
    -1 as Activo, 
    '' as "Exis. Máxima", '' as "Exis. Mínima", '' AS "Punto Reorden",	
    'Gr.' as "Unid. Medida", 	
	'' as "Precio 1",
	'' as "Precio 2", '' as "Precio 3", '' as "Precio 4",
	'' as "Grupo Uno",
	'0' as IVA,
	'' AS "Tipo Iva",
	'Producto' as "Clasificación", 'Producto' AS "Clasificación Niif",
	0 as Producto,
	-1 "Facturar sin Existen.",
	-1 as "Pertenece Produc.",
	'' AS "Producto Proceso",
	0 AS "Maneja Seriales",
	'' AS Observaciones,
	'' AS "Verificar Utilidad", '' AS "Utilidad Estimada",
	'' AS Arancel,
	'' AS Impoconsumo, '' AS "Porcentaje de impoconsumo", '' AS "ImpoConsumo al Costo",
	0 AS "Iva Mayor Vr al costo", '' AS "Gasto que afecta el Costo",
	'' AS "Centro Costos",
	'' AS "Código Barras",
	'' AS "Favorito POS",
	'' AS "Imagen POS",
	'' AS Impresora,
	'' AS "Ocualtar Imprimir",
	'' AS "Código Internacional",
	'' AS "Grupo Dos", '' AS "Grupo Tres", '' AS "Grupo Cuatro", '' AS "Grupo Cinco", '' AS "Grupo Seis", '' AS "Grupo Siete", '' AS "Grupo Ocho", '' AS "Grupo Nueve", '' AS "Grupo Diez",
	'' AS "Precio 5", '' AS "Precio 6", '' AS "Precio 7", '' AS "Precio 8", '' AS "Precio 9", '' AS "Precio 10", '' AS "Precio 11", '' AS "Precio 12", '' AS "Precio 13",
	'' AS "Precio 14", '' AS "Precio 15", '' AS "Precio 16", '' AS "Precio 17", '' AS "Precio 18", '' AS "Precio 19", '' AS "Precio 20", '' AS "Precio 21",
	'' AS "Precio 22", '' AS "Precio 23", '' AS "Precio 24", '' AS "Precio 25", '' AS "Precio 26", '' AS "Precio 27", '' AS "Precio 28", '' AS "Precio 29",	'' AS "Precio 30",
	'' AS "Personalizado 1", '' AS "Personalizado 2", '' AS "Personalizado 3", '' AS "Personalizado 4", '' AS "Personalizado 5", '' AS "Personalizado 6",
	'' AS "Personalizado 7", '' AS "Personalizado 8", '' AS "Personalizado 9", '' AS "Personalizado 10", '' AS "Personalizado 11", '' AS "Personalizado 12",
	'' AS "Personalizado 13", '' AS "Personalizado 14", '' AS "Personalizado 15",
	'' AS "Código Centro Costos"
FROM (
  SELECT DISTINCT
    ptmp.name
  FROM mrp_bom AS b
  JOIN mrp_bom_line AS bl ON bl.bom_id = b.id
  JOIN product_product AS pp ON bl.product_id = pp.id
  JOIN product_template AS ptmp ON pp.product_tmpl_id = ptmp.id
) AS materias_primas
ORDER BY name;

