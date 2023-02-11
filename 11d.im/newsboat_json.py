# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# ## usage
#
# ```bash
# $ python newsboat_json.py > feeds.json
# ```

# %%
from xml.dom.minidom import parseString
import json
import subprocess

# %%
stdout = (subprocess.run(["newsboat", "-e"], capture_output=True)).stdout

# %%
xml = parseString(stdout)

# %%
blacklist = [
    "11d.im",
    "webmention.io"
]

# %%
feeds = [
    feed
        for feed
        in [ dict(node.attributes.items()) for node in xml.getElementsByTagName('outline') ]
        if
            feed['title'] != ''
            and all([ not ignore in feed['htmlUrl'] for ignore in blacklist ])
]

# %%
print(json.dumps(feeds, indent=2))

# %%
