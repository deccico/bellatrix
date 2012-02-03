sudo rm -rf bellatrix.egg-info
python setup.py sdist upload
hg commit
hg push
