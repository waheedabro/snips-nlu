# coding=utf-8
from pynini import SymbolTable, transducer, string_map, replace, compose, \
    acceptor

input_sym_table = SymbolTable()
input_sym_table.add_symbol("<eps>")

cities_symbols = ["paris", "Berlin", "London", "San Francisco"]
cities = [(city, "<eps>") for city in cities_symbols]

other_words = ["Find", "me", "a", "flight", "from", "to"]
slot_names = ["START_LOCATION", "END_LOCATION"]
symbols = other_words + cities_symbols + slot_names

for sym in symbols:
    for chunk in sym.split():
        input_sym_table.add_symbol(chunk)

tag_sym_table = SymbolTable()
tag_sym_table.add_symbol("<eps>")

slots = ("O", "START_LOCATION", "END_LOCATION", "bookFlight")
for slot in slots:
    tag_sym_table.add_symbol(slot)

city_fst = string_map(cities, input_token_type=input_sym_table,
                      output_token_type=input_sym_table).optimize()

pattern_fst = transducer(
    "Find me a flight from START_LOCATION to END_LOCATION",
    "O O O O O START_LOCATION O END_LOCATION bookFlight",
    input_token_type=input_sym_table,
    output_token_type=tag_sym_table)

final_fst = replace(pattern_fst, START_LOCATION=city_fst,
                    END_LOCATION=city_fst, call_arc_labeling="output")
final_fst = final_fst.optimize()

final_fst.draw("fst.dot")

composed_fst = compose(acceptor("Find me a flight from paris to San Francisco",
                                token_type=input_sym_table),
                       final_fst)
