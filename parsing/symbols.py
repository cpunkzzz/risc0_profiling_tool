from functools import total_ordering
from bisect import bisect_left

@total_ordering
class Symbol:
  def __init__(self, addr, name, next) -> None:
    if name.startswith(".hidden "):
      self.name = name[8:]
    else: 
      self.name = name
    self.addr = addr
    self.next = next

  def __eq__(self, addr) -> bool:
    return self.addr <= addr and self.next > addr

  def __gt__(self, other) -> bool:
    return self.addr > other
 
  def __repr__(self) -> str:
    return f"{self.name}: {self.addr} to {self.next}"
