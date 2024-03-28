import sqlite3


def main_menu():
  global connection
  while True:
    print('\n\n\nMain Menu:\n'
          '[0] Four Kings\n'
          '[1] BTD6\n'
          '[2] osu! resettable PP tracker\n'
          '[.] Quit')
    user_input = input()
    if user_input == '0':
      four_kings()
    if user_input == '1':
      btd6()
    if user_input == '2':
      osu()
    if user_input == '.' or user_input == ',':
      connection.close()
      exit(0)


def osu():
  global cursor, connection
  scores = cursor.execute('SELECT * FROM osu_scores ORDER BY osu_scores.pp DESC')
  scores = scores.fetchall()
  if scores is None:
    scores = [0]
  print('\n\n\nEnter the PP you get from each Play you want to record.\n'
        'Enter "." to return to the Main Menu and store the PP values recorded this session.\n'
        'Enter "..." to return to the Main Menu without storing the PP values recorded this session.\n'
        'Enter "--" to reset all recorded PP values and return to the Main Menu. This cannot be undone.')
  while True:
    pp = 0
    for n in range(len(scores)):
      score_value = int(scores[n] * (0.95 ** n))
      if score_value == 0:
        scores.pop(n)
      pp += score_value
    print('\nCurrent PP: ' + str(pp))
    user_input = input()
    if user_input == '--':
      cursor.execute('DELETE FROM osu_scores')
      connection.commit()
      return
    if user_input == '.':
      return
    if user_input == '...':
      cursor.execute('DELETE FROM osu_scores')
      connection.commit()
      for score in scores:
        cursor.execute('INSERT INTO osu_scores VALUES(?)', score)
      connection.commit()
      return
    new_score = int(user_input)
    scores.append(new_score)
    scores.sort(reverse=True)


def fk_view_slot_stats(_slot=''):
  global cursor
  stats = cursor.execute('SELECT * FROM fk_slots WHERE fk_slots.name=:slot', {'slot': _slot})
  stats = stats.fetchone()
  if stats is None:
    print('\n\n\n' + _slot + ' has no recorded stats.')
  else:
    print_fk_slot_stats(stats, '\n\n\nStats for ' + _slot + ':\n')
  _ = input()
  return


def print_fk_slot_stats(_stats, _string_preface=''):
  to_print = _string_preface
  if _stats[3] != 0:
    to_print = (to_print + 'Average Spins to encounter a Bonus: ' +
                str(round(_stats[2] / _stats[3], 3)) + '\n')
  if _stats[4] != 0:
    to_print = (to_print + 'Average Spins to encounter a Big Win: ' +
                str(round(_stats[2] / _stats[4], 3)) + '\n')
  if _stats[5] != 0:
    to_print = (to_print + 'Average RTP: ' +
                str(round(_stats[6] / _stats[5] * 100, 2)) + '%\n')
  to_print = to_print + 'Total Spins recorded: ' + str(_stats[2])
  print(to_print)
  return


def choose_line_count(_choices, _slot):
  menu = '\n\n\nChoose line count:'
  for i in range(len(_choices)):
    menu = menu + '\n[' + str(i) + '] ' + str(_choices[i])
  menu = menu + '\n[.] Return to Slot Selection'
  print(menu)
  user_input = input()
  if user_input == '.' or user_input == ',':
    return None
  else:
    return _slot + ' ' + str(_choices[int(user_input)])


def fk_view_slots():
  while True:
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
      slot = choose_line_count([25, 50, 75, 100], 'Big Top Slots')
      if slot is None:
        continue
      fk_view_slot_stats(slot)
    if user_input == '1':
      slot = choose_line_count([8, 18, 28, 38, 88], 'Crazy 8 Slots')
      if slot is None:
        continue
      fk_view_slot_stats(slot)
    if user_input == '2':
      fk_view_slot_stats('Fish N Chips')
    if user_input == '3':
      slot = choose_line_count([25, 50, 75, 100], 'Gold Rush')
      if slot is None:
        continue
      fk_view_slot_stats(slot)
    if user_input == '4':
      slot = choose_line_count([5, 10, 15, 20, 25], 'Millionaire Manor')
      if slot is None:
        continue
      fk_view_slot_stats(slot)
    if user_input == '5':
      fk_view_slot_stats('Seasonal Slots')
    if user_input == '6':
      fk_view_slot_stats('Slots in Space')
    if user_input == '7':
      slot = choose_line_count([25, 50, 75, 100], 'Spinning Cogs')
      if slot is None:
        continue
      fk_view_slot_stats(slot)
    if user_input == '8':
      fk_view_slot_stats('Treasure Trap')
    if user_input == '9':
      slot = choose_line_count([25, 50, 75, 100], 'Winds of Fortune')
      if slot is None:
        continue
      fk_view_slot_stats(slot)
    if user_input == '.' or user_input == ',':
      return


def fk_record_slot_stats(_slot=''):
  global cursor, connection
  stats = cursor.execute('SELECT * FROM fk_slots WHERE fk_slots.name=:slot', {'slot': _slot})
  stats = stats.fetchone()
  if stats is None:
    stats = (_slot, 0, 0, 0, 0, 0, 0)
  stats = [stats[0],
           int(stats[1]),
           int(stats[2]),
           int(stats[3]),
           int(stats[4]),
           int(stats[5]),
           int(stats[6])]
  bet = int(input('\n\n\nEnter total bet for this recording session: '))
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
    if stats[2] != 0:
      print_fk_slot_stats(stats, '\nCurrent Stats:\n')
    user_input = input()
    if user_input == '...' or user_input == ',,,':
      return
    if user_input == '.' or user_input == ',':
      cursor.execute('DELETE FROM fk_slots WHERE fk_slots.name=:slot', {'slot': _slot})
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
      user_input = user_input.strip('+')
    elif user_input.startswith('-'):
      stats[3] += 1
      undo_bonus = True
      user_input = user_input.strip('-')
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
  while True:
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
      slot = choose_line_count([25, 50, 75, 100], 'Big Top Slots')
      if slot is None:
        continue
      fk_record_slot_stats(slot)
    if user_input == '1':
      slot = choose_line_count([8, 18, 28, 38, 88], 'Crazy 8 Slots')
      if slot is None:
        continue
      fk_record_slot_stats(slot)
    if user_input == '2':
      fk_record_slot_stats('Fish N Chips')
    if user_input == '3':
      slot = choose_line_count([25, 50, 75, 100], 'Gold Rush')
      if slot is None:
        continue
      fk_record_slot_stats(slot)
    if user_input == '4':
      slot = choose_line_count([5, 10, 15, 20, 25], 'Millionaire Manor')
      if slot is None:
        continue
      fk_record_slot_stats(slot)
    if user_input == '5':
      fk_record_slot_stats('Seasonal Slots')
    if user_input == '6':
      fk_record_slot_stats('Slots in Space')
    if user_input == '7':
      slot = choose_line_count([25, 50, 75, 100], 'Spinning Cogs')
      if slot is None:
        continue
      fk_record_slot_stats(slot)
    if user_input == '8':
      fk_record_slot_stats('Treasure Trap')
    if user_input == '9':
      slot = choose_line_count([25, 50, 75, 100], 'Winds of Fortune')
      if slot is None:
        continue
      fk_record_slot_stats(slot)
    if user_input == '.' or user_input == ',':
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
    if user_input == '.' or user_input == ',':
      return


def btd6():
  pass


def init():
  global connection, cursor
  connection = sqlite3.connect('tracked_stats.db')
  cursor = connection.cursor()
  cursor.execute('CREATE TABLE IF NOT EXISTS fk_slots(name, lines, spins, bonus, big_win, wagered, returned)')
  cursor.execute('CREATE TABLE IF NOT EXISTS osu_scores(pp)')
  return


if __name__ == '__main__':
  connection = ''
  cursor = ''
  init()
  main_menu()
