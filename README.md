Compare The Spire
---
![screen_shot](/uploads/50110f05ae242e9296b24078fabf9ec2/screen_shot.png)

![autocomplete](/uploads/85f6142932285cb81b2ee8f0e916e58f/autocomplete.gif)

![show_all_matches](/uploads/076c58c4dd42a570faeffbe05d772f3c/show_all_matches.gif)

Compare The Spire is an easy to use program that weighs cards based on popularity from the website [Spirelogs](https://spirelogs.com).

## Features

* Sorts by popularity
* Partial word search such as 'acc' -> 'Accuracy'
* Auto-complete words by partially typing and then hitting tab
* Show all matches by partially typing the card then hitting tab twice
* Caches data for quick access, re-caches after 1 day
* Compare as many cards as you want!

## Dependencies

Only tested in Arch Linux, requires Python 3+

Required python packages:
* Requests
* BS4
* Colorama

## Installation

Download or clone
`download https://gitlab.com/burningsunrise/awake/-/archive/master/awake-master.zip`
or
`git clone https://gitlab.com/burningsunrise/awake.git`

`cd awake/`

`pip install -r requirements.txt`

`python awake.py OR ./awake.py`

## Issues

If there are any issues, or feature requests please add an issue to the repo.