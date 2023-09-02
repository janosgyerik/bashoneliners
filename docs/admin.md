Admin notes
===========

Helpful notes for site operators / administrators.

Deploying updates
-----------------

Push to the `beta` branch in the `releases` remote:

```bash
git push releases master:beta
```

The remote has a `post-receive` hook script (see under `misc/`), which triggers automated upgrade.

Tweeting one-liners
-------------------

Automatic tweeting of one-liners on behalf of `@bashoneliners` is temporarily disabled, to ensure high quality in the official feed.

Administrators can manually Tweet a worthy one-liner by opening it on the website and using the **Tweet** button.

Banning users
-------------

On Django admin, edit user, uncheck **Active**. They won't be able to login anymore.

Installing a custom version of Python
-------------------------------------

```bash
wget https://www.python.org/ftp/python/3.10.1/Python-3.10.1.tgz
tar zxf Python-3.10.1.tgz
cd Python-3.10.1
./configure --prefix="$HOME/usr/local"
make
make install
```
