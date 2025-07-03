from main import CSV, aggregate_parse_args, filter_parse_args

my_csv = CSV()
def test_filter_data_equal():
    data = [
        {'name': 'chiron', 'brand': 'bugatti', 'price': 1000000, 'rating': 5},
        {'name': 'lx570', 'brand': 'lexus', 'price': 20000, 'rating': 4.8}
    ]
    filtered_data = my_csv.filter_data(data, 'brand', 'bugatti')
    assert len(filtered_data) == 1
    assert filtered_data[0]['name'] == 'chiron'

def test_aggregate_equal():
    data = [
        {'price': 100},
        {'price': 200},
        {'price': 300}
    ] 
    result = my_csv.aggregate_data(data, 'price', 'avg')
    assert result == 200

def test_parse_filter_condition():
    condition = 'rating>4.7'
    assert filter_parse_args(condition) == ('rating', '>', '4.7')

def test_parse_aggregate_condition():
    condition = 'rating=avg'
    assert aggregate_parse_args(condition) == ('rating', 'avg')    