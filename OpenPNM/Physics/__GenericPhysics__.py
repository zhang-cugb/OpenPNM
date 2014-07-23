"""
module Physics
===============================================================================

"""
import sys, os, collections
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if sys.path[1] != parent_dir:
    sys.path.insert(1, parent_dir)

import OpenPNM
import scipy as sp
from functools import partial

class GenericPhysics(OpenPNM.Utilities.Tools):
    r"""
    Generic class to generate Physics objects  

    Parameters
    ----------
    network : OpenPNM Network object 
        The network to which this Physics should be attached
        
    fluid : OpenPNM Fluid object 
        The Fluid object to which this Physics applies
    
    pores and/or throats : array_like
        The list of pores and throats where this physics applies. If either are
        left blank this will apply the physics nowhere.  The locations can be
        change after instantiation using ``set_locations()``.
    
    name : str, optional
        A unique string name to identify the Physics object, typically same as 
        instance name but can be anything.  If left blank, and name will be
        generated that include the class name and a random string.  
    
    """

    def __init__(self,network,fluid,pores=[],throats=[],name=None,dynamic_data=False,**kwargs):
        super(GenericPhysics,self).__init__(**kwargs)
        self._logger.debug("Construct class")
        
        #Append objects self for internal access
        self._net = network
        self._fluid = fluid

        #Append self to other objects
        network._physics.append(self)
        fluid._physics.append(self)
        
        #Initialize attributes
        self._models = collections.OrderedDict()
        self.name = name
        
        #Initialize Physics locations
        self['pore.all'] = sp.ones((sp.shape(pores)[0],),dtype=bool)
        self['throat.all'] = sp.ones((sp.shape(throats)[0],),dtype=bool)
        fluid['pore.'+self.name] = False
        fluid['pore.'+self.name][pores] = True
        fluid['throat.'+self.name] = False
        fluid['throat.'+self.name][throats] = True
        
    def pores(self,**kwargs):
        return self._fluid.pores(labels=self.name)

    def throats(self,**kwargs):
        return self._fluid.throats(labels=self.name)
        
    def regenerate(self, props=''):
        r'''
        This updates all properties using the selected methods

        Parameters
        ----------
        props : string or list of strings
            The names of the properties that should be updated, defaults to all
            
        Examples
        --------
        na
        '''
        if props == '':
            props = self._models.keys()
        elif type(props) == str:
            props = [props]
        for item in props:
            if item in self._models.keys():
                self[item] = self._models[item]()
            else:
                self._logger.warning('Requested proptery is not a dynamic model: '+item)
            
    def add_model(self,model,propname,static=False,**kwargs):
        r'''
        Add specified property estimation model to the fluid object.
        
        Parameters
        ----------
        na
        
        Examples
        --------
        None yet

        '''
        #Build partial function from given kwargs
        Ps = self.pores()
        Ts = self.throats()
        fn = partial(model,fluid=self._fluid,network=self._net,pores=Ps,throats=Ts,**kwargs)
        self[propname] = fn()  # Generate data and store it locally
        if not static:  # Store model in a private attribute
            self._models[propname] = fn
        
    def physics_health(self):
        r'''
        Perform a check to find pores with overlapping or undefined Physics.
        '''
        phys = self._net.physics()
        temp = sp.zeros((self._fluid.Np,))
        for item in phys:
            ind = self._fluid['pore.'+item]
            temp[ind] = temp[ind] + 1
        health = {}
        health['overlaps'] = sp.where(temp>1)[0].tolist()
        health['undefined'] = sp.where(temp==0)[0].tolist()
        return health
        
    def fluids(self):
        r'''
        Return a list of Fluid object names associated with this Physics
        '''
        temp = []
        temp.append(self._fluid.name)
        return temp
        
if __name__ == '__main__':
    print('none yet')


