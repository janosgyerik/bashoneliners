virtualenv=$(dirname "$BASH_SOURCE")/virtualenv
activate=$virtualenv/bin/activate

if [ -f "$activate" ]; then
    . "$activate"
else
    {
        echo "Virtualenv looks broken, not a regular file: $activate"
        echo "Create a clean new virtualenv with:"
        echo "  rm -fr \"$virtualenv\""
        echo "  ./scripts/setup.sh path/to/very/specific/version/of/python"
    } >&2
    return 1
fi
