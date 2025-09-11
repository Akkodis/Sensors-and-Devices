from __future__ import print_function
from py5gmeta.activemq.amqp import  VideoReceiver
from proton.reactor import Container
import random
import sys
import gi
from gi.repository import Gst, GObject, GLib, GstApp, GstVideo


pts = 0  # buffers presentation timestamp
gi.require_version('GLib', '2.0')
gi.require_version('GObject', '2.0')
gi.require_version('Gst', '1.0')
gi.require_version('GstApp', '1.0')
gi.require_version('GstVideo', '1.0')


if __name__ == "__main__":
    
    appsrc = None

    pipeline = None
    bus = None
    message = None

    # initialize GStreamer
    Gst.init(sys.argv[1:])

    # build the pipeline
    pipeline = Gst.parse_launch(
        'appsrc caps="video/x-h264, stream-format=byte-stream, alignment=au" name=appsrc ! h264parse config-interval=-1 ! decodebin ! videoconvert ! autovideosink'
    )

    appsrc = pipeline.get_by_name("appsrc")  # get AppSrc
    # instructs appsrc that we will be dealing with timed buffer
    appsrc.set_property("format", Gst.Format.TIME)

    # instructs appsrc to block pushing buffers until ones in queue are preprocessed
    # allows to avoid huge queue internal queue size in appsrc
    appsrc.set_property("block", True)

    # start playing
    print("Pipeline Playing")
    ret = pipeline.set_state(Gst.State.PLAYING)
    if ret == Gst.StateChangeReturn.FAILURE:
        print("Unable to set the pipeline to the playing state.")
        exit(-1)

    print("Container RECEIVER")
    Container(VideoReceiver(url)).run()

    # wait until EOS or error
    bus = pipeline.get_bus()

    # free resources
    pipeline.set_state(Gst.State.NULL)
