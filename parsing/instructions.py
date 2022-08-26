def initialize_function_instructions(symtable):
    function_instructions = {}
    for symbol in symtable.keys():
        function_instructions[symtable[symbol]] = {}
    return function_instructions


def initialize_function_table(symtable):
    function_times = {}
    for symbol in symtable.keys():
        function_times[symtable[symbol]] = 0
    return function_times


def update_function_total_time(function_total_time, time):
    for func in set(function_total_time):
        function_total_time[func] += time
    return function_total_time
