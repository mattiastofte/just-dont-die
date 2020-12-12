def install(libary):
    if libary == "pygame":
        print("[info] installing pygame 2.0.0 ...")
        try:
            os.system("pip3 install pygame==2.0.0")
            print("[info] correct version of pygame was successfully installed")
        except:
            print("[error] failed to install correct version of pygame")
    else:
        pass

try:
    pygame_package_info = os.popen("pip3 show pygame").read()
    index = pygame_package_info.find("Version:")
    pygame_version = str(pygame_package_info[index+9:index+14])
except:
    pygame_version = "null"

if pygame_version == "2.0.0":
    print("[info] correct version of pygame detected.")
elif pygame_version == "null":
    print("[warning] pygame libary is missing")
    install("pygame")
else:
    print("[warning] pygame is outdated and an update is required.")
    install("pygame")