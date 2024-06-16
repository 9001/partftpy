this is a fork of [tftpy](https://github.com/msoulier/tftpy) with [copyparty](https://github.com/9001/copyparty)-specific changes

available [on pypi](https://pypi.org/project/partftpy/)

99% of the code here is copyright 2010-2021, Michael P. Soulier (msoulier@digitaltorque.ca)


# warning

the purpose of this fork is to support copyparty with any necessary changes (possibly controversial ones, such as [4e873925](https://github.com/9001/partftpy/commit/4e873925))

while unlikely at this point, there might be additional **breaking changes,** but I'll try to not break anything by accident

my main focus will be features/bugs which affect copyparty, meaning the server part of this library -- anything else will be **low priority, or maybe even wontfix** (sorry!)


# significant changes

* `from tftpy import TftpServer` => `from partftpy.TftpServer import TftpServer` [4e873925](https://github.com/9001/partftpy/commit/4e873925)
  * to make it possible to monkeypatch stuff inside `TftpServer`, for example swapping out the `os` module with a virtual filesystem, which copyparty does
  * crude alternative to [fknittel's proper VFS](https://github.com/msoulier/tftpy/pull/30) but copyparty was already doing this for impacket so for my purposes it's fine

* supports specifying a portrange to use for data transfer instead of selecting an ephemeral port [b8844c03](https://github.com/9001/partftpy/commit/b8844c03)
  * good for firewalls

* support IPv6 by merging [#98 (Add ipv6 support for server and client)](https://github.com/msoulier/tftpy/pull/98/files) [b3e3c39a](https://github.com/9001/partftpy/commit/b3e3c39a)

* support utf-8 filenames [73d12fc0](https://github.com/9001/partftpy/commit/73d12fc0)
  * spec says netascii but many clients do this instead, including curl

* yolo fix for [#140 (crash on small packets)](https://github.com/msoulier/tftpy/issues/140) [79ac8460](https://github.com/9001/partftpy/commit/79ac8460)

* improved robustness for unreliable networks

  * ignore duplicate ACK/OACK instead of panicking [72acb114](https://github.com/9001/partftpy/commit/72acb114)

* workarounds for buggy servers/clients

  * fix [#141 (allow blank options in OACK)](https://github.com/msoulier/tftpy/issues/141) [8e52f3d8](https://github.com/9001/partftpy/commit/8e52f3d8)

  * fix [#136 (allow multiple null-terminators in OACK)](https://github.com/msoulier/tftpy/issues/136) [236fb087](https://github.com/9001/partftpy/commit/236fb087)

* fix [#113 (uploading from stdin, downloading to stdout)](https://github.com/msoulier/tftpy/issues/113) [0087f02d](https://github.com/9001/partftpy/commit/0087f02d)


# other changes

* less info logs [b7e71855](https://github.com/9001/partftpy/commit/b7e71855)

* restored python 2.7 support [c0d19ada](https://github.com/9001/partftpy/commit/c0d19ada)


----

how to release:

* update version and date in `__init__.py`
* `git commit -m v0.x.y`
* `git tag v0.x.y`
* `git push --tags`
* `./scripts/make-pypi-release.sh u`

