# 5QLC Spoofer - Roblox | by 5qlc | Win11 | run as admin
import os, sys, random, shutil, subprocess, winreg, time

BANNER = r"""
 53 51 76 67
              .-')                        
            .(  OO)                       
.------.   (_)---\_)  ,--.       .-----.  
|   ___|   '  .-.  '  |  |.-')  '  .--./  
|  '--.   ,|  | |  |  |  | OO ) |  |('-.  
`---.  '.(_|  | |  |  |  |`-' |/_) |OO  ) 
.-   |  |  |  | |  | (|  '---.'||  |`-'|  
| `-'   /  '  '-'  '-.|      |(_'  '--'\  
 `----''    `-----'--'`------'   `-----'  

      5 Q L C   S P O O F E R
      -----------------------
           by 5qlc
"""

def require_admin():
    import ctypes
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("[-] Please relaunch as ADMINISTRATOR.")
        sys.exit(1)

def rand_id(n=16):
    return ''.join(random.choice("0123456789ABCDEF") for _ in range(n))

def spoof_guids():
    print("\n[*] Spoofing MachineGuid + HwProfileGuid...")
    new_guid = "{%s-%s-%s-%s-%s}" % (rand_id(8), rand_id(4), rand_id(4), rand_id(4), rand_id(12))
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Cryptography", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "MachineGuid", 0, winreg.REG_SZ, new_guid)
        winreg.CloseKey(key)
        print(f"[+] MachineGuid -> {new_guid}")
    except Exception as e:
        print(f"[-] MachineGuid failed: {e}")
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\IDConfigDB\Hardware Profiles\0001",
            0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "HwProfileGuid", 0, winreg.REG_SZ, new_guid)
        winreg.CloseKey(key)
        print(f"[+] HwProfileGuid -> {new_guid}")
    except Exception as e:
        print(f"[-] HwProfileGuid failed: {e}")
    time.sleep(1)

def clean_traces():
    print("\n[*] Cleaning Roblox traces...")
    paths = [
        os.path.expandvars(r"%LOCALAPPDATA%\Roblox\logs"),
        os.path.expandvars(r"%TEMP%\Roblox"),
    ]
    for p in paths:
        if os.path.isdir(p):
            try:
                shutil.rmtree(p)
                print(f"[+] Deleted: {p}")
            except Exception as e:
                print(f"[-] {p}: {e}")
        else:
            print(f"[-] Not found: {p}")
    subprocess.run(["taskkill", "/F", "/IM", "RobloxPlayerBeta.exe"],
        capture_output=True, check=False)
    subprocess.run(["taskkill", "/F", "/IM", "RobloxCrashHandler.exe"],
        capture_output=True, check=False)
    print("[+] Roblox processes killed.")
    time.sleep(1)

def flush_dns():
    print("\n[*] Flushing DNS...")
    subprocess.run(["ipconfig", "/flushdns"], capture_output=True, check=False)
    print("[+] DNS flushed.")
    time.sleep(1)

def full_spoof():
    spoof_guids()
    clean_traces()
    flush_dns()
    print("\n[+] FULL SPOOF DONE by 5qlc.")
    print("[!] REBOOT YOUR PC NOW, then launch your game.")

def menu():
    require_admin()
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(BANNER)
        print("  [1] Full Spoof (recommended)")
        print("  [2] Spoof HWID only")
        print("  [3] Clean traces only")
        print("  [4] Flush DNS only")
        print("  [0] Exit")
        print()
        choice = input("  5qlc > ").strip()
        if choice == "1":
            full_spoof()
        elif choice == "2":
            spoof_guids()
        elif choice == "3":
            clean_traces()
        elif choice == "4":
            flush_dns()
        elif choice == "0":
            print("\n  Bye. by 5qlc.\n")
            break
        else:
            print("\n[-] Invalid choice.")
        input("\n  Press ENTER to return to menu...")

if __name__ == "__main__":
    menu()
