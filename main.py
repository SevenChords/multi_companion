import sqlite3


def main_menu():
  global connection
  while True:
    print('\n\n\nMain Menu:\n'
          '[0] Four Kings\n'
          '[1] BTD6\n'
          '[.] Quit')
    user_input = input()
    if user_input == '0':
      four_kings()
    if user_input == '1':
      btd6()
    if user_input == '.':
      connection.close()
      exit(0)


def fk_view_slots():
  global cursor
  print('\n\n\nView Slot Stats:\n'
        '[0] Big Top Slots\n'
        '[1] Crazy 8 Slots\n'
        '[2] Fish N Chips\n'
        '[3] Gold Rush\n'
        '[4] Millionaire Manor\n'
        '[5] Seasonal Slots\n'
        '[6] Slots in Space\n'
        '[7] Spinning Cogs\n'
        '[8] Treasure Trap\n'
        '[9] Winds of Fortune\n'
        '[.] Return to Four Kings Menu')
  user_input = input()
  if user_input == '0':
    pass
  if user_input == '1':
    pass
  if user_input == '2':
    pass
  if user_input == '3':
    pass
  if user_input == '4':
    pass
  if user_input == '5':
    pass
  if user_input == '6':
    pass
  if user_input == '7':
    pass
  if user_input == '8':
    pass
  if user_input == '9':
    pass
  if user_input == '.':
    return


def fk_record_slots():
  pass


def four_kings():
  while True:
    print('\n\n\nFour Kings Companion:\n'
          '[0] View Stats for Slots\n'
          '[1] View Stats for Table Games\n'
          '[2] View Stats for Machine Games\n'
          '[3] Record Stats for Slots\n'
          '[4] Record Stats for Table Games\n'
          '[5] Record Stats for Machine Games\n'
          '[.] Return to Main Menu')
    user_input = input()
    if user_input == '0':
      fk_view_slots()
    if user_input == '1':
      pass
      # fk_view_tables()
    if user_input == '2':
      pass
      # fk_view_machines()
    if user_input == '3':
      fk_record_slots()
    if user_input == '4':
      pass
      # fk_record_tables()
    if user_input == '5':
      pass
      # fk_record_machines()
    if user_input == '.':
      return


def btd6():
  pass


def init():
  global connection, cursor
  connection = sqlite3.connect('tracked_stats.db')
  cursor = connection.cursor()
  cursor.execute('CREATE TABLE IF NOT EXISTS fk_slots(name, lines, spins, bonus, wagered, returned)')
  return


if __name__ == '__main__':
  connection = ''
  cursor = ''
  init()
  main_menu()
