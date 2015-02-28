# pylibcreator

A script that initializes a library structure for you, including setting up a repository on github.

## Requirements

* Need to have the [requests](http://docs.python-requests.org/en/latest/) library installed: `pip install requests`.

## Usage

```
pylibcreator.py --path /path/to/foo_lib --token <github_personal_token>
```

`github_personal_token` can be setup via your [github account](https://github.com/blog/1509-personal-api-tokens) to give the script access to the github API on your behalf. 

Once you run it, the script does the following tasks for you:
1) Initializes a new private git repository for foo_lib on github and clones that to /path/to/foo_lib
2) Sets up package and tests directories 
3) Sets up a setup.py file with initial contents
