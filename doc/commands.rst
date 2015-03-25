Scan Commands
=============

Assemble a scan from commands.

.. sourcecode:: python

    from scan.commands import *
    
    cmds = [
       Set('pv1', 42)
    ]
    

Key Commands
------------
   
.. autoclass:: scan.commands.comment.Comment
   :members:

.. autoclass:: scan.commands.set.Set
   :members:

.. autoclass:: scan.commands.delay.Delay
   :members:

.. autoclass:: scan.commands.log.Log
   :members:

.. autoclass:: scan.commands.include.Include
   :members:


Specialized Commands
--------------------

.. autoclass:: scan.commands.command.Command
   :members: genXML, __repr__, toCmdString

.. autoclass:: scan.commands.configlog.ConfigLog
   :members:
   