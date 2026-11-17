# MONOCOTIL (web vulnerability scanner)

import sys
import requests


# ─────── color ───────
rs = "\033[0m"

rd = "\033[1;91m"
gr = "\033[1;92m"
yl = "\033[1;93m"
bl = "\033[1;94m"
mg = "\033[1;95m"
cy = "\033[1;96m"
wh = "\033[1;97m"


# ─────── banner func ───────
def banner(txt): return f"\033[1;90;47m{txt}{rs}"


# ─────── status marker ───────
syst = f"{wh}[{yl}SYS{wh}]{rs}"
info = f"{wh}[{bl}INF{wh}]{rs}"
errr = f"{wh}[{rd}ERR{wh}]{rs}"
desc = f"{wh}[{mg}DES{wh}]{rs}"

def mark(n): return f"{wh}⟨{rs}{n}{wh}⟩{rs}"



def rawHeader(respon):
  print(banner("  RAW HEADER" + " " * 64) + "\n")
  
  print(f"{info} {wh}response: {respon.status_code}\n")
  
  for hea, val in respon.headers.items():
    print(f"{wh}╰➤ {gr}{hea}{wh}: {val}")
    if hea.lower() == 'server':
      print(f"{wh}╰➤ {yl}Server-Version{wh}: {val}")



def secHeader(respon):
  print("\n\n" + banner("  SECURITY HEADERS" + " " * 58) + "\n")
  
  mainHeader = [
    "Content-Security-Policy",
    "X-Frame-Options",
    "Strict-Transport-Security",
    "X-Content-Type-Options",
  ]
  
  for name in mainHeader:
    if name in respon.headers:
      print(f"{info} {mark(gr + " ADA ")}    {desc} {cy}{name}{wh}: {respon.headers[name]}")
    else:
      print(f"{info} {mark("HILANG")}   {desc} {yl}{name}")



def clickJacking(respon):
  print("\n\n" + banner("  CLICK JACKING" + " " * 61) + "\n")
  
  xfo = respon.headers.get("X-Frame-Options")
  csp = respon.headers.get("Content-Security-Policy", "")

  frameAncestors = "frame-ancestors" in csp.lower()


  if not xfo and not frameAncestors:
    print(f"{info} {mark(rd + "VULNERABILITY")}   {desc} {wh}tidak ada X-Frame-Options maupun CSP frame-ancestors")
  else:
    if xfo:
      print(f"{info} {mark(gr + "SECURE")}   {desc} {wh}{xfo}")
    if frameAncestors:
      print(f"{info} {mark(gr + "SECURE")}")



def cookieFlags(respon):
  print("\n\n" + banner("  COOKIE FLAG" + " " * 63) + "\n")

  rawCookies = []
  
  try:
    rawCookies = respon.raw.headers.getlist("Set-Cookie")
  except AttributeError:
    rawCookies = []

  if not rawCookies:
    print(f"{info} Set-Cookie tidak ditemukan")
    return

  for cookie in rawCookies:
    nameCookie = cookie.split("=")[0]
    lowerCookie = cookie.lower()
    httpOnly = "httponly" in lowerCookie
    secure = "secure" in lowerCookie
    samSite = "samesite" in lowerCookie

    print(f"{wh}╰➤ {gr}Cookie{wh}: {nameCookie}")
    print(f"{wh}╰➤ {gr}HttpOnly{wh}: {'ADA' if httpOnly else 'TIDAK ADA'}")
    print(f"{wh}╰➤ {gr}Secure{wh}: {'ADA' if secure else 'TIDAK ADA'}")
    print(f"{wh}╰➤ {gr}SameSite{wh}: {'ADA' if samSite else 'TIDAK ADA'}")



def cors(urlTarget):
  print("\n\n" + banner("  CORS" + " " * 70) + "\n")
  
  fakeOrigin = "https://evil-test.com"

  try:
    respon = requests.get(urlTarget, headers={"Origin": fakeOrigin}, timeout=10)
  except requests.exceptions.RequestException as e:
    print(f"{errr} {wh}{urlTarget}: {rs}{e}")
    return

  originAcc = respon.headers.get("Access-Control-Allow-Origin")
  credenAcc = respon.headers.get("Access-Control-Allow-Credentials")

  if originAcc is None:
    print(f"{info} Access-Control-Allow-Origin tidak ditemukan")
    return

  print(f"{desc} {wh}Access-Control-Allow-Origin: {yl}{originAcc}")
  print(f"{desc} {wh}Access-Control-Allow-Credentials: {yl}{credenAcc}")

  if originAcc == fakeOrigin:
    if credenAcc == "true":
      print(f"{info} {mark(rd + "CRITICAL VULN")}   {desc} {wh}origin palsu di-reflect dan credentials diizinkan")
    else:
      print(f"{info} {mark(yl + "VULNERABILITY")}   {desc} {wh}origin palsu di-reflect (tanpa credentials)")
  elif originAcc == "*":
    print(f"{info} {mark(mg + "ATTENTION")}   {desc} {wh}wilcard (*) - dari origin manapun diizinkan")
  else:
    print(f"{info} {mark(gr + "SECURE")}   {desc} {wh}origin tidak di-reflect")



def checkHeader(urlTarget):
  try:
    respon = requests.get(urlTarget, timeout=5)
  except requests.exceptions.RequestException as e:
    print(f"\n{errr} {wh}{urlTarget}: {rs}{e}\n")
    return


  rawHeader(respon)
  secHeader(respon)
  clickJacking(respon)
  cookieFlags(respon)
  cors(urlTarget)


  print("\n")



def main():
  urlTarget = input("[?] URL TARGET: ")
  if not urlTarget:
    sys.exit()

  print()

  checkHeader(urlTarget)


if __name__ == "__main__":
  main()