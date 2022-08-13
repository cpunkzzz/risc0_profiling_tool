def initialize_instruction_table():
  return {
    'ADD': 0 ,
    'SUB': 0 ,
    'XOR': 0 ,
    'OR': 0 ,
    'AND': 0 ,
    'SLT': 0 ,
    'SLTU': 0 ,
    'ADDI': 0 ,
    'ORI': 0 ,
    'ANDI': 0 ,
    'XORI': 0 ,
    'SLTIU': 0 ,
    'SLLI': 0 ,
    'SRLI': 0 ,
    'LB': 0 ,
    'LH': 0 ,
    'LW': 0 ,
    'SW': 0,
    'LBU': 0 ,
    'LHU': 0 ,
    'SB': 0 ,
    'SH': 0 ,
    'BEQ': 0 ,
    'BLE': 0 ,
    'BLT': 0 ,
    'BGE': 0 ,
    'BNE': 0 ,
    'BLTU': 0 ,
    'BGEU': 0 ,
    'JAL': 0 , 
    'JALR': 0 ,
    'LUI': 0 ,
    'AUIPC': 0 ,
    'MUL': 0 ,
    'MULU': 0 ,
    'HALT': 0
  }

def initialize_function_instructions(symtable):
  function_instructions = {}
  for symbol in symtable.keys():
    function_instructions[symtable[symbol]] = initialize_instruction_table()
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