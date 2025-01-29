import dataset
import datetime
from util import PrintBox, getName

log = PrintBox(title="DATABASE", border_style="green")
  

class Database:
  def __init__(self, table):
    self._connect = dataset.connect('sqlite:///database/database.db')
    self.db = self._connect[table]
  
  def insert(self, data):
    self.db.insert(data)
  
  def find(self, *_clause, **kwargs):
    return self.db.find(*_clause, **kwargs)
  
  def find_one(self, *arg, **kwarg):
    return self.db.find_one(*arg, **kwarg)
  
  def update(self, row, keys):
    self.db.update(row, keys)
  
  def upsert(self, row, keys):
    self.db.upsert(row, keys)


class Users(Database):
  def __init__(self):
    super().__init__('users')
  
  def _new(self, uid, name):
    self.upsert(dict(
      uid = uid,
      name = name,
      points = 0, # Points system
      money = 200, # Bank system
    ), ['uid'])
    log.border_style = 'green'
    log.message(f"New user - [yellow]{uid}[/yellow] | [yellow]{name}[/yellow]")
  
  def get(self, uid):
    user = self.find_one(uid=uid)
    return user
  def add(self, uid, name='Facebook User'):
    if not self.get(uid):
      if name == 'Facebook User':
        name = getName(uid)
      self._new(uid, name)

class User(Users):
  def __init__(self, uid):
    super().__init__()
    self.uid = str(uid)
    self.row = self.get(self.uid)
    if not self.row:
      self.add(self.uid)
      self.row = self.get(self.uid)
  
  @property
  def name(self) -> str:
    return self.row.get('name')
  
  @property
  def points(self) -> int:
    return self.row.get('points')
  
  @property
  def money(self) -> int:
    return self.row.get('money')
  
  """POINTS"""
  def addPoints(self, value: int|float) -> None:
    prev = self.points
    
    # check if value is float, and convert into integer
    if isinstance(value, float):
      value = int(value)
    
    # check if value is valid to add
    if value < 0:
      log.border_style = 'red'
      log.message("[bold red]POINTS[/bold red] Invalid value")
      raise ValueError("Invalid value, it must be integers or float")
      
    # check if value type is not integer
    if not isinstance(value, int):
      log.border_style = 'red'
      log.message("[bold red]POINTS[/bold red] Invalid value")
      raise ValueError("Invalid value, it must be integers or float")
    
    new = prev + value
    self.upsert(dict(uid=self.uid, points=new), ['uid'])
    return new
  
  """BANK"""
  def addMoney(self, amount:int):
    prev = self.money
    if not isinstance(amount, int):
      log.border_style = 'red'
      log.message("[bold red]BANK[/bold red] Invalid argument")
      return prev
    if amount <= 0:
      log.border_style = 'red'
      log.message("[bold red]BANK[/bold red]  Invalid amount of money")
      return prev
    self.upsert(dict(uid=self.uid,money=prev+amount), ['uid'])
    return prev + amount
  def subMoney(self, amount:int):
    prev = self.money
    if not isinstance(amount, int):
      log.border_style = 'red'
      log.message("[bold red]BANK[/bold red] Invalid argument")
      return prev
    if amount > prev:
      log.border_style = 'red'
      log.message(f"[bold red]BANK[/bold red] Current money is not enough to subtract by {amount}")
      return prev
    self.upsert(dict(uid=self.uid,money=prev-amount), ['uid'])
    return prev - amount