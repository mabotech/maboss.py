
function AvlDataCtrl($scope){

/*
(u'GCIC_T_AVL_DATA', u'ID', u'CHAR', 1, 10, -1, None, 1, None, 0, None, u'avl', 1000004L, 1, 0, None, None)
*/
/*
(u'GCIC_T_AVL_DATA', u'TYPE', u'SMALLINT', 1, None, -1, None, 0, None, 0, None, u'avl', 1000004L, 2, 0, None, None)
*/
/*
(u'GCIC_T_AVL_DATA', u'STATUS', u'SMALLINT', 1, None, -1, None, 0, None, 0, None, u'avl', 1000004L, 3, 0, None, None)
*/
/*
(u'GCIC_T_AVL_DATA', u'COMMENTS', u'NVARCHAR', 0, 1000, -1, None, 0, None, 0, None, u'avl', 1000004L, 4, 0, None, None)
*/
/*
(u'GCIC_T_AVL_DATA', u'TESTCELL', u'NVARCHAR', 0, 40, -1, None, 0, None, 0, None, u'avl', 1000004L, 5, 0, None, None)
*/
/*
(u'GCIC_T_AVL_DATA', u'PALLET', u'NVARCHAR', 0, 40, -1, None, 0, None, 0, None, u'avl', 1000004L, 6, 0, None, None)
*/
/*
(u'GCIC_T_AVL_DATA', u'ESN', u'NVARCHAR', 0, 40, -1, None, 0, None, 0, None, u'avl', 1000004L, 7, 0, None, None)
*/
/*
(u'GCIC_T_AVL_DATA', u'TESTDATE', u'DATETIME', 0, None, -1, None, 0, None, 0, None, u'avl', 1000004L, 8, 0, None, None)
*/
/*
(u'GCIC_T_AVL_DATA', u'SPEED', u'NUMERIC', 0, 18, 0, None, 0, None, 0, None, u'avl', 1000004L, 9, 0, None, None)
*/
/*
(u'GCIC_T_AVL_DATA', u'PWR_KW', u'NUMERIC', 0, 18, 0, None, 0, None, 0, None, u'avl', 1000004L, 10, 0, None, None)
*/
/*
(u'GCIC_T_AVL_DATA', u'TORQUE', u'NUMERIC', 0, 18, 0, None, 0, None, 0, None, u'avl', 1000004L, 11, 0, None, None)
*/
/*
(u'GCIC_T_AVL_DATA', u'BSFC', u'NUMERIC', 0, 18, 0, None, 0, None, 0, None, u'avl', 1000004L, 12, 0, None, None)
*/
/*
(u'GCIC_T_AVL_DATA', u'FUEL_RATE', u'NUMERIC', 0, 18, 0, None, 0, None, 0, None, u'avl', 1000004L, 13, 0, None, None)
*/
/*
(u'GCIC_T_AVL_DATA', u'OIL_FILTER_P', u'NUMERIC', 0, 18, 0, None, 0, None, 0, None, u'avl', 1000004L, 14, 0, None, None)
*/
/*
(u'GCIC_T_AVL_DATA', u'BLOWBY_L_P', u'NUMERIC', 0, 18, 0, None, 0, None, 0, None, u'avl', 1000004L, 15, 0, None, None)
*/
/*
(u'GCIC_T_AVL_DATA', u'IN_MANIFOLD_L_P', u'NUMERIC', 0, 18, 0, None, 0, None, 0, None, u'avl', 1000004L, 16, 0, None, None)
*/
/*
(u'GCIC_T_AVL_DATA', u'COOLANT_IN_T', u'NUMERIC', 0, 18, 0, None, 0, None, 0, None, u'avl', 1000004L, 17, 0, None, None)
*/
/*
(u'GCIC_T_AVL_DATA', u'CELL_AIR_T', u'NUMERIC', 0, 18, 0, None, 0, None, 0, None, u'avl', 1000004L, 18, 0, None, None)
*/
/*
(u'GCIC_T_AVL_DATA', u'FUEL_IN_P', u'NUMERIC', 0, 18, 0, None, 0, None, 0, None, u'avl', 1000004L, 19, 0, None, None)
*/
/*
(u'GCIC_T_AVL_DATA', u'FUEL_IN_T', u'NUMERIC', 0, 18, 0, None, 0, None, 0, None, u'avl', 1000004L, 20, 0, None, None)
*/
/*
(u'GCIC_T_AVL_DATA', u'FUEL_OUT_P', u'NUMERIC', 0, 18, 0, None, 0, None, 0, None, u'avl', 1000004L, 21, 0, None, None)
*/
/*
(u'GCIC_T_AVL_DATA', u'COOLANT_OUT_T', u'NUMERIC', 0, 18, 0, None, 0, None, 0, None, u'avl', 1000004L, 22, 0, None, None)
*/
/*
(u'GCIC_T_AVL_DATA', u'COOLANT_OUT_P', u'NUMERIC', 0, 18, 0, None, 0, None, 0, None, u'avl', 1000004L, 23, 0, None, None)
*/
/*
(u'GCIC_T_AVL_DATA', u'COOLANT_IN_P', u'NUMERIC', 0, 18, 0, None, 0, None, 0, None, u'avl', 1000004L, 24, 0, None, None)
*/
/*
(u'GCIC_T_AVL_DATA', u'SMOKE', u'NUMERIC', 0, 10, 0, None, 0, None, 0, None, u'avl', 1000004L, 25, 0, None, None)
*/
/*
(u'GCIC_T_AVL_DATA', u'TURBO_TUR_OUT_L_T', u'NUMERIC', 0, 10, 0, None, 0, None, 0, None, u'avl', 1000004L, 26, 0, None, None)
*/
/*
(u'GCIC_T_AVL_DATA', u'TURBO_TUR_OUT_L_P', u'NUMERIC', 0, 10, 0, None, 0, None, 0, None, u'avl', 1000004L, 27, 0, None, None)
*/
/*
(u'GCIC_T_AVL_DATA', u'OPACITY', u'NUMERIC', 0, 10, 0, None, 0, None, 0, None, u'avl', 1000004L, 28, 0, None, None)
*/

}
 
