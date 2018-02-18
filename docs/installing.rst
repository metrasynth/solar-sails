======================
Installing Solar Sails
======================

Follow the steps below to download and install Solar Sails for your platform.

Proceed to :doc:`getting-started` after you've finished installing the app.


macOS
=====

1.  Visit the `Travis CI build page for Solar Sails`_.
    Click on the build job that says "Xcode: xcode8".

2.  Scroll to the very bottom of the page.
    Find the line that begins with ``download_url: ...``.

3.  Highlight the entire URL starting with ``https://s3.amazonaws.com`` and ending with ``.tar.bz2``.

4.  Copy the URL to your clipboard.

5.  Paste the URL into your browser location bar and press return.
    The download should begin.

6.  After the download completes, open the downloaded ``Solar Sails.app.tar.bz2`` file to extract the app.

7.  Move the resulting Solar Sails app to your Applications folder.

8.  Open the app.
    You will likely receive a warning dialog.
    Refer to Apple's `Open an app from an unidentified developer`_ page, and authorize the Solar Sails app.

9.  If the app closes immediately the first time you open it, open it a second time.
    This is a known issue, but only occurs once each time you install and authorize a new version.

If the app launches successfully, you'll see a small window containing large "Solar Sails" text.
Now proceed to :doc:`getting-started`.

..  _Travis CI build page for Solar Sails:
    https://travis-ci.org/metrasynth/solar-sails

..  _Open an app from an unidentified developer:
    https://support.apple.com/kb/PH25088?locale=en_US


Windows
=======

1.  Visit the `AppVeyor latest build artifact page for Solar Sails`_.

2.  Click on ``dist.zip``.
    The download should begin.

3.  After the download completes, reveal the file in explorer.

4.  Right-click the file and click Extract All.

5.  Choose the destination folder of your choice and click Extract.
    A folder named ``solar-sails`` will be created within the destination folder.

6.  Open the ``solar-sails`` application inside the folder.
    Click Run when the security warning dialog appears.

..  _AppVeyor latest build artifact page for Solar Sails:
    https://ci.appveyor.com/project/gldnspud/solar-sails/build/artifacts

If the app launches successfully, you'll see a small window containing large "Solar Sails" text.
Now proceed to :doc:`getting-started`.


Linux
=====

It is difficult to provide a bundled package that works well across several Linux distributions.
Therefore please follow the steps below for your distribution.

Debian variants without Python 3.6
----------------------------------

Examples: Debian, Linux Mint, Ubuntu.

This assumes you cannot install ``python3-dev``, or if you do, only Python 3.5 is available.
The steps below help you use ``pyenv`` to install Python 3.6.

First-time setup
................

..  code-block:: shell-session

      $ sudo apt install python-dev build-essential libasound2-dev librtmidi-dev libpcre3-dev \
          zlib1g-dev libbz2-dev libreadline-dev libssl-dev libsqlite3-dev

      $ git clone https://github.com/pyenv/pyenv.git ~/.pyenv
      $ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
      $ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
      $ echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc
      $ exec "$SHELL"

      $ pyenv install 3.6.4
      $ git clone https://github.com/metrasynth/solar-sails ~/solar-sails
      $ cd solar-sails
      $ pyenv shell 3.6.4
      $ python --version  # => Python 3.6.4
      $ python -m venv venv
      $ source venv/bin/activate
      $ pip install -r requirements/app.txt
      $ pip install -e $PWD

Starting Solar Sails
....................

..  code-block:: shell-session

      $ ~/solar-sails/venv/bin/sails-gui <optional-mmckpy-pathname>

Updating Solar Sails
....................

..  code-block:: shell-session

      $ cd ~/solar-sails
      $ source venv/bin/activate
      $ git pull
      $ pip install -r requirements/app.txt
      $ pip install -e $PWD

Solus
-----

This is based on Solus 3 Budgie.

First-time setup
................

..  code-block:: shell-session

      $ sudo eopkg install -c system.devel
      $ sudo eopkg install alsa-lib-devel git
      $ cd ~
      $ git clone https://github.com/metrasynth/solar-sails
          # The following is optional, but contains many MMCK example scripts:
      $ git clone https://github.com/metrasynth/gallery
      $ cd ~/solar-sails
      $ python3 -m venv venv
      $ source venv/bin/activate
      $ pip install -r requirements/app.txt
      $ pip install -e .

Starting Solar Sails
....................

..  code-block:: shell-session

      $ ~/solar-sails/venv/bin/sails-gui <optional-mmckpy-pathname>

Updating Solar Sails
....................

..  code-block:: shell-session

      $ cd ~/solar-sails
      $ source venv/bin/activate
      $ git pull
      $ pip install -r requirements/app.txt
      $ pip install -e $PWD
