# ETHMinerWatcher

This software will launch and monitor your Etherium (ETH) Miner and restart it if it runs into trouble.  It will also managed your overclock settings and disable overclocking until DAG is constructed.

# Configuration

Ensure your paths and arguments are correct in config.yaml.

# Requires

* [NSFMiner](https://github.com/no-fee-ethereum-mining/nsfminer) -- or other windows miner
* [MSI Afterburner](https://www.guru3d.com/files-details/msi-afterburner-beta-download.html) -- for overclock settings
* [Python](https://www.python.org/downloads/) - to run the watcher

# Admin

You must run this as admin, or MSI Afterburner launch will produce UAC prompts