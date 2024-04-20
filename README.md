# CS2 Lobby Share

### TLDR: This script automates the process of initiating the GamersClub anti-cheater, launching Counter-Strike, setting up a game lobby, and sharing the lobby link with friends.

Counter-Strike, a beloved first-person shooter game, becomes even more thrilling when played among friends. Yet, the presence of cheaters, using unauthorized hacks for advantages like seeing through walls and perfect aiming, can spoil the fun.

To address this, we turn to private servers (such as Gamers Club, though others like FaceIt are also viable). These servers come with advanced, intrusive anti-cheat software, ensuring game integrity and a fair competitive environment for all players.

The process of setting up a lobby on these servers requires following a set of specific, orderly actions. This script automates these steps, along with additional custom actions tailored to meet my unique gaming preferences, enhancing the pre-game experience.

Incorporating this script into your setup involves initial adjustments. You'll need to modify it according to your particular gaming environment and requirements.

## Actions executed by this script
just look the share_lobby() function on the main.py file. 
the actions are clearly summarized there.

# Running the Script

## Install the Required Software 
- Make sure you are on Windows (Gamers Club requirement)
- Install:
  - Gamers Club Anti Cheater (https://gamersclub.com.br/)
  - Counter-Strike (https://store.steampowered.com/app/730/CounterStrike_2/)
  - Mozilla Firefox (or adapt the script to work with another browser)
  - VoiceMeeter (or just comment out the prepared_voicemeeter() line on main.py)
  - a Unix like shell or environment, like git_bash  or msys2)
  - Python
  - pew (https://pypi.org/project/pew/)

## Setup GitHub Access Token
the script is configured to share the lobby link using Github Gist.
If you want to use it, you will need to setup a github access token, with access to Gists.
If you don't want to use this feature, just comment out the `share_with_friends()` function call on main.py

## Login on the necessary plataforms
Make sure you are alogged in on:
- Steam App
- Gamers Club Anti Cheater App
- Gamers Club website, on Firefox browser

## Setup the configuration files to your Computer
- Setup the environment variables:
  - copy `.env.sample` to `.env`
  - edit the `.env` file inserting your values
   - ignore the GITHUB values if you are not using them
- Setting up the applications directories
  - if your applications (like firefox and gamers club anticheater) are not in the same directory as mine:
    - edit `cfg/apps.py`

## Pre-Vetoing maps
Gamers Club allow its Plus and Premium users to pre-veto some maps before any match.
If you want to change the list of maps to pre-veto, just edit this file:
`cfg/vetos.py`


## Run the script
- launch your unix like shell on this project's folder
- `./run.sh run`

## Troubleshooting Virtual Environment
If your pew virtual environment gets to a problematic state, just run this command to set it up again:
`./run.sh venv_fix`

If you need to enter on the virtual environment, to install more packages, just do `./run.sh venv_enter`


# FAQ

### Why cliking around Gamers Club website, when some steps could be done by making API calls?
That's an improvement I might add in the future (probably not, time is short)

### Would be nice to have the ability to also share the Server IP (the connect command)
That's an improvement I might add in the future (probably not, time is short)

### Does it worth doing all this script crap? Shouldn't you be playing more CS instead?
I am a terrible Counter Strike player. At least writing an script, outside of the game, I experience some wins. And I enjoy writing it =)


