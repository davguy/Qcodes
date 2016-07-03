from qcodes import Instrument
from qcodes.instrument.parameter import Parameter
from qcodes.instrument.parameter import ManualParameter
from qcodes.utils.validators import Enum, Bool

class CurrentParameter(Parameter):
    def __init__(self, measured_param, camp_ins, name=None):
        p_name = measured_param.name
        self.name = name or 'curr'
        super().__init__(names=(p_name+'_raw', self.name))

        _p_label = None
        _p_unit = None

        self.measured_param = measured_param
        self._instrument = camp_ins

        if hasattr(measured_param, 'label'):
            _p_label = measured_param.label
        if hasattr(measured_param, 'units'):
            _p_unit = measured_param.units

        self.labels = (_p_label, 'Current')
        self.units = (_p_unit, 'A')

    def get(self):
        volt = self.measured_param.get()
        current = (self._instrument.sens.get() *
                   self._instrument.sens_factor.get()) * volt

        if self._instrument.invert.get():
            current *= -1

        value = (volt, current)
        self._save_val(value)
        return value


class Ithaco_1211(Instrument):
    """
    dmm_parameter: The parameter used to measure the voltage output

    This is the qcodes driver for the Ithaco 1211 Current-preamplifier,
    This is a virtual driver only and will not talk to your instrument.
    """
    def __init__(self, name, dmm_parameter=None, **kwargs):
        super().__init__(name, **kwargs)
        self.dmm_parameter = dmm_parameter

        self.add_parameter('sens',
                           parameter_class=ManualParameter,
                           initial_value=1e-8,
                           label='Sensitivity',
                           units='A/V',
                           vals=Enum(1e-11, 1e-10, 1e-09, 1e-08, 1e-07,
                                     1e-06, 1e-05, 1e-4, 1e-3))

        self.add_parameter('invert',
                           parameter_class=ManualParameter,
                           initial_value=True,
                           label='Inverted output',
                           vals=Bool())

        self.add_parameter('sens_factor',
                           parameter_class=ManualParameter,
                           initial_value=1,
                           label='Sensitivity factor',
                           units=None,
                           vals=Enum(0.1, 1, 10))

        self.add_parameter('suppression',
                           parameter_class=ManualParameter,
                           initial_value=1e-7,
                           label='Suppression',
                           units='A',
                           vals=Enum(1e-10, 1e-09, 1e-08, 1e-07, 1e-06,
                                     1e-05, 1e-4, 1e-3))

        self.add_parameter('risetime',
                           parameter_class=ManualParameter,
                           initial_value=0.3,
                           label='Rise Time',
                           units='msec',
                           vals=Enum(0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30,
                                     100, 300, 1000))

    def get_idn(self):
        vendor = 'Ithaco (DL Instruments)'
        model = '1211'
        serial = None
        firmware = None
        return {'vendor': vendor, 'model': model,
                'serial': serial, 'firmware': firmware}
