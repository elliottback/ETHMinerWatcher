# ETHMinerWatcher

This software will launch and monitor your Etherium (ETH) Miner and restart it if it runs into trouble.  It will also managed your overclock settings and disable overclocking until DAG is constructed.

# Configuration & Runtime

## Config.yaml

Ensure your paths and arguments are correct in `config.yaml`.

## Admin

You must run this as admin, or MSI Afterburner launch will produce UAC prompts

## Afterburner

Ensure that you have a normal profile, and a mining profile, and set them in `config.yml`.  For example, with an NVidia RTX 3070, the following profiles work well:

Normal Profile:

![normal profile](img/profile1.png)

Mining Profile:

![mining profile](img/profile2.png)

And in the `config.yml`, we have:

```yml
afterburner:
  executable: 'C:\Program Files (x86)\MSI Afterburner\MSIAfterburner.exe'
  profile_normal: 'Profile1'
  profile_overclocked: 'Profile2'
```

# Requires

* [NSFMiner](https://github.com/no-fee-ethereum-mining/nsfminer) -- or other windows miner
* [MSI Afterburner](https://www.guru3d.com/files-details/msi-afterburner-beta-download.html) -- for overclock settings
* [Python](https://www.python.org/downloads/) - to run the watcher