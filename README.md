# Auto Accept Invite

This script will accept all pending invites for a user.  This tool can be run with your personal access token or a service account.  You can find your token in the [general account settings](https://app.snyk.io/account?_gl=1*fa0v8*_gcl_au*MTIwNDU2NjMxMy4xNzI2NTI0OTgw*_ga*NDUxODc4NDg1LjE2OTA5MDQ2MDk.*_ga_X9SH3KP7B4*MTcyOTg4OTY0Ny43MDIuMS4xNzI5ODkwNzkzLjQ4LjAuMA..).

## Requirements

Python version 3.10.0

## Tool arguments

run the following to see options:

```bash
python3 index.py --help
```

## Script Arguments

[SNYK_GROUP_ID](https://docs.snyk.io/snyk-admin/groups-and-organizations/groups/group-general-settings)

## Running
```bash
export SNYK_TOKEN=TYPE-SNYK-TOKEN-HERE
pip install -r requirements.txt
python3 index.py SNYK_GROUP_ID
```
