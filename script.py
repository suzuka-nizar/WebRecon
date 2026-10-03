import requests
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import pyfiglet

header = pyfiglet.figlet_format("DiverDiving",font="standard", width=80)
print(f"\033[36m{header}")

def cek_header(url):
  
  try:
    # mengirim request http get
    respon = requests.get(url, timeout=5)
    print()
    print(f"\033[34m[+] Status code:  {respon.status_code}")
    print("{HTTP HEADER}")
    # loop seluruh header yang dikirim server
    for header, value in respon.headers.items():
      print(f"\033[0m● \033[32m{header}: {value}")
      # kebocoran versi server
      if header.lower() == 'server':
        print(f"\033[0m● \033[33mserver version: {value}")

  except requests.exceptions.RequestException as e:
    print(f"\033[31m[-] error while connecting to {url}:  {e}")

def cek_satu_id(url_target, user_id, keywords):
  target = f"{url_target}{user_id}"

  try:
    respon = requests.get(target, timeout=5)
    found = [kw for kw in keywords if kw.lower() in respon.text.lower()]
    if respon.status_code == 200:
      pesan = f"[+] {target} Status code: 200 OK"
      if found:
        pesan += f"[+] Find keywords: {found}"
      print(f"\033[32m{pesan}\033[0m")
    elif found:
      print(f"\033[33m[-] {target} Status code: {respon.status_code}\033[0m\n\033[32m[+] Find keywords: {found}\033[0m")
  
  except requests.exceptions.RequestException as e:
    print(f"\033[31m[!] error while connecting to {target}: {e}\033[0m")
  
def tes_idor(url_target, id_start, id_end, keywords, max_workers=15):
  print()
  print(f"\033[34m[#] start IDOR parameter scan: {id_start} - {id_end}, {keywords}...")

  with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = [
      executor.submit(cek_satu_id, url_target, user_id, keywords)
      for user_id in range(id_start, id_end + 1)
    ]
    for _ in as_completed(futures):
      pass
    print("\033[34m[#] scanning is completed.")


def clear_screen():
  os.system('cls' if os.name == 'nt' else 'clear')

def main():
  while  True:
    print("  \033[36m[\033[97m1\033[36m] \033[33mHeader Inspect")
    print("  \033[36m[\033[97m2\033[36m] \033[33mIDOR")
    print()
    opsi = input("select an option: \033[0m")
    print("=" * 69)
    print()
  
    if not opsi:
      print("  \033[35m——Thank You——\033[0m")
      print()
      sys.exit()
    
    if opsi == "1":
      url_target = input("\033[35m[\033[97m*\033[35m] ENTER TARGET URL: \033[0m")
      if not url_target:
        sys.exit()
      print("\033[97m-" * 69)
      cek_header(url_target)
    
    elif opsi == "2":
      url_target = input("\033[35m[\033[97m*\033[35m] ENTER TARGET URL: \033[0m")
      first_id = input("\033[35m[\033[97m*\033[35m] FIRST ID PARAMETER: \033[0m")
      final_id = input("\033[35m[\033[97m*\033[35m] LAST ID PARAMETER: \033[0m")
      if not url_target or not first_id or not final_id:
        print()
        sys.exit()
      
      try:
        id_start = int(first_id)
        id_end = int(final_id)
      except ValueError:
        print(" \033[31mError: id parameter must be numeric.\033[0m")
        input(" \033[36m*press enter to return. \033[0m")
        print()
        print()
        continue

      if id_start > id_end:
        print(" \033[31mError: start id parameter exceeds end id parameter.\033[0m")
        input(" \033[36m*press enter to return. \033[0m")
        print()
        print()
        continue
        
      key_words = input("\033[35m[\033[97m*\033[35m] ENTER KEYWORDS: \033[0m").strip()
      keywords = [k.strip() for k in key_words.split(",") if k.strip()]
      print("\033[97m-" * 69)
      
      tes_idor(url_target, id_start, id_end, keywords)
    
    else:
      print("\033[31minvalid option: EXIT PROGRAM!\033[0m")
      sys.exit()

    print()
    home_quit = input(
      "\033[36m*type home to return to the menu"
      "\n*press enter to exit.\n~ "
    ).strip().lower()
    print("\033[97m=" * 69)
    print()
    print()
    if home_quit != "home":
      sys.exit()


if __name__ == "__main__":
  main()