# SGR
A script for ripping full-quality Suicide Girls photosets.

## Installation
1) Make sure Google Chrome is installed
2) Make sure Python 3.6 or greater is installed
3) Install Selenium using PIP with `pip install -U selenium`
4) Clone the repo into the directory of your choosing. For future examples, we will use `C:\SGR` and `/var/SGR`
5) Create a new directory called "dependencies" (`C:\SGR\dependencies` or `/var/SGR/dependencies`)
6) Download the Chrome webdriver from http://chromedriver.chromium.org/ and place it into the dependencies directory (`C:\SGR\dependencies\chromedriver.exe` or `/var/SGR/dependencies/chromedriver`)
7) Download aria2 from https://aria2.github.io/ and extract the files (not the directories) in the archive into a new folder `dependencies/aria2` (`C:\SGR\dependencies\aria2\aria2c.exe` or `/var/SGR/dependencies/aria2/aria`; compilation may be necessary for non-Windows users)

## Usage
`cd` into your install directory and call `python main.py -h` for help

## Flags
`-d`, `--dir` - The parent directory into which photosets should be downloaded (dir/Suicide Girls/<girl>/<set>); defaults to the current working directory
`-p`, `--processes` - SGR uses Python's multiprocessing library for calling into aria2 for downloads, this flag sets the maximum number of processes it can spawn; defaults to 4
`-t [type]`, `--type [type]` - The type of content to ripping
    The following types are supported:
	1) `g` or `girl` - all photosets by the specified suicide girls
	2) `h` or `hopeful` - all photosets by the specified hopefuls
	3) `s` or `set` - the photosets at the URLs provided
	4) `ag` or `all_girls` - all photosets by all suicide girls who had a photoset in the chosen time period
	5) `ah` or `all_hopefuls` - all photosets by all hopefuls who had a photoset in the chosen time period
	6) `as`, `all_sotds`, or `all_sets_of_the_day` - all photosets by all suicide girls with a featured set of the day in the chosen time period
	7) `a` or `all` - all photosets in the chosen time period
`-i [time_period]`, `--in [time_period]` - The time period to filter search results to; defaults to `all`
    The following time periods are supported:
	1) `all` - all time
	2) `24hours` - the last 24 hours
	3) `7days` - the last week
	4) `1month` - the last month
	5) `3months` - the last 3 months
	6) `6months` - the last 6 months
	7) All years from 2001 to 2018 inclusive
`-n [name]`, `--name [name]` - The name(s) of girls to rip; only works for suicide girls and hopefuls; DO NOT MIX SUICIDE GIRLS AND HOPEFULS
`-u [url]`, `--url [url]` - The URL(s) of sets to rip

## Examples
```
python main.py -p 2 -t all_sotds -i 7days
```
Download all photosets from all suicide girls who had a set of the day in the past week into the current directory while using only 2 worker processes

```
python main.py -t ah
```
Download all photosets from all hopefuls with the default 4 worker processes

```
python main.py -p 8 -t g -n vandoll pulp
```
Download all photosets from the suicide girls Vandoll and Pulp using 8 worker processes

```
python main.py -t s -u https://www.suicidegirls.com/girls/vandoll/album/3735859/blue-morning/ https://www.suicidegirls.com/girls/vandoll/album/3665933/come-closer/
```
Download the photosets "Blue Morning" and "Come Closer" by Vandoll