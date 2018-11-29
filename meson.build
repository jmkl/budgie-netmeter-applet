project('jmkl-netmeter',
	version: '0.1.0',	
)

prefix = get_option('prefix')
libdir = join_paths(prefix, get_option('libdir'))

APP_DIR = join_paths(libdir, 
	'budgie-desktop',
	'plugins', 
	meson.project_name())


install_data(['netmetertext.py','NetMeterApplet.py','NetMeterApplet.plugin','style.css'],
    install_dir: APP_DIR
)