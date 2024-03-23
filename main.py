import os

DATA_PATHS_ = ['data',
              'data/fk',
              'data/fk/slots',
              'data/fk/slots/888',
              'data/fk/slots/circus',
              'data/fk/slots/cogs',
              'data/fk/slots/fish',
              'data/fk/slots/ghost',
              'data/fk/slots/gold',
              'data/fk/slots/prog',
              'data/fk/slots/space',
              'data/fk/slots/trap',
              'data/fk/slots/winds',
              'data/fk/tables',
              'data/fk/tables/baccarat',
              'data/fk/tables/big6',
              'data/fk/tables/bingo',
              'data/fk/tables/blackjack',
              'data/fk/tables/craps',
              'data/fk/tables/poker',
              'data/fk/tables/roulette',
              'data/fk/tables/war',
              'data/fk/machines',
              'data/fk/machines/blackjack',
              'data/fk/machines/keno',
              'data/fk/machines/poker']


def main_menu():
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
      exit(0)


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
      fk_view_tables()
    if user_input == '2':
      fk_view_machines()
    if user_input == '3':
      fk_record_slots()
    if user_input == '4':
      fk_record_tables()
    if user_input == '5':
      fk_record_machines()
    if user_input == '.':
      return


def btd6():
  pass


def init():
  for path in DATA_PATHS_:
    if not os.path.exists(path):
      os.mkdir(path)
  return


if __name__ == '__main__':
  init()
  main_menu()
