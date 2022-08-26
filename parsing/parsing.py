import re
from parsing.instructions import *
from parsing.utils import *


def parse_headers(f):
    # Parsing header of ELF file using regex
    data = f.read()
    parsed_data = re.findall(
        '([0-9a-f]{8}) ([lgu!]) +([wCWIidDFfO]*) +\.text\t([0-9a-f]{8}) (.*)', data)
    symbols_table = {}
    for symbol in parsed_data:
        symbols_table[symbol[0]] = demangle(symbol[4])
    return symbols_table


def parse_logs():
    # Parse logs in out.log using regex
    inst_count = {}
    inst_time = {}
    call_stack = []
    entry_time = []
    parent_stack = []
    function_length = {}
    with open('disass.log', "r") as fp:
        data = fp.read()
        parsed_data = data.split('\n\n')
        for function_trace in parsed_data:
            lines = function_trace.split('\n')
            func_address = lines[0].split(' ')[0]
            func_trace_length = len(lines[1:])
            function_length[func_address] = func_trace_length
        # print(function_length)
    with open('headers.log', "r") as f:
        symtable = parse_headers(f)
        function_instructions = initialize_function_instructions(symtable)
        function_self_time = initialize_function_table(symtable)
        function_total_time = initialize_function_table(symtable)
        function_calls = initialize_function_table(symtable)
        function_calls_by_address = {}
        with open('out.log', 'r') as logfile:
            data = logfile.read()
            parsed_data = re.findall(
                '  (\d+\.\d{3}) \((\d+\.\d{3})\): C(\d+): ([a-zA-Z ]+):? ?(.*)\n', data)
            entry = True
            for cycle in parsed_data:
                time = float(cycle[0])
                timedelta = float(cycle[1])
                if cycle[3] == 'pc':
                    inst_data = re.findall(
                        '([0-9a-f]+) ([a-zA-Z]+): ?(.*)', cycle[4])
                    if inst_data[0][1] == 'Decode':
                        # This is where we update our instruction counters.
                        if entry:
                            call_stack.append(
                                demangle(symtable[inst_data[0][0]]))
                            entry_time = time
                            entry = False
                        params = re.findall(
                            '([A-Z]+) r(\d+)=0x([0-9a-f]+), r(\d+)=0x([0-9a-f]+), imm=0x([0-9a-f]+)', inst_data[0][2])
                        inst_count[params[0][0]] = inst_count.get(
                            params[0][0], 0) + 1
                        inst_time[params[0][0]] = inst_time.get(params[0]
                                                                [0], 0) + timedelta
                        function_instructions[call_stack[-1]][params[0][0]] = function_instructions.get(
                            call_stack[-1], {}).get(params[0][0], 0) + 1
                        # Here is where we update the call stack. Originally, this was done by doing a bisection search for pc in the symtable
                        # at each clock cycle but it's must faster to update the call stack at each jump instruction.
                        # Jump instructions have to be categorized in a unique way since not all jump instructions behave in the same way.
                        # I classified five types of jump instructions. This could be totally wrong but it ended up working for my single
                        # test-case. I also wanted to start by only parsing Decode instructions. If I also started parsing Compute instructions,
                        # I don't think I would have had to resort to parsing jump instructions in this weird way.
                        # JALR:
                        # jump-link: Jumps to a function and links ra to pc+4.
                        # ret-type: returns from one function back to the parent. In this case, the call stack is popped back to the parent.
                        # jump-nolink: Jumps to a function but doesn't link ra to pc+4.
                        # JAL:
                        # disass-jal: Jumps to a function and links ra
                        # disass-j: Doesn't jump to a function and doesn't link ra to pc+4. (this case doesn't update the call stack)
                        if params[0][0] == 'JALR':
                            reg = int(params[0][1])
                            r1 = int(params[0][2], base=16)
                            imm = int(params[0][5], base=16)
                            imm = twos_comp(imm)
                            cur_symbol = demangle(call_stack[-1])
                            if reg == 1:
                                if '{:08x}'.format(r1+imm) in symtable:
                                    # jump-link
                                    next_address = '{:08x}'.format(r1+imm)
                                    next_symbol = demangle(
                                        symtable[next_address])
                                    parent_stack.append(cur_symbol)
                                    call_stack.append(next_symbol)
                                    function_self_time[cur_symbol] += time - \
                                        entry_time
                                    function_total_time = update_function_total_time(
                                        function_total_time, time - entry_time)
                                    function_calls[next_symbol] += 1
                                    function_calls_by_address[next_address] = function_calls_by_address.get(
                                        next_address, 0) + 1
                                    entry_time = time
                                else:
                                    # ret-type
                                    idx = call_stack.index(parent_stack[-1])
                                    call_stack = call_stack[:idx+1]
                                    parent_stack.pop()
                                    function_self_time[cur_symbol] += time - \
                                        entry_time
                                    function_total_time = update_function_total_time(
                                        function_total_time, time - entry_time)
                                    entry_time = time
                            else:
                                # jump-nolink
                                next_address = '{:08x}'.format(r1+imm)
                                next_symbol = demangle(
                                    symtable[next_address])
                                call_stack.append(next_symbol)
                                function_self_time[cur_symbol] += time - \
                                    entry_time
                                function_total_time = update_function_total_time(
                                    function_total_time, time - entry_time)
                                function_calls[next_symbol] += 1
                                function_calls_by_address[next_address] = function_calls_by_address.get(
                                    next_address, 0) + 1
                                entry_time = time
                        elif params[0][0] == 'JAL':
                            pc = int(inst_data[0][0], base=16)
                            imm = int(params[0][5], base=16)
                            imm = twos_comp(imm)
                            cur_symbol = demangle(call_stack[-1])
                            if '{:08x}'.format(pc+imm) in symtable:
                                # disass-jal
                                next_address = '{:08x}'.format(pc+imm)
                                next_symbol = demangle(
                                    symtable[next_address])
                                parent_stack.append(cur_symbol)
                                call_stack.append(next_symbol)
                                function_self_time[cur_symbol] += time - \
                                    entry_time
                                function_total_time = update_function_total_time(
                                    function_total_time, time - entry_time)
                                function_calls[next_symbol]
                                function_calls_by_address[next_address] = function_calls_by_address.get(
                                    next_address, 0) + 1
                                entry_time = time
    results = []
    for (address, number_of_calls) in function_calls_by_address.items():
        if address not in function_length:
            print(address, 'not found')
        else:
            m = number_of_calls * function_length[address]
            results.append((address, m))
    print("total trace is", sum(val[1] for val in results))
    print(sorted(results, key=lambda y: y[1], reverse=True))
