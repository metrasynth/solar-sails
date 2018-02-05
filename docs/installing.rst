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

1.  Visit the `Travis CI build page for Solar Sails`_.
    Select the build job that says "Python: 3.6".

2.  Scroll to the very bottom of the page.
    Find the line that begins with ``download_url: ...``.

3.  Highlight the entire URL starting with ``https://s3.amazonaws.com`` and ending with ``.tar.bz2``.

4.  Copy the URL to your clipboard.

5.  Paste the URL into your browser location bar and press return.
    The download should begin.

6.  Using your preferred method, extract the contents of the file to your preferred location.
    A directory named ``solar-sails`` will be created within the destination.

7.  In a terminal (or using a launcher) run the following command inside the ``solar-sails`` directory to launch the app::

        ./solar-sails.sh

If the app launches successfully, you'll see a small window containing large "Solar Sails" text.
Now proceed to :doc:`getting-started`.
