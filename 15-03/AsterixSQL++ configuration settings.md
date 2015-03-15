## Config options 

To be continued...

(premature) conclusions : it seems that the most immediate problem
with giving out the full string of configurations available for 
AsterixDB people to use is the fact that the interface does not have 
all the configuration parameters already set up. 

```
@tuple_nav { 
	absent: null,
	type_mismatch: error
}
@array_nav {
	absent: null,
	type_mismatch: error
}
@eq {
	complex: error,
	type_mismatch: error,
	null_eq_null:  null,
	null_eq_scalar: null,
	null_eq_complex: null,
	null_and_true: null,
	null_and_false: false
	null_and_null: null
}
@from { // not supported in the live demo
	bag_order : counter
	no_match : null
}
@groupby{
	support : yes
}
```

```
@data.array			yes
@data.bag			yes
@data.tuple			yes
@data.scalar			yes
@data.null			yes
@data.missing			error
@data.heterogeneous			yes
@stored_named.array			error
@stored_named.bag			yes
@stored_named.tuple			error
@stored_named.scalar			error
@stored_named.null			error
@stored_named.missing			irrelevant
@stored_array.element_array			yes
@stored_array.element_bag			yes
@stored_array.element_tuple			yes
@stored_array.element_scalar			yes
@stored_array.element_null			yes
@stored_array.element_missing			irrelevant
@stored_array.heterogeneous			yes
@stored_bag.element_array			partial
@stored_bag.element_bag			partial
@stored_bag.element_tuple			yes
@stored_bag.element_scalar			partial
@stored_bag.element_null			partial
@stored_bag.element_missing			irrelevant
@stored_bag.heterogeneous			yes
@stored_tuple.attribute_array			yes
@stored_tuple.attribute_bag			yes
@stored_tuple.attribute_tuple			yes
@stored_tuple.attribute_scalar			yes
@stored_tuple.attribute_null			yes
@stored_tuple.attribute_missing			irrelevant
@stored_tuple.heterogeneous			yes
@schema.support			yes
@schema.scalar_type			yes
@schema.bag_type			yes
@schema.array_type			yes
@schema.any_type			error
@schema.union_type			error
@schema.open_tuple_type			yes
@schema.closed_tuple_type			yes
@schema.optional_type			yes
@schema.not_null_type			error
@schema.not_missing_type			irrelevant
@literal.array			
@literal.bag			
@literal.tuple			
@literal.scalar			
@literal.null			
@literal.missing			
@subquery.support			yes
@result_missing.normalize_in_array			irrelevant
@result_missing.normalize_in_bag			irrelevant
@result_missing.normalize_in_tuple			irrelevant
@named_value.restrict_to_from			yes
@tuple_nav.support			yes
@tuple_nav.absent			null
@tuple_nav.type_mismatch			error
@array_nav.support			yes
@array_nav.absent			null
@array_nav.type_mismatch			error
@logical.null_and_true			
@logical.null_and_false			
@logical.null_and_null			
@logical.null_and_missing			irrelevant
@logical.missing_and_true			irrelevant
@logical.missing_and_false			irrelevant
@logical.missing_and_missing			irrelevant
@logical.null_or_true			
@logical.null_or_false			
@logical.null_or_null			
@logical.null_or_missing			irrelevant
@logical.missing_or_true			irrelevant
@logical.missing_or_false			irrelevant
@logical.missing_or_missing			irrelevant
@logical.not_null			
@logical.not_missing			irrelevant
@eq.support			yes
@eq.complex			error
@eq.type_mismatch			error
@eq.null_eq_scalar			
@eq.null_eq_null			
@eq.null_eq_missing			irrelevant
@eq.missing_eq_scalar			irrelevant
@eq.missing_eq_missing			irrelevant
@eq.null_eq_complex			irrelevant
@eq.missing_eq_complex			irrelevant
@eq.result_null			
@eq.result_missing			irrelevant
@eq.null_and_true			irrelevant
@eq.null_and_false			irrelevant
@eq.null_and_null			irrelevant
@eq.null_and_missing			irrelevant
@eq.missing_and_true			irrelevant
@eq.missing_and_false			irrelevant
@eq.missing_and_missing			irrelevant
@from.support			yes
@from.named_value			yes
@from.subquery			yes
@from.function_call			yes
@from.array			yes
@from.bag			yes
@from.at			yes
@from.bag_order			counter
@from.tuple			error
@from.no_match			null
@from.inner_correlate			yes
@from.outer_correlate			yes
@from.full_correlate			error
@from.cartesian_product			yes
@from.inner_join			yes
@from.left_join			yes
@from.full_join			error
@from.inner_flatten			yes
@from.outer_flatten			yes
@from_collection.coerce_null			error
@from_collection.coerce_missing			irrelevant
@from_collection.coerce_value			error
@from_tuple.coerce_null			irrelevant
@from_tuple.coerce_missing			irrelevant
@where.support			yes
@where.function_call			yes
@where.subquery			error
@where.coerce_null			error
@where.coerce_missing			irrelevant
@where.coerce_scalar			error
@where.coerce_complex			error
@select.support			yes
@select.element			yes
@select.attribute			error
@select.subquery			yes
@select.path			yes
@select.function_call			yes
@group_by.support			yes
@group_by.scalar			yes
@group_by.complex			error
@group_by.null			yes
@group_by.missing			irrelevant
@group_by.group_var			yes
@order_by.support			
@order_by.with_order			
@order_by.without_order			
@order_by.complex			
@order_by.type_order			
@collection_op.support			error
@collection_op.concatenate			irrelevant
@collection_op.union_all			irrelevant
@collection_op.intersect_all			irrelevant
@collection_op.except_all			irrelevant
@collection_op.union			irrelevant
@collection_op.intersect			irrelevant
@collection_op.except			irrelevant
@collection_op.coerce_null			irrelevant
@collection_op.coerce_missing			irrelevant
@collection_op.coerce_value			irrelevant
```