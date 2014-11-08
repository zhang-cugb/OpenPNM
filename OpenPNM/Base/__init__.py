r"""
###############################################################################
:mod:`OpenPNM.Base` -- Abstract Base Class, and Core Data Class
###############################################################################

.. autoclass:: OpenPNM.Base.Controller
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: OpenPNM.Base.Base
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: OpenPNM.Base.Core
   :members:
   :undoc-members:
   :show-inheritance:

"""

import logging as logging
# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(levelname)-6s %(name)-22s %(message)s',
                    datefmt='20%y-%m-%d %H:%M',
                    )

from .__Controller__ import Controller
from .__Base__ import Base
from .__Core__ import Core