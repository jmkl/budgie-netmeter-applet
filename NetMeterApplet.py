import gi.repository
import os
gi.require_version('Budgie', '1.0')
from gi.repository import Budgie, Gdk, Gio, GLib, GObject, Gtk
from threading import Event
from netmetertext import MThread


css_data = """

#labeltext {
    margin:5px;
    padding: 0 15px 0 15px;
    color: #fff;
    background: rgba(0,0,0,0.4);
    border-radius: 20px;
    
}

"""


class Runner(object):

    def __init__(self):
        self.metext = Gtk.Label("Hello...")
        print("runner init!")

        self.alive = Event()
        self.alive.set()
        n = MThread(self)
        n.start()

    def pangofy(self, d):
        _in = d[0]
        _out = d[1]
        return(" %s<sup><small>%s/s</small></sup>  %s<sup><small>%s/s</small></sup>" % (_in[0], _in[1], _out[0], _out[1]))

    def update(self, data):
        def done(d):
            #fruit = 'Apple'
            #isApple = True if fruit == 'Apple' else False
            self.metext.set_visible(True if int(d[0][0]) > 1 else False)
            self.metext.set_markup(self.pangofy(d))

        if data and self.metext:
            GLib.idle_add(done, data)


class NetMeter(GObject.Object, Budgie.Plugin):
    __gtype_name__ = "JMKLNetMeter"

    def __init__(self):
        GObject.Object.__init__(self)

    def do_get_panel_widget(self, uuid):
        return NetMeterApplet(uuid)


class NetMeterApplet(Budgie.Applet):

    def __init__(self, uuid):
        curdir = os.path.dirname(os.path.abspath(__file__))
        Budgie.Applet.__init__(self)
        r = Runner()
        cssProvider = Gtk.CssProvider()
        cssProvider.load_from_path(os.path.join(curdir, "style.css"))
        # cssProvider.load_from_data(css_data.encode())
        self.nm = r.metext
        self.nm.set_name("labeltext")
        Gtk.StyleContext.add_provider_for_screen(
            self.get_display().get_default_screen(),
            cssProvider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.add(self.nm)
        self.show_all()


class Test(object):

    def __init__(self):
        GObject.threads_init()
        w = Gtk.Window()
        h = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        w.set_default_size(200, 100)
        l = Gtk.Label("Hello")
        cssProvider = Gtk.CssProvider.new()
        cssProvider.load_from_data(css_data.encode())
        styleContext = Gtk.StyleContext()
        styleContext.add_provider_for_screen(
            Gtk.StyleContext(), cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        r = Runner()
        l = r.metext
        l.set_name("labeltext")
        h.add(Gtk.Label("Left"))
        h.add(l)
        h.add(Gtk.Label("Right"))
        w.add(h)
        w.show_all()
        w.connect("destroy", Gtk.main_quit)
        Gtk.main()

    def on_exit(self, event=None, data=None):
        print("ONEXIT")


if __name__ == '__main__':
    n = Test()
