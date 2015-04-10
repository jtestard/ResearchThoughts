{ "aggregates" : [ { "order_year" : "2010",
          "sum_price" : 10.0
        } ],
    "nation_key" : 1,
    "nation_name" : "Canada"
  },
  { "aggregates" : [
  		{
  		  "order_year" : "2010",
          "sum_price" : 15.0
        },
        { "order_year" : "2011",
          "sum_price" : 5.0
        }
      ],
    "nation_key" : 2,
    "nation_name" : "England"
  },
  { "aggregates" : [  ],
    "nation_key" : 3,
    "nation_name" : "Algeria"
  }
  project ([result])
    assign [result] <- { “nation_key” : n.nation_key, “nation_name” : n.nation_name, “aggregates” : r.aggregates }
    left-outer-join l.nation_key = r.nation_key
    	//Right tree
    	
{{
	bt1 <- { "nation_key" : 1, "aggregates" : [
			{
				"order_year" : "2010" , "list_price" : 10.0
			}
		]
	}
	bt2 <- { "nation_key" : 2, "aggregates" : [
			{
				"order_year" : "2010" , "list_price" : 15.0
			},
			{
				"order_year" : "2011" , "list_price" : 5.0
			}
		]
	}
}}
	assign r <- { "nation_key" : nation_key, "aggregates" : aggregates }
	subplan {
		aggregate aggretates <- listify( g )
		assign g <- { "order_year" : g.order_year, "sum_price" : g.sum_price }
		limit 3
		order DESC, g.list_price;
		unnest g <- newGroup
		nested tuple source
	}
	group by nation_key <- nation_key {
		aggregate newGroup <- listify ( newGroupVar )
		nested tuple source }
{{
	bt1 <- { "newGroupVar" : {
		"nation_key" : 1, "order_year" : "2010" , "list_price" : 10.0
	}, ...}
	bt2 <- { "newGroupVar" : {
		"nation_key" : 2, "order_year" : "2010" , "list_price" : 15.0
	}, ...}
	bt3 <- { "newGroupVar" : {
		"nation_key" : 2, "order_year" : "2011" , "list_price" : 5.0
	}, ...}
}}
		assign newGroupVar <- { "nation_key" : nation_key, "order_year" : order_year, "list_price" : list_price }
		assign list_price <- sql-sum ( list_of_prices )
			subplan {
				aggregate list_of_prices <- listify ( total_price ) ; assign total_price <- g.o.total_price
				unnest g <- groupVar; nested tuple source }
{{
	bt1 <- { 
		"nation_key" : 1, "order_year" : "2010" , "group" {{
			{
				"o" : { "order_key" : 1, "cust_ref" : 1 , "order_year" : "2011", "total_price" : 10.0 },
				"c" : { "cust_key" : 1, "nation_ref" : 1 },
				"n" : { "nation_key" : 1, "nation_name" : "Canada" }
			}
		}}
	},
	bt2 <- { 
		"nation_key" : 2, "order_year" : "2010" , "group" {{
			{
				"o" : { "order_key" : 2, "cust_ref" : 2 , "order_year" : "2010", "total_price" : 15.0 },
				"c" : { "cust_key" : 2, "nation_ref" : 2 },
				"n" : { "nation_key" : 2, "nation_name" : "England" }
			},
			{
				"o" : { "order_key" : 3, "cust_ref" : 2 , "order_year" : "2011", "total_price" : 5.0 },
				"c" : { "cust_key" : 2, "nation_ref" : 2 },
				"n" : { "nation_key" : 2, "nation_name" : "England" }
			}
		}}
	}
}}
		group by nation_key <- n.nation_key, order_year <- o.order_year {
			aggregate group <- listify ( groupVar ) ; nested tuple source }
		assign groupVar <- { "n" : n, “c” : c, “o” : o }
{{
	bt1 <- {
		"o" : { "order_key" : 1, "cust_ref" : 1 , "order_year" : "2010", "total_price" : 10.0 },
		"c" : { "cust_key" : 1, "nation_ref" : 1 },
		"n" : { "nation_key" : 1, "nation_name" : "Canada" }
	},
	bt2 <- {
		"o" : { "order_key" : 2, "cust_ref" : 2 , "order_year" : "2010", "total_price" : 15.0 },
		"c" : { "cust_key" : 2, "nation_ref" : 2 },
		"n" : { "nation_key" : 2, "nation_name" : "England" }
	},
	bt3 <- {
		"o" : { "order_key" : 3, "cust_ref" : 2 , "order_year" : "2011", "total_price" : 5.0 },
		"c" : { "cust_key" : 2, "nation_ref" : 2 },
		"n" : { "nation_key" : 2, "nation_name" : "England" }
	}
}}
		select o.cust_ref = c.cust_key and c.nation_ref = n.nation_key
		unnest c <- scan-dataset Customers
	    	unnest o <- scan-dataset Orders
	    		distinct n.nation_key
		    		unnest n <- scan-dataset Nations
   		 				empty-tuple-source                              
		//Left tree
{{
{ "nation_key" : 1, "nation_name" : "Canada" },
{ "nation_key" : 2, "nation_name" : "England" },
{ "nation_key" : 3, "nation_name" : "Algeria" }
}}		
    	unnest l <- scan-dataset Nations
    		empty-tuple-source