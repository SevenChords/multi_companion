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


def fk_view_slots_fish():
  global cursor
  stats = cursor.execute('SELECT * FROM fk_slots WHERE fk_slots.name="Fish N Chips"')
  stats = stats.fetchone()
  if stats is None:
    print('\n\n\nFish N Chips has no recorded stats.')
  else:
    print('\n\n\nStats for Fish N Chips:\n'
          'Average Spins for a Bonus: ' + str(round(stats[3] / stats[2] + 1, 3)) + '\n'
          'Average Spins for a Big Win: ' + str(round(stats[4] / stats[2] + 1, 3)) + '\n'
          'Average RTP: ' + str(round(float(stats[6]) / float(stats[5]), 3)) + '\n'
          'Total Spins recorded: ' + str(stats[2]))
  _ = input()
  return


def fk_view_slots():
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
    fk_view_slots_fish()
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


def fk_record_slots_fish():
  global cursor, connection
  stats = cursor.execute('SELECT * FROM fk_slots WHERE fk_slots.name="Fish N Chips"')
  stats = stats.fetchone()
  if stats is None:
    stats = ("Fish N Chips", 0, 0, 0, 0, 0, 0)
  stats = [stats[0],
           int(stats[1]),
           int(stats[2]),
           int(stats[3]),
           int(stats[4]),
           int(stats[5]),
           int(stats[6])]
  bet = int(input('\n\n\nEnter bet for this recording session: '))
  print('Enter the return you got from a spin to record it.\n'
        'Empty input will be recorded as 0 return.\n'
        'A "+" before the input signifies a bonus that is recorded '
        'separate from the return from the spin that triggered the bonus\n'
        'A "-" before the input signifies a bonus that is recorded '
        'at the same time as the return from the spin that triggered the bonus.\n'
        'A single "." will store all recorded information and return to the Record Slot Stats menu.\n'
        'A "..." will return to the Record Slot Stats menu without storing information recorded this session.\n'
        'A * will undo the last entry.\n')
  can_undo = False
  undo_big_win = False
  undo_bonus = False
  undo_bonus_spin_correction = False
  undo_return = 0
  while True:
    if stats[2] != 0 and stats[5] != 0:
      print('\nCurrent Stats:\n'
            'Average Spins for a Bonus: ' + str(round(stats[3] / stats[2] + 1, 3)) + '\n'
            'Average Spins for a Big Win: ' + str(round(stats[4] / stats[2] + 1, 3)) + '\n'
            'Average RTP: ' + str(round(float(stats[6]) / float(stats[5]), 3)) + '\n'
            'Total Spins recorded: ' + str(stats[2]))
    user_input = input()
    if user_input == '...':
      return
    if user_input == '.':
      cursor.execute('DELETE FROM fk_slots WHERE fk_slots.name="Fish N Chips"')
      connection.commit()
      cursor.execute('INSERT INTO fk_slots VALUES(?, ?, ?, ?, ?, ?, ?)', stats)
      connection.commit()
      return
    if user_input == '*':
      if can_undo:
        if undo_big_win:
          stats[4] -= 1
          undo_big_win = False
        if undo_bonus:
          stats[3] -= 1
          undo_bonus = False
        if not undo_bonus_spin_correction:
          stats[2] -= 1
        undo_bonus_spin_correction = False
        stats[5] -= bet
        stats[6] -= undo_return
        can_undo = False
      else:
        print('Nothing to undo.')
      continue
    if user_input.startswith('+'):
      stats[3] += 1
      stats[2] -= 1
      undo_bonus = True
      undo_bonus_spin_correction = True
      user_input.strip('+')
    elif user_input.startswith('-'):
      stats[3] += 1
      undo_bonus = True
      user_input.strip('-')
    else:
      undo_bonus = False
      undo_bonus_spin_correction = False
    if user_input == '':
      user_return = 0
    else:
      user_return = int(user_input)
    stats[2] += 1
    stats[5] += bet
    stats[6] += user_return
    undo_return = user_return
    can_undo = True
    if user_return >= 4*bet and not undo_bonus:
      stats[4] += 1
      undo_big_win = True
    elif undo_big_win:
      undo_big_win = False


def fk_record_slots():
  print('\n\n\nRecord Slot Stats:\n'
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
    fk_record_slots_fish()
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
  cursor.execute('CREATE TABLE IF NOT EXISTS fk_slots(name, lines, spins, bonus, big_win, wagered, returned)')
  return


if __name__ == '__main__':
  connection = ''
  cursor = ''
  init()
  main_menu()
