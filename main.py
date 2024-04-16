import sqlite3
import random


def generate_menu(_title, _items, _returns, _last_page=1):
  if not _items:
    print('\n\n\nNothing to select.')
    _ = input()
    return None, None
  pages = int(len(_items) / 10) + 1
  if len(_items) % 10 == 0:
    pages -= 1
  current_page = _last_page
  if current_page > pages:
    current_page = pages
  while True:
    prev_page = False
    next_page = False
    cancel = False
    to_print = '\n\n\n' + _title + '\n'
    if current_page > 1:
      to_print = to_print + '[-] Previous page\n'
      prev_page = True
    if current_page == pages:
      for i in range(len(_items) % 10):
        to_print = to_print + '[' + str(i) + '] ' + _items[(current_page - 1) * 10 + i] + '\n'
      to_print = to_print + '[.] End Selection'
      cancel = True
    else:
      for i in range(10):
        to_print = to_print + '[' + str(i) + '] ' + _items[(current_page - 1) * 10 + i] + '\n'
      to_print = to_print + '[+] Next page\n'
      next_page = True
    print(to_print)
    user_input = input()
    if user_input == '.' or user_input == ',':
      return None, None
    if next_page and user_input == '+':
      current_page += 1
    if prev_page and user_input == '-':
      current_page -= 1
    if user_input in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
      return [_returns[(current_page - 1) * 10 + int(user_input)], current_page]


def main_menu():
  global connection
  while True:
    print('\n\n\nMain Menu:\n'
          '[0] Four Kings\n'
          '[1] BTD6\n'
          '[2] osu! resettable PP tracker\n'
          '[3] League\n'
          '[.] Quit')
    user_input = input()
    if user_input == '0':
      four_kings()
    if user_input == '1':
      btd6()
    if user_input == '2':
      osu()
    if user_input == '3':
      lol()
    if user_input == '.' or user_input == ',':
      connection.close()
      exit(0)


def lol_add_champs_to_position(_position):
  global connection, cursor
  champion_names = ['Aatrox', 'Ahri', 'Akali', 'Akshan', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Aphelios', 'Ashe',
                    'Aurelion Sol', 'Azir', 'Bard', "Bel'Veth", 'Blitzcrank', 'Brand', 'Braum', 'Briar', 'Caitlyn',
                    'Camille', 'Cassiopeia', "Cho'Gath", 'Corki', 'Darius', 'Diana', 'Draven', 'Dr. Mundo', 'Ekko',
                    'Elise', 'Evelynn', 'Ezreal', 'Fiddlesticks', 'Fiora', 'Fizz', 'Galio', 'Gangplank', 'Garen',
                    'Gnar', 'Gragas', 'Graves', 'Gwen', 'Hecarim', 'Heimerdinger', 'Hwei', 'Illaoi', 'Irelia', 'Ivern',
                    'Janna', 'Jarvan IV', 'Jax', 'Jayce', 'Jhin', 'Jinx', "Kai'Sa", 'Kalista', 'Karma', 'Karthus',
                    'Kassadin', 'Katarina', 'Kayle', 'Kayn', 'Kennen', "Kha'Zix", 'Kindred', 'Kled', "Kog'Maw",
                    "K'Sante", 'LeBlanc', 'Lee Sin', 'Leona', 'Lillia', 'Lissandra', 'Lucian', 'Lulu', 'Lux',
                    'Malphite', 'Malzahar', 'Maokai', 'Master Yi', 'Milio', 'Miss Fortune', 'Mordekaiser', 'Morgana',
                    'Naafiri', 'Nami', 'Nasus', 'Nautilus', 'Neeko', 'Nidalee', 'Nilah', 'Nocturne', 'Nunu & Willump',
                    'Olaf', 'Orianna', 'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Qiyana', 'Quinn', 'Rakan', 'Rammus',
                    "Rek'Sai", 'Rell', 'Renata Glasc', 'Renekton', 'Rengar', 'Riven', 'Rumble', 'Ryze', 'Samira',
                    'Sejuani', 'Senna', 'Seraphine', 'Sett', 'Shaco', 'Shen', 'Shyvana', 'Singed', 'Sion', 'Sivir',
                    'Skarner', 'Smolder', 'Sona', 'Soraka', 'Swain', 'Sylas', 'Syndra', 'Tahm Kench', 'Taliyah',
                    'Talon', 'Taric', 'Teemo', 'Thresh', 'Tristana', 'Trundle', 'Tryndamere', 'Twisted Fate', 'Twitch',
                    'Udyr', 'Urgot', 'Varus', 'Vayne', 'Veigar', "Vel'Koz", 'Vex', 'Vi', 'Viego', 'Viktor', 'Vladimir',
                    'Volibear', 'Warwick', 'Wukong', 'Xayah', 'Xerath', 'Xin Zhao', 'Yasuo', 'Yone', 'Yorick', 'Yuumi',
                    'Zac', 'Zed', 'Zeri', 'Ziggs', 'Zilean', 'Zoe', 'Zyra']
  table = 'lol_' + _position + '_champs'
  title = ''
  if _position == 'top':
    title = 'Toplane'
  if _position == 'jungle':
    title = 'Jungle'
  if _position == 'mid':
    title = 'Midlane'
  if _position == 'bot':
    title = 'Botlane'
  if _position == 'support':
    title = 'Support'
  already_added = cursor.execute('SELECT * FROM {}'.format(table))
  already_added = already_added.fetchall()
  for champ in already_added:
    champion_names.remove(champ[0])
  last_page = 1
  while True:
    to_add, last_page = generate_menu('Choose Champions to add to ' + title + ' Champion Pool:', champion_names,
                                      champion_names, last_page)
    if to_add is None:
      return
    cursor.execute('INSERT INTO {} VALUES(:name, 0, 0)'.format(table), {'name': to_add})
    connection.commit()
    champion_names.remove(to_add)


def lol_add_champions():
  while True:
    position = 'none'
    print('\n\n\nChoose Position to add to:\n'
          '[0] Toplane\n'
          '[1] Jungle\n'
          '[2] Midlane\n'
          '[3] Botlane\n'
          '[4] Support\n'
          '[.] Back to League of Legends Menu')
    user_input = input()
    if user_input == '.' or user_input == ',':
      return
    if user_input == '0':
      position = 'top'
    if user_input == '1':
      position = 'jungle'
    if user_input == '2':
      position = 'mid'
    if user_input == '3':
      position = 'bot'
    if user_input == '4':
      position = 'support'
    if position != 'none':
      lol_add_champs_to_position(position)


def lol_position_select(_suggestion_basis):
  global cursor, connection
  while True:
    position_order = []
    positions = ['top', 'jungle', 'mid', 'bot', 'support']
    if _suggestion_basis == 'random':
      position_order = ['top', 'jungle', 'mid', 'bot', 'support']
      random.shuffle(position_order)
    else:
      position_stats = [(), (), (), (), ()]
      for i in range(5):
        position_stats[i] = cursor.execute('SELECT * FROM lol_positions WHERE lol_positions.position=:position',
                                           {'position': positions[i]})
        position_stats[i] = position_stats[i].fetchone()
        if position_stats[i] is None:
          position_stats[i] = [positions[i], 0, 0]
        else:
          position_stats[i] = [position_stats[i][0],
                               int(position_stats[i][1]),
                               int(position_stats[i][2])]
      position_winrates = [50, 50, 50, 50, 50]
      position_experience = [0, 0, 0, 0, 0]
      for i in range(5):
        if position_stats[i][2] > 0:
          position_winrates[i] = round((position_stats[i][1] / position_stats[i][2]) * 100, 2)
        position_experience[i] = position_stats[i][2]
      if _suggestion_basis == 'winrate':
        while position_winrates:
          max_winrate = -1
          index = 0
          max_index = 0
          for wr in position_winrates:
            if wr > max_winrate:
              max_index = index
              max_winrate = wr
            index += 1
          position_order.append(positions[max_index])
          position_winrates.pop(max_index)
          positions.pop(max_index)
      if _suggestion_basis == 'experience':
        while position_experience:
          least_experience = 999999999
          index = 0
          max_index = 0
          for exp in position_experience:
            if exp < least_experience:
              max_index = index
              least_experience = exp
            index += 1
          position_order.append(positions[max_index])
          position_experience.pop(max_index)
          positions.pop(max_index)
    position_names = []
    for position in position_order:
      if position == 'top':
        position_names.append('Toplane')
      if position == 'jungle':
        position_names.append('Jungle')
      if position == 'mid':
        position_names.append('Midlane')
      if position == 'bot':
        position_names.append('Botlane')
      if position == 'support':
        position_names.append('Support')
    position, _ = generate_menu('Select Position.\n'
                                'Positions are ordered by Pick Priority.', position_names, position_order)
    if position is None:
      return
    table = 'lol_' + position + '_champs'
    champ_table = cursor.execute('SELECT * FROM {}'.format(table))
    champ_table = champ_table.fetchall()
    champ_list = []
    for champ in champ_table:
      _c_name = champ[0]
      _c_winrate = 50
      _c_experience = champ[2]
      if _c_experience > 0:
        _c_winrate = round((champ[1]/champ[2]) * 100, 2)
      champ_list.append([_c_name, _c_winrate, _c_experience])
    champ_list_sorted = []
    number_of_picks = 20
    if len(champ_list) < 20:
      number_of_picks = len(champ_list)
    if _suggestion_basis == 'random':
      for champ in champ_list:
        champ_list_sorted.append(champ[0])
      random.shuffle(champ_list_sorted)
      while len(champ_list_sorted) > number_of_picks:
        champ_list_sorted.pop()
    if _suggestion_basis == 'winrate':
      for n_pick in range(number_of_picks):
        index = 0
        max_index = 0
        max_winrate = -1
        for champ in champ_list:
          if champ[1] > max_winrate:
            max_index = index
            max_winrate = champ[1]
          index += 1
        champ_list_sorted.append(champ_list.pop(max_index)[0])
    if _suggestion_basis == 'experience':
      for n_pick in range(number_of_picks):
        index = 0
        max_index = 0
        least_experience = 999999999
        for champ in champ_list:
          if champ[2] < least_experience:
            max_index = index
            least_experience = champ[2]
          index += 1
        champ_list_sorted.append(champ_list.pop(max_index)[0])
    position_name = ''
    if position == 'top':
      position_name = 'Toplane'
    if position == 'jungle':
      position_name = 'Jungle'
    if position == 'mid':
      position_name = 'Midlane'
    if position == 'bot':
      position_name = 'Botlane'
    if position == 'support':
      position_name = 'Support'
    champ, _ = generate_menu('Select Champ for ' + position_name + '.\n'
                             'Champions are ordered by Pick Priority.', champ_list_sorted, champ_list_sorted)
    if champ is None:
      return
    print('\n\n\nSelect Game Outcome for ' + champ + ' ' + position_name + '\n'
          '[0] Victory\n'
          '[1] Defeat\n'
          '[.] Cancel')
    user_input = input()
    if user_input == '.' or user_input == ',':
      return
    if user_input == '0' or user_input == '1':
      stats = cursor.execute('SELECT * FROM {} WHERE {}.champ=:champ'.format(table, table), {'champ': champ})
      stats = stats.fetchone()
      games_won = stats[1] + 1 - int(user_input)
      games_played = stats[2] + 1
      stats = (champ, games_won, games_played)
      cursor.execute('DELETE FROM {} WHERE champ=:champ'.format(table), {'champ': champ})
      cursor.execute('INSERT INTO {} VALUES(?, ?, ?)'.format(table), stats)
      connection.commit()
      position_stats = cursor.execute('SELECT * FROM lol_positions WHERE lol_positions.position=:position', {'position': position})
      position_stats = position_stats.fetchone()
      if position_stats is None:
        position_stats = (position, 0, 0)
      games_won = position_stats[1] + 1 - int(user_input)
      games_played = position_stats[2] + 1
      position_stats = (position, games_won, games_played)
      cursor.execute('DELETE FROM lol_positions WHERE lol_positions.position=:position', {'position': position})
      cursor.execute('INSERT INTO lol_positions VALUES(?, ?, ?)', position_stats)
      connection.commit()


def lol_manual_result_recording():
  global cursor, connection
  while True:
    lane_selected = False
    position = ''
    title = ''
    while not lane_selected:
      position = 'none'
      title = 'none'
      print('\n\n\nSelect Position:\n'
            '[0] Toplane\n'
            '[1] Jungle\n'
            '[2] Midlane\n'
            '[3] Botlane\n'
            '[4] Support\n'
            '[.] Cancel')
      user_input = input()
      if user_input == '.' or user_input == ',':
        return
      if user_input == '0':
        position = 'top'
        title = 'Toplane'
      if user_input == '1':
        position = 'jungle'
        title = 'Jungle'
      if user_input == '2':
        position = 'mid'
        title = 'Midlane'
      if user_input == '3':
        position = 'bot'
        title = 'Botlane'
      if user_input == '4':
        position = 'support'
        title = 'Support'
      if position != 'none':
        lane_selected = True
    table = 'lol_' + position + '_champs'
    champ_table = cursor.execute('SELECT * FROM {} ORDER BY {}.champ'.format(table, table))
    champ_table = champ_table.fetchall()
    champ_list = []
    for champ in champ_table:
      champ_list.append(champ[0])
    selected_champ, _ = generate_menu('Select Champ to record ' + title + ' game for:', champ_list, champ_list)
    if selected_champ is None:
      continue
    print('\n\n\nSelect Game Outcome for ' + selected_champ + ' ' + title + '\n'
          '[0] Victory\n'
          '[1] Defeat\n'
          '[.] Cancel')
    user_input = input()
    if user_input == '.' or user_input == ',':
      continue
    if user_input == '0' or user_input == '1':
      stats = cursor.execute('SELECT * FROM {} WHERE {}.champ=:champ'.format(table, table), {'champ': selected_champ})
      stats = stats.fetchone()
      games_won = stats[1] + 1 - int(user_input)
      games_played = stats[2] + 1
      stats = (selected_champ, games_won, games_played)
      cursor.execute('DELETE FROM {} WHERE {}.champ=:champ'.format(table, table), {'champ': selected_champ})
      cursor.execute('INSERT INTO {} VALUES(?, ?, ?)'.format(table), stats)
      connection.commit()
      position_stats = cursor.execute('SELECT * FROM lol_positions WHERE lol_positions.position=:position',
                                      {'position': position})
      position_stats = position_stats.fetchone()
      if position_stats is None:
        position_stats = (position, 0, 0)
      games_won = position_stats[1] + 1 - int(user_input)
      games_played = position_stats[2] + 1
      position_stats = (position, games_won, games_played)
      cursor.execute('DELETE FROM lol_positions WHERE lol_positions.position=:position', {'position': position})
      cursor.execute('INSERT INTO lol_positions VALUES(?, ?, ?)', position_stats)
      connection.commit()


def lol():
  while True:
    suggestion_basis = 'none'
    print('\n\n\nLeague of Legends Companion:\n'
          '[0] Suggestions based on best winrate\n'
          '[1] Suggestions based on least games played\n'
          '[2] Random suggestions\n'
          '[3] Add champions to selection\n'
          '[4] Manually add Results\n'
          '[.] Back to main menu')
    user_input = input()
    if user_input == '.' or user_input == ',':
      return
    if user_input == '3':
      lol_add_champions()
    if user_input == '4':
      lol_manual_result_recording()
    if user_input == '0':
      suggestion_basis = 'winrate'
    if user_input == '1':
      suggestion_basis = 'experience'
    if user_input == '2':
      suggestion_basis = 'random'
    if suggestion_basis != 'none':
      lol_position_select(suggestion_basis)


def osu():
  global cursor, connection
  scores = cursor.execute('SELECT * FROM osu_scores ORDER BY osu_scores.pp DESC')
  scores = list(scores.fetchall())
  for n in range(len(scores)):
    scores[n] = int(scores[n][0])
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
    if user_input == '...' or user_input == ',,,':
      return
    if user_input == '.' or user_input == ',':
      cursor.execute('DELETE FROM osu_scores')
      connection.commit()
      for score in scores:
        cursor.execute('INSERT INTO osu_scores VALUES(?)', (score,))
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
  cursor.execute('CREATE TABLE IF NOT EXISTS osu_scores(pp INT)')
  cursor.execute('CREATE TABLE IF NOT EXISTS lol_positions(position, wins, games_played)')
  cursor.execute('CREATE TABLE IF NOT EXISTS lol_top_champs(champ, wins, games_played)')
  cursor.execute('CREATE TABLE IF NOT EXISTS lol_jungle_champs(champ, wins, games_played)')
  cursor.execute('CREATE TABLE IF NOT EXISTS lol_mid_champs(champ, wins, games_played)')
  cursor.execute('CREATE TABLE IF NOT EXISTS lol_bot_champs(champ, wins, games_played)')
  cursor.execute('CREATE TABLE IF NOT EXISTS lol_support_champs(champ, wins, games_played)')
  return


if __name__ == '__main__':
  connection = ''
  cursor = ''
  init()
  main_menu()
