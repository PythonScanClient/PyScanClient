To start scan server:

ScanServer -pluginCustomization plugin_customization.ini

If scan server is executing in a different directory, it needs to be invoked with the full path
to the plugin_customization.ini file,

   AND
   
all paths inside the plugin_customization.ini which are currently relative to this directory
will also need to be made absolute.


For a production setup, such absolute paths are preferred, but for the example setup the need to
edit the files can be avoided by starting the scan server inside this 'server' directory.