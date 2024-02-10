#!/bin/bash
set -e
echo

# osx support
# port install gnutar findutils gsed coreutils
gtar=$(command -v gtar || command -v gnutar) || true
[ ! -z "$gtar" ] && command -v gfind >/dev/null && {
	tar()  { $gtar "$@"; }
	sed()  { gsed  "$@"; }
	find() { gfind "$@"; }
	sort() { gsort "$@"; }
	command -v grealpath >/dev/null &&
		realpath() { grealpath "$@"; }
}

mode="$1"

[ -z "$mode" ] &&
{
	echo "need argument 1:  (D)ry, (T)est, (U)pload"
	echo " optional arg 2:  fast"
	echo
	exit 1
}

[ -e partftpy/TftpServer.py ] || cd ..
[ -e partftpy/TftpServer.py ] ||
{
	echo "run me from within the partftpy folder"
	echo
	exit 1
}


# one-time stuff, do this manually through copy/paste
true ||
{
	cat > ~/.pypirc <<EOF
[distutils]
index-servers =
  pypi
  pypitest

[pypi]
repository: https://upload.pypi.org/legacy/
username: qwer
password: asdf

[pypitest]
repository: https://test.pypi.org/legacy/
username: qwer
password: asdf
EOF

	# set pypi password
	chmod 600 ~/.pypirc
	sed -ri 's/qwer/username/;s/asdf/password/' ~/.pypirc
}



pydir="$(
	which python |
	sed -r 's@[^/]*$@@'
)"

[ -e "$pydir/activate" ] &&
{
	echo '`deactivate` your virtualenv'
	exit 1
}

function have() {
	python -c "import $1; $1; getattr($1,'__version__',0)"
}

function load_env() {
	. buildenv/bin/activate || return 1
	have setuptools &&
	have wheel &&
	have build &&
	have twine &&
	have jinja2 &&
	have strip_hints &&
	return 0 || return 1
}

load_env || {
	echo creating buildenv
	deactivate || true
	rm -rf buildenv
	python3 -m venv buildenv
	(. buildenv/bin/activate && pip install \
		setuptools wheel build twine jinja2 strip_hints )
	load_env
}

# cleanup
rm -rf build/pypi

# clean-ish packaging env
rm -rf build/pypi
mkdir -p build/pypi
cp -pR pyproject.toml README.md LICENSE partftpy build/pypi/
cd build/pypi

# delete junk
find -name '*.pyc' -delete
find -name __pycache__ -delete
find -name py.typed -delete
find -type f \( -name .DS_Store -or -name ._.DS_Store \) -delete
find -type f -name ._\* | while IFS= read -r f; do cmp <(printf '\x00\x05\x16') <(head -c 3 -- "$f") && rm -f -- "$f"; done

# build
python3 -m build

[ "$mode" == t ] && twine upload -r pypitest dist/*
[ "$mode" == u ] && twine upload -r pypi dist/*

true
