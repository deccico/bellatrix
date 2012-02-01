sudo rm -rf bellatrix.egg-info
hg commit
hg push
python setup.py sdist upload
