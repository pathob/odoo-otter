Otter - The Odoo time tracker
=============================

[![PyPI version](https://badge.fury.io/py/odoo-otter.svg)](https://badge.fury.io/py/odoo-otter)
[![Latest Release](https://img.shields.io/badge/release-latest-brightgreen)](https://github.com/pathob/odoo-otter/releases/latest)
[![.github/workflows/ci.yaml](https://github.com/pathob/odoo-otter/actions/workflows/ci.yaml/badge.svg?event=push)](https://github.com/pathob/odoo-otter/actions/workflows/ci.yaml)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

Note: This project is still in an early development stage!

## Installation and upgrade

Installation and upgrade can simply be done with Pip:

```
pip install odoo-otter --upgrade
```

Alternatively, you can download one of the prebuilt standalone binaries from the [latest releases](https://github.com/pathob/odoo-otter/releases/latest) and put it into your system's path.

After installation or upgrade, check the installation with:

```
otter -v
```

## Usage

### Help

The help can be accesses with the following command:

```
otter -h
```

### Configure connection to Odoo

When using Otter for the first time, you need to configure the connection to Odoo and your Otter:

```
otter config
```

Follow the instructions on the screen.
Enter the Odoo URL, select a database from the list and select the number of recent projects you want to get displayed.
If all data was entered correctly, you can now login to Odoo.

### Login to Odoo

When using Otter for the first time or when your Odoo session expired, login to Odoo:

```
otter login
```

Follow the instructions on the screen; enter your username and your password.
If all data was entered correctly, you are logged in to Odoo and your session will stored locally (your password will not be stored!).

NOTE: Currently, the login is only valid for about a week.

### Logout from Odoo

Use the following command to logout from Odoo.
This will delete your locally stored session.

```
otter logout
```

### Sync from and to Odoo

Before you can start using Otter, you will need to sync the remote Odoo projects and tasks to the local Otter database:

```
otter sync
```

This is also the command to use whenever you want to sync your local time tracking records to Odoo.
By default, Otter will only sync the local records up to the last day ('yesterday').
This prevents you from accidentally syncing records that you are still going work on on the current work day.
Sometimes - for example at the end of a week or a month - you also want to sync your records of the current work day. This can be done by providing the `date` option with the value `TODAY` like this:

```
otter sync --date TODAY
```

### Tracking your work time

The strength of Otter is to switch between many project tasks throughout a work day without having to add a work description every time.
Otter will concatenate all work descriptions belonging to the same project task and the same work day when performing the sync to Odoo automatically.
And it will also automatically adjust the work time to 15 minutes blocks (note that very short tasks below 15 minutes might be dropped by that automatic adjustment).

To start working on a project task, just run the following command and follow the instructions.

```
otter start
```

While a project task is active, you can always add a description for your current work.

```
otter describe "[TICKET-123] Implement functionality and tests"
```

To see whether a project task is currently active, run the following command:

```
otter status
```

And to stop your work, just run:

```
otter stop
```

Sometimes you might forget to start or stop a task in time.
You can fix that by passing the `time` option to either the start or stop command with the following argument format:

* `"HH:MM"` (for current day)
* `"YYYY-MM-DD HH:MM"` (for a fixed date)

Example:

```
otter start --time "12:15"
```

In order to see the overall worktime for the current day, run:

```
otter show
```

You can also pass the `date` option with the following argument format:

* `"YYYY-MM-DD"`

Example:

```
otter show --date 2021-10-01
```
