# Upgrading the Library

Upgrade from PyPI.

```bash
pip install pynautobot --upgrade
```

???+ example "Upgrade example"

    ```
    root@a0480acc1c52:/# pip install --upgrade pynautobot
    Requirement already satisfied: pynautobot in /usr/local/lib/python3.11/site-packages (1.5.0)
    Collecting pynautobot
    Using cached pynautobot-2.1.1-py3-none-any.whl.metadata (5.9 kB)
    Requirement already satisfied: packaging<24.0,>=23.2 in /usr/local/lib/python3.11/site-packages (from pynautobot) (23.2)
    Requirement already satisfied: requests<3.0.0,>=2.30.0 in /usr/local/lib/python3.11/site-packages (from pynautobot) (2.31.0)
    Requirement already satisfied: urllib3<1.27,>=1.21.1 in /usr/local/lib/python3.11/site-packages (from pynautobot) (1.26.18)
    Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.11/site-packages (from requests<3.0.0,>=2.30.0->pynautobot) (3.3.2)
    Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.11/site-packages (from requests<3.0.0,>=2.30.0->pynautobot) (3.7)
    Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.11/site-packages (from requests<3.0.0,>=2.30.0->pynautobot) (2024.2.2)
    Using cached pynautobot-2.1.1-py3-none-any.whl (35 kB)
    Installing collected packages: pynautobot
    Attempting uninstall: pynautobot
        Found existing installation: pynautobot 1.5.0
        Uninstalling pynautobot-1.5.0:
        Successfully uninstalled pynautobot-1.5.0
    Successfully installed pynautobot-2.1.1
    ```