from colorama import Fore, Style
import crawler

def main():

  path              = input(Fore.CYAN + '[*]' + Fore.WHITE + ' Enter Zip Path: ')
  current_td        = input(Fore.CYAN + '[*]' + Fore.WHITE + ' Enter Current Text Domain: ')
  new_td            = input(Fore.CYAN + '[*]' + Fore.WHITE + ' New Text Domain: ')
  translateFunction = input(Fore.CYAN + '[*]' + Fore.WHITE + ' Enter Translate Function Name: ' + Style.RESET_ALL)

  game = crawler.LaunchCrawler(path, translateFunction)
  game.unzip_file()
  game.start(current_td, new_td)
  game.zip_file()

if __name__ == '__main__':
  main()