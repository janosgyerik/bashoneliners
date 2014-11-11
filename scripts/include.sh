. ./virtualenv.sh

apps=(bashoneliners oneliners)

langs=(fr ja hu)

msg() {
    echo "* $@"
}

errmsg() {
    echo ERROR: $@
}

is_app_dir() {
    appdir=$1
    test -f $appdir/__init__.py || {
        errmsg not an app dir: $appdir/__init__.py missing
        return 1
    }
}
