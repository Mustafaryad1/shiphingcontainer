import iso6346

class ShipContainer:
    
    HEIGHT_FT = 8.5
    WIDTH_FT = 8.0
    next_serial = 1337
    
    @staticmethod
    def _make_bic_code(owner_code,serial):
        return iso6346.create(owner_code=owner_code,serial=str(serial).zfill(6))
        
    @classmethod
    def _get_serial_number(cls):
        result = cls.next_serial
        cls.next_serial +=1
        return result
    
    @classmethod
    def create_empty(cls,owner_code,length_ft,*args,**kwargs):
        return cls(owner_code,length_ft,contents=None,*args,**kwargs)
    
    @classmethod
    def create_with_items(cls,owner_code,length_ft,items,*args,**kwargs):
        return cls(owner_code,contents=list(items),*args,**kwargs)
    
    def __init__(self,owner_code,length_ft,contents):
        self.owner_code = owner_code
        self.contents = contents
        self.length_ft = length_ft
        self.bic = self._make_bic_code(owner_code=owner_code,serial=ShipContainer._get_serial_number())
    
    @property
    def volume_ft3(self):
        return ShipContainer.HEIGHT_FT*ShipContainer.WIDTH_FT*self.length_ft

    
class RefrigeratedShippingContainer(ShipContainer):
    
    FRIDGE_VOLUME_FT3 = 100
    MAX_CELSUIS = 4.0
    
    @staticmethod
    def _c_to_f(celsuis):
        return celsuis *9/5 +32
    
    @staticmethod
    def _f_to_c(fahrenheit):
        return (fahrenheit-32) *5/9 
    
    @staticmethod
    def _make_bic_code(owner_code,serial):
        return iso6346.create(owner_code=owner_code,
                              serial=str(serial).zfill(6),
                              category='R')
    
    def __init__(self,owner_code,length_ft,contents,celsuis):
        super().__init__(owner_code,length_ft,contents)
        self._celsuis = celsuis
    
    @property
    def celsuis(self):
        return self._celsuis
    
    @celsuis.setter
    def celsuis(self,value):
        if value > RefrigeratedShippingContainer.MAX_CELSUIS:
            raise ValueError('Temperature is too hot!')
        self._celsuis = value
    
    @property
    def fahrenheit(self):
        return RefrigeratedShippingContainer._c_to_f(self.celsuis)
    
    @fahrenheit.setter
    def fahrenheit(self,value):
        self.celsuis = RefrigeratedShippingContainer._f_to_c(value)
    
    @property
    def volume_ft3(self):
        return super().volume_ft3 - RefrigeratedShippingContainer.FRIDGE_VOLUME_FT3

class HeatedRefrigeratedShippingContainer(RefrigeratedShippingContainer):
    MIN_CELSUIS = -20.0
    
    @RefrigeratedShippingContainer.celsuis.setter
    def celsuis(self,value):
        if value < HeatedRefrigeratedShippingContainer.MIN_CELSUIS:
            raise ValueError('Temperature is too cold!')
        RefrigeratedShippingContainer.celsuis.fset(self,value)