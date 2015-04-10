import sys
import pycountry
from random import shuffle
from random import randint
from random import uniform
import json
import argparse

# NOTICE : at the moment, only adm output format is supported.

def check_greater_than_zero(value):
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("%s is not an integer" % value)
    if ivalue < 1:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue

def write_to_file(dataset, filename):
    with open(filename, 'w') as f:
        for record in dataset:
            f.write(json.dumps(record, separators=(',', ':')))
        f.write('\n')

def generate_dataset():
    # Parse arguments
    parser = argparse.ArgumentParser(description='Generates a dataset with nations, customers and orders.')
    parser.add_argument(
        '-n',
        '--nations',
        dest='nations',
        action='store',
        type=check_greater_than_zero,
        required=True,
        help='The number of nations to generate. Must be positive and greater than zero.'
    )
    parser.add_argument(
        '-c',
        '--customers',
        dest='customers',
        action='store',
        type=check_greater_than_zero,
        required=True,
        help='The number of customers to generate. Must be positive and greater than zero.'
    )
    parser.add_argument(
        '-o',
        '--orders',
        dest='orders',
        action='store',
        type=check_greater_than_zero,
        required=True,
        help='The number of orders to generate. Must be positive and greater than zero.'
    )
    args = parser.parse_args()
    
    ### PART 1 : Generate Nations
    # Get (shuffled) list of countries from the pycountry module
    countries = map(lambda c : (c.name).encode('ascii', 'ignore'), list(pycountry.countries))
    shuffle(countries)
    
    if args.nations > len(countries):
        nation_count = len(countries)
    else:
        nation_count = args.nations
    
    # Generate nations 
    dataset = []
    
    for i in xrange(nation_count):
       dataset.append({
           'nation_key': i+1,
           'nation_name': countries[i]
       })

    write_to_file(dataset,'nations.adm')
    
    ### Part 2 : Generate Customers
    customer_count = args.customers
    dataset = []
    for i in xrange(customer_count):
        dataset.append({
            'cust_key' : i+1,
            'nation_ref' : randint(1,nation_count)
        })

    write_to_file(dataset,'customers.adm')

    ### Part 3 : Generate Orders
    order_years = ['2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']
    order_count = args.orders
    dataset = []
    for i in xrange(order_count):
        dataset.append({
            'order_key' : i+1,
            'cust_ref' : randint(1,customer_count),
            'order_year' : order_years[randint(0,14)],
            'total_price' : round(uniform(1,100),2)
        })
    
    write_to_file(dataset,'orders.adm')

    print 'Dataset of %d nations created...' % nation_count
    print 'Dataset of %d customers created...' % customer_count
    print 'Dataset of %d orders created...' % order_count

if __name__ == "__main__":
    generate_dataset()
