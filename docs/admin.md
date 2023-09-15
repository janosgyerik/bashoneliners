Admin notes
===========

Helpful notes for site operators / administrators.


Operations
----------


### Deploying updates

Push to the `beta` branch in the `releases` remote:

```bash
git push releases master:beta
```

The remote has a `post-receive` hook script (see under `misc/`), which triggers automated upgrade.


### Tweeting one-liners

Automatic tweeting of one-liners on behalf of `@bashoneliners` is temporarily disabled, to ensure high quality in the official feed.

Administrators can manually Tweet a worthy one-liner by opening it on the website and using the **Tweet** button.


### Viewing Django logs

See the `logs` directory in the deployment.

Configured in `settings.py`.


### Search engine optimization

Review Google's recommendations, at and around:
https://developers.google.com/search/docs/fundamentals/creating-helpful-content


### Banning users

On Django admin, edit user, uncheck **Active**. They won't be able to login anymore.


Initial setup
-------------


### Installing a custom version of Python

```bash
wget https://www.python.org/ftp/python/3.10.1/Python-3.10.1.tgz
tar zxf Python-3.10.1.tgz
cd Python-3.10.1
./configure --prefix="$HOME/usr/local"
make
make install
```


### Setting up social logins

Add appropriate `AUTHENTICATION_BACKENDS` in site `settings.py`.

See site `settings.py` for detailed steps to configure.

### Setting up URL shortener

TODO

### Setting up Tweeting

See site `settings.py` for detailed steps to configure.
