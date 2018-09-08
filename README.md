# sporum-archive
Some scripts I wrote to help me archive parts of the official [Spore forum](http://forum.spore.com/) in anticipation of its shutdown in late 2018/early 2019. They might also be useful if you're trying to archive other JForum forums with a similar structure.

## Dependencies

* Python 3
* `lxml` (`make_*_index.py` scripts only)
* `cssselect` (`make_*_index.py` scripts only)
* `requests`

## Structure

### `make_topics_index.py`
Iterates through all valid Sporum topic (thread) IDs, from oldest to newest, and assembles a TSV file (`topics.tsv`) containing a summary of every existing topic. Each row in this "topics index" file represents a single topic and has the following columns:

* `id` – the (positive integer) ID of this topic
* `op` – the username of the topic's original poster
* `page_count` – the number of pages in this topic (each page contains up to 15 messages)
* `category` – the name of the specific board/subforum in which this topic is located
* `title` – the title of this topic

The idea here is to produce a complete list of topics that can then be sorted by page count, filtered by category and original poster, searched by title, and so on to get a sense of which topics are most important to preserve. It seems unlikely that we'll be able to archive the entire forum before it goes down, so this kind of triage will likely be a necessary part of any successful archiving strategy.

This one takes quite a while to run to completion (over 24 hours of continuous runtime on my machine), which is no doubt exacerbated somewhat by the enforced 1-second wait after scraping each topic. However, with a shorter wait time, the server gets overwhelmed by the volume of requests pretty quickly, resulting in a much bigger slowdown before long.

### `make_profiles_index.py`
Iterates through the Sporum's member listing page by page and assembles a TSV file (`profiles.tsv`) containing a summary of every existing member profile. Each row in this "profiles index" file represents a single member profile and has the following columns:

* `id` – the (positive integer) ID of this profile
* `username` – this member's username
* `message_count` – the number of messages created by this member

### `archive_topics.py`
This will be a script that takes a list of topic IDs/URLs as input and automatically archives them in their entirety. This will probably use the Wayback Machine API to [make a snapshot](https://archive.readme.io/docs/creating-a-snapshot) of every page in the targeted topic; it might also download the pages to create a local backup. Automatic [archive.is](http://archive.is) submission (maybe using the [`archiveis`](https://github.com/pastpages/archiveis) library?) would be nice to have too, but the 70 uploads per day maximum that I've seen some people report they're hitting on the Spore Community Hub Discord might make this unreasonable to support in practice.

### `archive_profiles.py`
As with `archive_topics.py`, but will instead take a list of profile IDs/URLs as input and automatically archive all messages posted by this member. Should probably also archive the profile page itself and maybe even the thread listing page too, to keep as many direct links intact as possible.
