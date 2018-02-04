======================
Installing Solar Sails
======================

Follow the steps below to download and install Solar Sails for your platform.

Proceed to :doc:`getting-started` after you've finished installing the app.


macOS
=====

1.  Visit the `Travis CI build page for Solar Sails`_.

2.  Scroll to the very bottom of the page.

3.  Find the line that begins with ``download_url: ...``.

4.  Highlight the entire URL starting with ``https://s3.amazonaws.com`` and ending with ``.tar.bz2``.

5.  Copy the URL to your clipboard.

6.  Paste the URL into your browser location bar and press return.
    The download should begin.

7.  After the download completes, open the downloaded ``Solar Sails.app.tar.bz2`` file to extract the app.

8.  Move the resulting Solar Sails app to your Applications folder.

9.  Open the app.
    You will likely receive a warning dialog.
    Refer to Apple's `Open an app from an unidentified developer`_ page, and authorize the Solar Sails app.

10. If the app closes immediately the first time you open it, open it a second time.
    This is a known issue, but only occurs once each time you install and authorize a new version.

..  _Travis CI build page for Solar Sails:
    https://travis-ci.org/metrasynth/solar-sails

If the app launches successfully, you'll see a small window containing large "Solar Sails" text.
Now proceed to :doc:`getting-started`.


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

1.  Visit the `CircleCI build page for Solar Sails`_.

2.  Click on the most recent Success badge to view the latest build.

3.  Append ``#artifacts/containers/0`` to the end of the URL in your browser's location bar and press enter.
    The build artifacts will be revealed.

4.  Click on ``solar-sails-linux-x64.tar.bz2``.
    The download should begin.

5.  Using your preferred method, extract the contents of the file to your preferred location.
    A directory named ``solar-sails`` will be created within the destination.

6.  In a terminal, run the following command to launch the app::

        ./solar-sails

    If you receive an ``ImportError`` about ``undefined symbol: drmFreeDevice``,
    run this command instead::

        LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libdrm.so.2 ./solar-sails

..  _CircleCI build page for Solar Sails:
    https://circleci.com/gh/metrasynth/solar-sails

If the app launches successfully, you'll see a small window containing large "Solar Sails" text.
Now proceed to :doc:`getting-started`.
