def main_menu():
  while(True):
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
  while(True):
    print('\n\n\nFour Kings Companion:\n'
          '[0] View Stats for Slots\n'
          '[1] View Stats for Table Games\n'
          '[2] Record Stats for Slots\n'
          '[3] Record Stats for Table Games\n'
          '[.] Return to Main Menu')
    user_input = input()
    if user_input == '0':
      fk_view_slots()
    if user_input == '1':
      fk_view_tables()
    if user_input == '2':
      fk_record_slots()
    if user_input == '3':
      fk_record_tables()
    if user_input == '.':
      return


def btd6():
  pass


if __name__ == '__main__':
  main_menu()
