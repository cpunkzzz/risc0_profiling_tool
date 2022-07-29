import re
from parsing.symbols import *

def parse_headers(f):
  data = f.read()
  parsed_data = re.findall('([0-9a-f]{8}) ([lgu!]) +([wCWIidDFfO]*) +\.text\t([0-9a-f]{8}) (.*)', data)
  symbols_table = {}
  for symbol in parsed_data:
    symbols_table[symbol[0]] = symbol[4]
  return symbols_table

def twos_comp(val):
  if (val & (1 << (31))) != 0:
    val = val - (1 << 32)
  return val

def parse_logs():
  inst_count = {
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
  inst_time = {
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
  function_count = {}
  function_self_time = {}
  function_total_time = {}
  with open('headers.log', "r") as f:      
    symtable = parse_headers(f)
    with open('out.log', 'r') as logfile:
      data = logfile.read()
      parsed_data = re.findall('  (\d+\.\d{3}) \((\d+\.\d{3})\): C(\d+): ([a-zA-Z ]+):? ?(.*)\n', data)
      call_stack = []
      parent_stack = []
      entry = True
      for cycle in parsed_data:
        if cycle[3] == 'pc': 
          inst_data = re.findall('([0-9a-f]+) ([a-zA-Z]+): ?(.*)', cycle[4])        
          if inst_data[0][1] == 'Decode':
            if entry:
              call_stack.append(symtable[inst_data[0][0]])
              entry = False
            params = re.findall('([A-Z]+) r(\d+)=0x([0-9a-f]+), r(\d+)=0x([0-9a-f]+), imm=0x([0-9a-f]+)', inst_data[0][2])
            inst_count[params[0][0]] += 1
            inst_time[params[0][0]] += float(cycle[1])
            if params[0][0] == 'JALR':
              reg = int(params[0][1])
              r1 = int(params[0][2], base=16)
              imm = int(params[0][5], base=16)
              imm = twos_comp(imm)
              if reg == 1: 
                if'{:08x}'.format(r1+imm) in symtable:
                  parent_stack.append(call_stack[-1])
                  call_stack.append(symtable['{:08x}'.format(r1+imm)])
                else: 
                  idx = call_stack.index(parent_stack[-1])
                  call_stack = call_stack[:idx+1]
                  parent_stack.pop()
              else:
                call_stack.append(symtable['{:08x}'.format(r1+imm)])
            elif params[0][0] == 'JAL':
              pc = int(inst_data[0][0], base=16)
              imm = int(params[0][5], base=16)
              imm = twos_comp(imm)
              if '{:08x}'.format(pc+imm) in symtable:
                parent_stack.append(call_stack[-1])
                call_stack.append(symtable['{:08x}'.format(pc+imm)])
            print(call_stack)
      print(inst_count, inst_time)  
