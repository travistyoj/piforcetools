#!/usr/bin/python2
# Written by Capane.us

import os, collections, signal, sys, subprocess
import triforcetools
from systemd import daemon
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from time import sleep

# First we define a dictionary of game names to filenames.  Keep in mind game names are displayed on a 16x2 LCD display,
# so some game names must be split with a newline or abbreviated to fit.  Feel free to change names to whatever
# you like.  At load time, files that don't exist will be purge from the dictionary, so no need to trim this.  
# If you have a ROM dump with a different filename, either rename the .bin file or change the config here. 

ips = ["192.168.1.2", "192.168.1.3", "192.168.1.4", "192.168.1.5"] # Add or remove as many endpoints as you want
rom_dir = "/roms/"  # Set absolute path of rom files ending with trailing /

         # Atomiswave Games
games = {"Knights of Valor\nSeven Spirits":    "kov7spirits.bin",
         "Dolphin Blue":                       "dol222.bin",
         "Fist of the\nNorth Star":            "FOTNS_Naomi2_Fixed.bin",
         # Naomi Games
         "18 Wheeler (STD)":                   "18_Wheeler_STD.bin",
         "18 Wheeler (DLX)":                   "18_Wheeler_DX.bin", 
         "Airline Pilot":                      "AirlinePilots.bin", 
         "Akatsuki Blitz\nkampf Auf Asche":    "Akatsuki_Bk_Ausf_Achse.bin",
         "Alien Front":                        "AlienFront.bin", 
         "Azumanga Daioh\nPuzzle Bobble":      "AzumangaDaiohPuzzleBobble_v3.bin", 
         "Border Down":                        "BorderDown_v3.bin",
         "Burning Casino":                     "BurningCasino_v3.bin",
         "Capcom vs. SNK\nM. Fight 2K":        "Capcom_vs_SNK_Millenium_Fight_2000.bin",
         "Capcom vs. SNK\nM. Fight 2K Pro":    "Capcom_vs_SNK_Millenium_Fight_2000_Pro.bin",
         "Capcom vs. SNK 2\nM. Fighting 2001": "Capcom_Vs_SNK_2_Millionaire_Fighting_2001.bin",
         "Chaos Field":                        "ChaosField_v3.bin",
         "Cleopatra\nFortune Plus":            "CleopatraFortunePlus_v6.bin",
         "Confidential\nMission":              "ConfidentialMission.bin", 
         "Cosmic Smash":                       "CosmicSmash.bin",
         "Crazy Taxi":                         "CrazyTaxi.bin",
         "Dead or Alive 2":                    "DeadOrAlive2.bin",
         "Dead or Alive 2\nMillenium":         "DeadOrAlive2Millenium.bin",
         "Death Crimson OX":                   "DeathCrimsonOX.bin",
         "Doki Doki Idol\nStar Seeker":        "DokiDokiIdolStarSeeker.bin",
         "Dynamite Deka Ex":                   "DynamiteDekaEx.bin",  
         "Giant Gram Zen.\nPro Wrestle 2":     "Giant_Gram_EPR-21820_PATCHED.bin",
         "Giant Gram 2K Zn\nPro Wrestle 3":    "Giant_Gram_2000.bin",
         "Gigawing 2":                         "GigaWing2.bin",
         "Guilty Gear XX":                     "GuiltyGearXX.bin",
         "Guilty Gear XX\nReload":             "GuiltyGearXXReload.bin",
         "Guilty Gear XX\nSlash":              "GuiltyGearXXSlash_v6.bin",
         "Guilty Gear XX\nAccent Core":        "GuiltyGearXXAccentCore_v6.bin",
         "Gunspike":                           "GunSpike.bin",
         "Heavy Metal\nGeomatrix":             "HeavyMetalGeomatrix.bin",
         "Ikaruga":                            "Ikaruga_v3.bin",
         "Illvelo":                            "Illvelo_v6.bin",
         "Jambo Safari":                       "Jambo_Safari.bin",
         "Jingy Storm\nThe Arcade":            "JingyStormTheArcade.bin",
         "Karous":                             "karous_v3.bin",
         "Kuru Kuru\nChameleon":               "KuruKuruChameleon_v3.bin",
         "La Keyboard xyu":                    "LaKeyboardxyu_v3.bin",
         "Lupin 3\nThe Shooting":              "Lupin3-TheShooting.bin",
         "Lupin\nThe Typing":                  "Lupin-TheTyping.bin",
         "Mamoru-kun wa\nNoro. Shimatta!":     "mamonorov6.bin",
         "Marvel vs.\nCapcom 2":               "MarvelVsCapcom2.bin",
         "Maze of the King":                   "TheMazeOfTheKings.bin",
         "Melty Blood\nActress Again NP":      "MeltyBloodActressAgain.bin",
         "Melty Blood\nActress Again":         "MeltyBloodActressAgain_v6.bin",
         "Melty Blood\nAct Cadenza [A]":       "MeltyBloodActCadenza(RevA).bin",
         "Melty Blood\nAct Cadenza [B]":       "MeltyBloodActCadenzaVerB_v3.bin",
         "Melty Blood\nAct Cadenza [B2]":      "MeltyBloodActCadenzaVerB2_v3.bin",
         "Mob Suit Gundam\nFed. Vs Zeon":      "MobileSuitGundam-FederationVsZeon.bin",
         "Mob Suit Gundam\nFed. Vs Zeon DX":   "MobileSuitGundam-FederationVsZeonDX.bin",
         "Monkey Ball":                        "MonkeyBall.bin",
         "Musapeys Choco\nMarker":             "MusapeysChocoMarker.bin",
         "Nomiso Kone Kone\nPuzzle Takoron":   "NoukonePuzzleTakoron.bin",
         "Power Stone":                        "Powerstone.bin",
         "Power Stone 2":                      "PowerStone2.bin",
         "Project Justice\nRival School 2":    "RivalSchools2-ProjectJustice.bin",
         "Psyvariar 2":                        "Psyvariar2_v6.bin",
         "Puyo Puyo Da":                       "Puyo_Puyo_Da_EPR-22206_PATCHED.bin",
         "Puyo Puyo Fever":                    "PuyoPuyoFever_v6.bin",
         "Quiz Keitai\nQ Mode":                "QuizKeitaiQMode.bin",
         "Radirgy":                            "Radirgy_v3.bin", 
         "Radirgy Noa":                        "RadirgyNoa_v6.bin",
         "Samba de Amigo":                     "Samba_De_Amigo_EPR-22966B_Patched.bin",
         "Sega \nMarine Fishing":              "Sega_Marine_Fishing_EPR-22221.bin",
         "Sega\nStrike Fighter":               "SegaStrikeFighter.bin",
         "Sega Tetris":                        "SegaTetris.bin",
         "Senko no Ronde":                     "senkov3.bin",
         "Senko no Ronde\nNew Ver":            "senkonewv6.bin",
         "Senko no Ronde\nSP":                 "SenkoNoRondeSP_v3.bin",
         "Shikigami\nno Shiro II":             "ShikigamiNoShiroII_v6.bin",
         "Shooting Love\n2007 - Exzeal":       "ShootingLove2007-Exzeal_v6.bin",
         "SlashOut":                           "Slashout.bin",
         "Spawn":                              "spawn.bin",
         "Spikers Battle":                     "SpikersBattle.bin",
         "Sports Jam":                         "SportsJam.bin",
         "Street Fighter\nZero 3 Upper":       "StreetFighterZero3Upper.bin",
         "Super Shanghai\n2005":               "SuperShanghai2005_v6.bin",
         "Super Shanghai\n2005 [A]":           "SuperShanghai2005VerA_v6.bin",
         "Tetris\nKiwamemichi":                "TetrisKiwamemichi_v6.bin",
         "Typing of\nthe Dead":                "TheTypingOfTheDead.bin",
         "Toy Fighter":                        "ToyFighter.bin",
         "Trigger Heart\nExelica":             "TriggerHeartExelica_v6.bin",
         "Trizeal":                            "Trizeal_v3.bin",
         "Under Defeat":                       "UnderDefeat_v3.bin",
         "Usagui Yamashiro\nMahjong Hen":      "Usagui-YamashiroMahjongHen_v3.bin",
         "Virtua Athlete":                     "VirtuaAthlete.bin",
         "Virtua Golf":                        "VirtuaGolf.bin",
         "Virtua NBA":                         "VirtuaNBA.bin",
         "Virtua Striker 2\nVer. 2000":        "VirtuaStriker2-2000.bin",
         "Virtua Tennis":                      "VirtuaTennis.bin",
         "Virtua Tennis 2":                    "VirtuaTennis2.bin",
         "Wave Runner GP":                     "WaveRunnerGP.bin",
         "World Series\nBaseball":             "WorldSeriesBaseball.bin",
         "WWF Royal Rumble":                   "WWF_Royal_Rumble.bin",
         "Zero Gunner 2":                      "ZeroGunner2.bin", 
         "Zombie Revenge":                     "ZombieRevenge.bin",
         # Naomi 2 Games
         "Beach Spikers":                      "BeachSpikers.bin",
         "Club Kart\nEuropean Session":        "ClubKartEuropeanSessionUnlocked.bin",
         "Initial D\nExport":                  "InitialDexp.bin",
         "Initial D \nJapanese":               "InitialDjap.bin",
         "Initial D 2\nExport":                "InitialD2exp.bin",
         "Initial D 2\nJapanese":              "InitialD2jap.bin",
         "Initial D 2\nJapanese [B]":          "InitialD2jap-revb.bin",
         "Initial D 3\nExport":                "Initial_D3_Export.bin",
         "King Of\nRoute 66":                  "KingOfRoute66.bin",
         "Virtua Fighter 4":                   "VirtuaFighter4.bin", 
         "Virtua Fighter 4\nVer. B":           "VirtuaFighter4_verb.bin",
         "Virtua Fighter 4\nVer. C":           "VirtuaFighter4_verc.bin",
         "Virtua Fighter 4\nEvo":              "VirtuaFighter4Evo.bin",
         "Virtua Fighter 4\nEvo Ver. B":       "VirtuaFighter4Evo_verb.bin",
         "Virtua Fighter 4\nFinal Tuned":      "VirtuaFighter4FinalTuned.bin",
         "Virtua Fighter 4\nFinal Tuned [A]":  "VirtuaFighter4FinalTuned_vera.bin",
         "Virtua Fighter 4\nFinal Tuned [B]":  "VirtuaFighter4FinalTuned_verb.bin",
         "Virtua Striker 3":                   "VirtuaStriker3.bin",
         # Chihiro Games
         "Crazy Taxi\nHigh Roller":            "CrazyTaxiHighRoller.bin",
         "Ghost Squad\n512M":                  "Ghost_Squad_Ver._A_512.bin",
         "Ghost Squad \n1GB":                  "Ghost_Squad_Ver._A_1GB.bin",
         "Gundam Battle\nOperating Sim.":      "Gundam_Battle_Operating_Simulator.bin",
         "Ollie King\n512MB":                  "Ollie_King_512.bin",
         "Ollie King\n1GB":                    "Ollie_King_1GB.bin",
         "Out Run 2\n512MB":                   "OR2_512.bin",
         "Out Run 2\n1GB":                     "OR2_1gb.bin",
         "Out Run 2\nBETA":                    "OR2BETA.bin",
         "Out Run 2 SP":                       "or2sp_1gb.bin",
         "Out Run 2\nSpec Tours 512MB":        "Outrun_2_Special_Tours_512.bin",
         "Out Run 2\nSpec Tours 1GB":          "Outrun_2_Special_Tours_1GB.bin",
         "Sega Golf Club\n2006 NT 512MB":      "Sega_Golf_Club_Version_2006_Next_Tours_Rev.A_512.bin.bin",
         "Sega Golf Club\n2006 NT 1GB":        "Sega_Golf_Club_Version_2006_Next_Tours_Rev.A_1GB.bin.bin",
         "The House Of\nThe Dead 3":           "The_House_Of_The_Dead_3_GDX-0001.bin",
         "Virtua Cop 3\n512MB":                "Virtua_Cop_3_512.bin",
         "Virtua Cop 3\n1GB":                  "Virtua_Cop_3_1GB.bin",
         "Wangan Midnight\nMax Tune (EXP)":    "Wangan_Midnight_Maximum_Tune_EXPORT_(GDX-0009B).bin.bin",
         "Wangan Midnight\nMax Tune 512MB":    "Wangan_Midnight_Maximum_Tune_EXP_512.bin.bin",
         "Wangan Midnight\nMax Tune 1GB":      "Wangan_Midnight_Maximum_Tune_EXP_1GB.bin.bin",
         "Wangan Midnight\nMax Tune 2 (JAP)":  "Wangan_Midnight_Maximum_Tune_2_JAP_(GDX-0015).bin.bin",
         "Wangan Midnight\nMax Tune 2 512MB":  "Wangan_Midnight_Maximum_Tune_2_JAP_512.bin.bin",
         "Wangan Midnight\nMax Tune 2 1GB":    "Wangan_Midnight_Maximum_Tune_2_JAP_1GB.bin.bin",
         "Wangan Midnight\nMax Tune 2B 512M":  "Wangan_Midnight_Maximum_Tune_2B_EXP_512.bin",
         "Wangan Midnight\nMax Tune 2B 1GB":   "Wangan_Midnight_Maximum_Tune_2B_EXP_1GB.bin",
         # Triforce Games
         "F-Zero AX":                          "FZeroAx.bin",
         "Mario Kart\nArcade GP":              "MarioKartGP.bin",
         "Mario Kart\nArcade GP 2":            "MarioKartGP2.bin",
         "Virtua Striker\n2002":               "vs2002e.bin",
         "Virtua Striker 4\nv2006":            "vs406.bin",
         "Virtua Striker 4\n2006 (Export)":    "Virtua_Striker_4_2006_Exp.bin"}
commands = ["Change Target", "Download Update", "Shutdown", "Restart", "Enable DHCP", "Enable Static", "Ping Netdimm"]

# Define a signal handler to turn off LCD before shutting down
def handler(signum = None, frame = None):
    lcd = Adafruit_CharLCDPlate()
    lcd.clear()
    lcd.stop()
    sys.exit(0)
signal.signal(signal.SIGTERM , handler)

# We are up, so tell systemd
daemon.notify("READY=1")

# Purge game dictionary of game files that can't be found
missing_games = []
for key, value in games.iteritems():
    if not os.path.isfile(rom_dir+value):
        missing_games.append(key)
for missing_game in missing_games:
    del games[missing_game]
if not os.path.isfile("netctl/ethernet-dhcp"):
    commands.remove("Enable DHCP")
if not os.path.isfile("netctl/ethernet-static"):
    commands.remove("Enable Static")

# Initialize LCD
pressedButtons = []
curr_ip = 0
lcd = Adafruit_CharLCDPlate()
lcd.begin(16, 2)
lcd.message(" Piforce Tools\n   Ver. 1.1")
sleep(2)
lcd.clear()
if len(games) is 0:
    lcd.clear()
    lcd.message("NO GAMES FOUND!")
    sleep(1)
    iterator  = iter(commands)
    selection = iterator.next()
    mode = "commands"    
else:
    iterator  = iter(collections.OrderedDict(sorted(games.items(), key=lambda t: t[0])))
    selection = iterator.next()
    mode = "games"
    lcd.message(selection)


while True:

    # Handle SELECT
    if lcd.buttonPressed(lcd.SELECT):
        if lcd.SELECT not in pressedButtons:
            pressedButtons.append(lcd.SELECT)
            if selection is "Shutdown":
                os.system("shutdown -h now")
            elif selection is "Restart":    
                os.system("shutdown -r now")
            elif selection is "Change Target":
                curr_ip += 1
                if curr_ip >= len(ips):
                    curr_ip = 0
                lcd.message("\n"+ips[curr_ip])
            elif selection is "Download Update":
                lcd.clear()
                lcd.message("Downloading...")
                lcd.setCursor(14, 0)
                lcd.ToggleBlink()
                try:
                    response = subprocess.check_output(["git", "pull"])
                except:
                    response = "Update Error:\nCheck Internet"
                if response.strip() == "Already up-to-date.":
                    message = "No Update Found"
                else:
                    message = response.strip()
                lcd.ToggleBlink()
                lcd.clear()
                lcd.message(message)
                sleep(2)
                lcd.clear()
                lcd.message(selection)
            elif selection is "Enable DHCP":
                os.system("cp netctl/ethernet-dhcp /etc/netctl/eth0")
                lcd.clear()                
                lcd.message("Enabled DHCP")
                sleep(1)
                lcd.clear()
                lcd.message(selection)
            elif selection is "Enable Static":
                os.system("cp netctl/ethernet-static /etc/netctl/eth0")
                lcd.clear()
                lcd.message("Enabled Static")
                sleep(1)
                lcd.clear()
                lcd.message(selection)
            elif selection is "Ping Netdimm":
                lcd.clear()
                lcd.message("Pinging\n"+ips[curr_ip])
                response = os.system("ping -c 1 "+ips[curr_ip])
                lcd.clear()
                if response == 0:
                    lcd.message("Netdimm is\nreachable!")
                else:
                    lcd.message("Netdimm is\nunreachable!")
                sleep(1)
                lcd.clear()
                lcd.message(selection)
            else:
                lcd.clear()
                lcd.message("Connecting...")

                try:
                    triforcetools.connect(ips[curr_ip], 10703)
                except:
                    lcd.clear()
                    lcd.message("Error:\nConnect Failed")
                    sleep(1)
                    lcd.clear()
                    lcd.message(selection)
                    continue

                lcd.clear()
                lcd.message("Sending...")
                lcd.setCursor(10, 0)
                lcd.ToggleBlink()

                triforcetools.HOST_SetMode(0, 1)
                triforcetools.SECURITY_SetKeycode("\x00" * 8)
                triforcetools.DIMM_UploadFile(rom_dir+games[selection])
                triforcetools.HOST_Restart()
                triforcetools.TIME_SetLimit(10*60*1000)
                triforcetools.disconnect()

                lcd.ToggleBlink()
                lcd.clear()
                lcd.message("Transfer\nComplete!")
                sleep(5)
                lcd.clear()
                lcd.message(selection)
    elif lcd.SELECT in pressedButtons:
        pressedButtons.remove(lcd.SELECT)

    # Handle LEFT
    if lcd.buttonPressed(lcd.LEFT):
        if lcd.LEFT not in pressedButtons and len(games) > 0:
            pressedButtons.append(lcd.LEFT)
            mode      = "games"
            iterator  = iter(collections.OrderedDict(sorted(games.items(), key=lambda t: t[0])))
            selection = iterator.next()
            previous  = None
            lcd.clear()
            lcd.message("Games")
            sleep(1)
            lcd.clear()
            lcd.message(selection)            
    elif lcd.LEFT in pressedButtons:
        pressedButtons.remove(lcd.LEFT)

    # Handle RIGHT
    if lcd.buttonPressed(lcd.RIGHT):
        if lcd.RIGHT not in pressedButtons:
            pressedButtons.append(lcd.RIGHT)
            mode      = "commands"
            iterator  = iter(commands)
            selection = iterator.next()
            previous  = None
            lcd.clear()
            lcd.message("Commands")
            sleep(1)
            lcd.clear()
            lcd.message(selection)
    elif lcd.RIGHT in pressedButtons:
        pressedButtons.remove(lcd.RIGHT)

    # Handle UP
    if lcd.buttonPressed(lcd.UP):
        if lcd.UP not in pressedButtons and previous != None:
            pressedButtons.append(lcd.UP)
            if mode is "games":
                iterator = iter(collections.OrderedDict(sorted(games.items(), key=lambda t: t[0])))
            else:
                iterator = iter(commands)
            needle = iterator.next()
            selection = previous
            previous = needle
            while selection != needle and selection != previous:
                previous = needle
                try:
                    needle = iterator.next()
                except StopIteration:
                    break
            lcd.clear()
            lcd.message(selection)                
    elif lcd.UP in pressedButtons:
        pressedButtons.remove(lcd.UP)

    # Handle DOWN
    if lcd.buttonPressed(lcd.DOWN):
        if lcd.DOWN not in pressedButtons:
            pressedButtons.append(lcd.DOWN)            
            previous = selection
            try:
                selection = iterator.next()
            except StopIteration:
                if mode is "games":
                    iterator = iter(collections.OrderedDict(sorted(games.items(), key=lambda t: t[0])))
                else:
                    iterator = iter(commands)
                selection = iterator.next()
            lcd.clear()
            lcd.message(selection)
    elif lcd.DOWN in pressedButtons:
        pressedButtons.remove(lcd.DOWN)
