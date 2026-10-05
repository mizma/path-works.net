import os
from invoke import task

defaultTgt = "~/"
allItems = {
    "~/": [
        "zsh",
        "nvim",
        "tmux",
        "dotDesktop",
        "scripts",
        "kitty",
        "noctalia",
        "electron",
        "discord",
        "mpv",
        "mangohud",
        "es-de",
    ],
}

genPaths = [
    "~/scripts/upscaylWallpaper/work/Desktop/upscayl",
    "~/scripts/upscaylWallpaper/work/AI/upscayl",
    "~/.config/systemd/user",
    "~/.local/share/applications/",
]

def root_dir() -> str:
    """
    Returns the invoke root directory (aka the project root)
    so that tasks can use it and be directory agnostic
    """
    return os.path.dirname(__file__)

@task()
def initDir(c):
    """Initialize Required Directories"""
    for path in genPaths:
        try:
            os.makedirs(os.path.expanduser(path), exist_ok=True)
            print(f"creating {path}")
        except Exception as e:
            print(f"failed creating {path}: {e}")

@task()
def pusha(c):
    """Push to all remotes"""
    c.run("git push origin")
    c.run("git push github")


@task(pre=[initDir])
def stow(c, item, tgt=defaultTgt, adopt=False, dry=False, restow=False, verbose=0):
    """run stow against item to tgt path. (cwd is always project root)
    Args:
        item (String, required): the stow items directory path
        tgt (String, optional): target path to stow to (default to ~/)
        adopt (Bool, optional): set the --adopt flag
        dry (bool, optional): dry run
        restow (bool, optional): set the --restow flag
        verbose (Int, optional): set verbosity level up to 5 (default: 0)
    """
    os.chdir(root_dir())
    flags = "--dotfiles"
    flags += " --no-folding"
    if adopt:
        flags += " --adopt"
    if dry:
        flags += " --simulate"
    if restow:
        flags += " --restow"
    flags += f" -v {verbose}"

    cmd = f"stow {flags} -t {tgt} {item}"
    print(f"running: {cmd}")
    c.run(cmd)
    pass


@task(default=True, aliases=["all"], pre=[initDir])
def stowAll(c, adopt=False, dry=False, restow=False, verbose=0):
    """run stow against all items
    Args:
        adopt (Bool, optional): set the --adopt flag
        dry (bool, optional): dry run
        restow (bool, optional): set the --restow flag
        verbose (Int, optional): set verbosity level up to 5 (default: 0)
    """
    os.chdir(root_dir())
    print(f"allItems: {allItems}")
    for tgt in allItems:
        print(f"for {tgt}: {allItems[tgt]}")
        for item in allItems[tgt]:
            print(f"running {item}")
            stow(c, item, tgt, adopt, dry, restow, verbose)
    pass

@task(aliases=["resetsm"])
def resetSubmodule(c):
    """Reset Submodule"""
    os.chdir(root_dir())
    c.run("git submodule sync")
    c.run("git submodule foreach --recursive git reset --hard")
    c.run("git submodule update --init --recursive")

