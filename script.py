import requests
import sys
import pyfiglet

header = pyfiglet.figlet_format("DiverDiving",font="standard", width=80)
print(f"\033[36m{header}")

def cek_header(url):
  respon = requests.get(url, timeout=5)
  # mengirim request http get
  try:
    print()
    print(f"\033[34m[+] Status code:  {respon.status_code}")
    print("{HTTP HEADER}")
    # loop seluruh header yang dikirim server
    for header, value in respon.headers.items():
      print(f"\033[32m•{header}:  {value}")
      # kebocoran versi server
      if header.lower() == 'server':
        print(f"\033[35m•server version:  {value}")

  except requests.exceptions.RequestException as e:
    print(f"\033[31m[-] error while connecting to {url}:  {e}")


def tes_idor(url_target, list_id):
  print()
  print("\033[34m[#] start IDOR parameter scan...")

  for user_id in list_id:
    target = f"{url_target}{user_id}"
    print(f"\033[32m[+] Endpoint testing: {target}")

    if user_id in ["admin", "root"]:
      print(f"\033[31m[!] Find sensitive endpoint•────⟨{user_id}⟩\033[0m")


def main():
  print("  \033[33m[1] Header Inspect")
  print("  [2] IDOR")
  print()
  opsi = input("select an option: ")
  print()
  print()
  
  if not opsi:
    sys.exit()
    
  if opsi == "1":
    url_target = input("[*] ENTER TARGET URL: ")
    if not url_target:
      sys.exit()
    cek_header(url_target)
    
  elif opsi == "2":
    url_target = input("[*] ENTER TARGET URL: ")
    list_id = input("[*] ENTER PARAMETER ID: ")
    if not url_target:
      sys.exit()
    list_id = [item.strip() for item in list_id.split(",")]  
    tes_idor(url_target, list_id)

  else:
    print("\033[31minvalid option: EXIT PROGRAM!\033[0m")


if __name__ == "__main__":
  main()