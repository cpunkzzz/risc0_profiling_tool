import rust_demangler

def twos_comp(val):
  if (val & (1 << (31))) != 0:
    val = val - (1 << 32)
  return val

def demangle(funcname):
  try: 
    return rust_demangler.demangle(funcname)
  except: 
    return funcname