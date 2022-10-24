# NI-VMM audio classification



## Getting started

To clone the GitLab repository, execute these commands:

```
cd existing_repo
git remote add origin https://gitlab.fit.cvut.cz/sirmart2/ni-vmm-audio-classification.git
git branch -M master
git push -uf origin master
```

Requirements for Flask:

- Python 3.7 and higher

Flask installation:
```
cd server
. venv/bin/activate
pip install Flask (nebo pip3)
```
To run the server:
```
flask --app app run
```
