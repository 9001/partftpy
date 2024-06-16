#!/usr/bin/env python
# vim: ts=4 sw=4 et ai:
# -*- coding: utf8 -*-

import logging
import os
import socket
import sys
import threading
import time
from optparse import OptionParser

import partftpy.TftpPacketTypes
from partftpy.TftpClient import TftpClient
from partftpy.TftpShared import TftpException
from partftpy.TftpContexts import TftpContext

log = logging.getLogger("partftpy")
log.setLevel(logging.INFO)

# console handler
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
default_formatter = logging.Formatter("[%(asctime)s] %(message)s")
handler.setFormatter(default_formatter)
log.addHandler(handler)


def main():
    usage = ""
    parser = OptionParser(usage=usage)
    parser.add_option(
        "-H",
        "--host",
        help="remote host or ip address",
    )
    parser.add_option(
        "-p",
        "--port",
        help="remote port to use (default: 69)",
        default=69,
    )
    parser.add_option(
        "-f",
        "--filename",
        help="filename to fetch (deprecated, use download)",
    )
    parser.add_option(
        "-D",
        "--download",
        help="filename to download",
    )
    parser.add_option(
        "-u",
        "--upload",
        help="filename to upload",
    )
    parser.add_option(
        "-b",
        "--blksize",
        help="udp packet size to use (default: 512)",
    )
    parser.add_option(
        "-o",
        "--output",
        help="output file, - for stdout (default: same as download)",
    )
    parser.add_option(
        "-i",
        "--input",
        help="input file, - for stdin (default: same as upload)",
    )
    parser.add_option(
        "-d",
        "--debug",
        action="store_true",
        default=False,
        help="upgrade logging from info to debug",
    )
    parser.add_option(
        "-q",
        "--quiet",
        action="store_true",
        default=False,
        help="downgrade logging from info to warning",
    )
    parser.add_option(
        "-t",
        "--tsize",
        action="store_true",
        default=False,
        help="ask client to send tsize option in download",
    )
    parser.add_option(
        "-l",
        "--localip",
        action="store",
        dest="localip",
        default="",
        help="local IP for client to bind to (ie. interface)",
    )
    options, args = parser.parse_args()
    # Handle legacy --filename argument.
    if options.filename:
        options.download = options.filename
    if not options.host or (not options.download and not options.upload):
        sys.stderr.write("Both the --host and --filename options are required.\n")
        parser.print_help()
        sys.exit(1)

    if options.debug and options.quiet:
        sys.stderr.write("The --debug and --quiet options are mutually exclusive.\n")
        parser.print_help()
        sys.exit(1)

    class Progress(object):
        def __init__(self, out):
            self.out = out
            self.metrics = None
            self.thr = threading.Thread(target=self._print_progress)
            self.thr.daemon = True
            self.thr.start()

        def progresshook(self, pkt, ctx):
            # type: (bytes, TftpContext) -> None
            if isinstance(pkt, partftpy.TftpPacketTypes.TftpPacketDAT):
                self.metrics = ctx.metrics
            elif isinstance(pkt, partftpy.TftpPacketTypes.TftpPacketOACK):
                self.out("Received OACK, options are: %s" % pkt.options)

        def _print_progress(self):
            while True:
                time.sleep(0.5)
                if not self.metrics:
                    continue
                metrics = self.metrics
                self.metrics = None

                pkts = metrics.packets
                nbytes = metrics.bytes
                left = metrics.tsize - nbytes
                if left < 0:
                    self.out("Transferred %d pkts, %d bytes", pkts, nbytes)
                else:
                    self.out(
                        "Transferred %d pkts, %d bytes, %d bytes left",
                        pkts,
                        nbytes,
                        left,
                    )

    if options.debug:
        log.setLevel(logging.DEBUG)
        # increase the verbosity of the formatter
        debug_formatter = logging.Formatter(
            "[%(asctime)s%(msecs)03d] %(levelname)s [%(name)s:%(lineno)s] %(message)s"
        )
        handler.setFormatter(debug_formatter)
    elif options.quiet:
        log.setLevel(logging.WARNING)

    progresshook = Progress(log.info).progresshook

    tftp_options = {}
    if options.blksize:
        tftp_options["blksize"] = int(options.blksize)
    if options.tsize and options.download:
        tftp_options["tsize"] = 0
    if options.tsize and options.upload and options.input != "-":
        fn = options.input or options.upload
        tftp_options["tsize"] = os.path.getsize(fn)

    fam = socket.AF_INET6 if ":" in options.host else socket.AF_INET

    tclient = TftpClient(
        options.host,
        int(options.port),
        tftp_options,
        options.localip,
        af_family=fam,
    )
    try:
        if options.download:
            if not options.output:
                options.output = os.path.basename(options.download)
            tclient.download(
                options.download,
                options.output,
                progresshook,
            )
        elif options.upload:
            if not options.input:
                options.input = os.path.basename(options.upload)
            tclient.upload(
                options.upload,
                options.input,
                progresshook,
            )
    except TftpException as err:
        sys.stderr.write("%s\n" % str(err))
        sys.exit(1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
