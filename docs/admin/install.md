# Installation

There are two options for installing pynautobot. Installing from pypi, which is the likely install method, or if you need a particular feature branch, then option 2 installs from GitHub.

=== "Option 1: Install from PyPI."

    ```bash
    pip install pynautobot
    ```

    ???+ example "Example Output"
        ```
        root@a0480acc1c52:/# pip install pynautobot
        Collecting pynautobot
        Downloading pynautobot-2.1.1-py3-none-any.whl.metadata (5.9 kB)
        Collecting packaging<24.0,>=23.2 (from pynautobot)
        Downloading packaging-23.2-py3-none-any.whl.metadata (3.2 kB)
        Collecting requests<3.0.0,>=2.30.0 (from pynautobot)
        Downloading requests-2.31.0-py3-none-any.whl.metadata (4.6 kB)
        Collecting urllib3<1.27,>=1.21.1 (from pynautobot)
        Downloading urllib3-1.26.18-py2.py3-none-any.whl.metadata (48 kB)
            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 48.9/48.9 kB 1.1 MB/s eta 0:00:00
        Collecting charset-normalizer<4,>=2 (from requests<3.0.0,>=2.30.0->pynautobot)
        Downloading charset_normalizer-3.3.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (33 kB)
        Collecting idna<4,>=2.5 (from requests<3.0.0,>=2.30.0->pynautobot)
        Downloading idna-3.7-py3-none-any.whl.metadata (9.9 kB)
        Collecting certifi>=2017.4.17 (from requests<3.0.0,>=2.30.0->pynautobot)
        Downloading certifi-2024.2.2-py3-none-any.whl.metadata (2.2 kB)
        Downloading pynautobot-2.1.1-py3-none-any.whl (35 kB)
        Downloading packaging-23.2-py3-none-any.whl (53 kB)
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 53.0/53.0 kB 1.8 MB/s eta 0:00:00
        Downloading requests-2.31.0-py3-none-any.whl (62 kB)
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 62.6/62.6 kB 2.1 MB/s eta 0:00:00
        Downloading urllib3-1.26.18-py2.py3-none-any.whl (143 kB)
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 143.8/143.8 kB 3.7 MB/s eta 0:00:00
        Downloading certifi-2024.2.2-py3-none-any.whl (163 kB)
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 163.8/163.8 kB 6.4 MB/s eta 0:00:00
        Downloading charset_normalizer-3.3.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (140 kB)
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 140.3/140.3 kB 5.9 MB/s eta 0:00:00
        Downloading idna-3.7-py3-none-any.whl (66 kB)
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 66.8/66.8 kB 2.6 MB/s eta 0:00:00
        Installing collected packages: urllib3, packaging, idna, charset-normalizer, certifi, requests, pynautobot
        Successfully installed certifi-2024.2.2 charset-normalizer-3.3.2 idna-3.7 packaging-23.2 pynautobot-2.1.1 requests-2.31.0 urllib3-1.26.18
        WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
        ```

=== "Option 2: Install from a GitHub branch"

    ```bash
    pip install git+https://github.com/nautobot/pynautobot.git@develop
    ```

    ???+ example "Install pynautobot from Git"
        ```bash
        root@a0480acc1c52:/# pip install git+https://github.com/nautobot/pynautobot.git@develop
        Collecting git+https://github.com/nautobot/pynautobot.git@develop
        Cloning https://github.com/nautobot/pynautobot.git (to revision develop) to /tmp/pip-req-build-ksc5p8fv
        Running command git clone --filter=blob:none --quiet https://github.com/nautobot/pynautobot.git /tmp/pip-req-build-ksc5p8fv
        Resolved https://github.com/nautobot/pynautobot.git to commit 5b16f2bde691230018882d48ae47d96c135729b0
        Installing build dependencies ... done
        Getting requirements to build wheel ... done
        Preparing metadata (pyproject.toml) ... done
        Requirement already satisfied: packaging<24.0,>=23.2 in /usr/local/lib/python3.11/site-packages (from pynautobot==2.1.1) (23.2)
        Requirement already satisfied: requests<3.0.0,>=2.30.0 in /usr/local/lib/python3.11/site-packages (from pynautobot==2.1.1) (2.31.0)
        Requirement already satisfied: urllib3<1.27,>=1.21.1 in /usr/local/lib/python3.11/site-packages (from pynautobot==2.1.1) (1.26.18)
        Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.11/site-packages (from requests<3.0.0,>=2.30.0->pynautobot==2.1.1) (3.3.2)
        Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.11/site-packages (from requests<3.0.0,>=2.30.0->pynautobot==2.1.1) (3.7)
        Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.11/site-packages (from requests<3.0.0,>=2.30.0->pynautobot==2.1.1) (2024.2.2)
        Building wheels for collected packages: pynautobot
        Building wheel for pynautobot (pyproject.toml) ... done
        Created wheel for pynautobot: filename=pynautobot-2.1.1-py3-none-any.whl size=35823 sha256=ef02e1e6343400301177a7b070951da2359b40ca191fe0177f7a91f8fb4ac867
        Stored in directory: /tmp/pip-ephem-wheel-cache-_jbbt_v5/wheels/68/d3/c1/7f4fe09e4d1fc8d499db39136d1e3481853e84e92aca960016
        Successfully built pynautobot
        Installing collected packages: pynautobot
        Successfully installed pynautobot-2.1.1
        WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
        ```

## Install Specific Version

You may need to install a specific version of pynautobot. Such as when you are using Nautobot 1.6.x yet, you will need to install a 1.x version of pynautobot.

```
pip install pynautobot==1.5.0
```

???+ example "Example installation of pynautobot 1.5"
    ```bash
    root@a0480acc1c52:/# pip install pynautobot==1.5.0
    Collecting pynautobot==1.5.0
    Downloading pynautobot-1.5.0-py3-none-any.whl.metadata (5.9 kB)
    Requirement already satisfied: requests<3.0.0,>=2.30.0 in /usr/local/lib/python3.11/site-packages (from pynautobot==1.5.0) (2.31.0)
    Requirement already satisfied: urllib3<1.27,>=1.21.1 in /usr/local/lib/python3.11/site-packages (from pynautobot==1.5.0) (1.26.18)
    Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.11/site-packages (from requests<3.0.0,>=2.30.0->pynautobot==1.5.0) (3.3.2)
    Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.11/site-packages (from requests<3.0.0,>=2.30.0->pynautobot==1.5.0) (3.7)
    Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.11/site-packages (from requests<3.0.0,>=2.30.0->pynautobot==1.5.0) (2024.2.2)
    Downloading pynautobot-1.5.0-py3-none-any.whl (33 kB)
    Installing collected packages: pynautobot
    Successfully installed pynautobot-1.5.0
    WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
    ```