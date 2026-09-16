# Generated from 'v1_2_1.xml' on 2025-07-21 10:00:16.755427

from typing import Tuple
from typing import Optional

from toptica.lasersdk.client import UserLevel
from toptica.lasersdk.client import Client

from toptica.lasersdk.client import DecopError
from toptica.lasersdk.client import DeviceNotFoundError

from toptica.lasersdk.client import DecopBoolean
from toptica.lasersdk.client import DecopInteger
from toptica.lasersdk.client import DecopReal
from toptica.lasersdk.client import DecopString
from toptica.lasersdk.client import DecopBinary

from toptica.lasersdk.client import MutableDecopBoolean
from toptica.lasersdk.client import MutableDecopInteger
from toptica.lasersdk.client import MutableDecopReal
from toptica.lasersdk.client import MutableDecopString
from toptica.lasersdk.client import MutableDecopBinary

from toptica.lasersdk.client import SettableDecopBoolean
from toptica.lasersdk.client import SettableDecopInteger
from toptica.lasersdk.client import SettableDecopReal
from toptica.lasersdk.client import SettableDecopString
from toptica.lasersdk.client import SettableDecopBinary

from toptica.lasersdk.client import Subscription
from toptica.lasersdk.client import Timestamp
from toptica.lasersdk.client import SubscriptionValue

from toptica.lasersdk.client import Connection
from toptica.lasersdk.client import SerialConnection

import toptica.lasersdk.client


class NetworkConnection(toptica.lasersdk.client.NetworkConnection):
    def __init__(self, host: str, command_line_port: int = 50000, monitoring_line_port: int = 0, timeout: int = 5) -> None:
        super().__init__(host, command_line_port, monitoring_line_port, timeout)


class Laser:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._label = DecopString(client, name + ':label')
        self._type = DecopString(client, name + ':type')
        self._remote_id = DecopInteger(client, name + ':remote-id')
        self._multidiode_id = DecopInteger(client, name + ':multidiode-id')
        self._enable = MutableDecopBoolean(client, name + ':enable')
        self._cw = MutableDecopBoolean(client, name + ':cw')
        self._ready = DecopBoolean(client, name + ':ready')
        self._fault = DecopBoolean(client, name + ':fault')
        self._clip = DecopBoolean(client, name + ':clip')
        self._status = DecopInteger(client, name + ':status')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._level = MutableDecopReal(client, name + ':level')
        self._raw_level = MutableDecopInteger(client, name + ':raw-level')
        self._analog_mode = MutableDecopBoolean(client, name + ':analog-mode')
        self._use_ttl = MutableDecopBoolean(client, name + ':use-ttl')
        self._fine = Fine(client, name + ':fine')
        self._entime = DecopInteger(client, name + ':entime')
        self._entime_txt = DecopString(client, name + ':entime-txt')
        self._ontime = DecopInteger(client, name + ':ontime')
        self._ontime_txt = DecopString(client, name + ':ontime-txt')
        self._internal100 = MutableDecopReal(client, name + ':internal100')
        self._analog_in = DecopInteger(client, name + ':analog-in')
        self._digital_in = DecopInteger(client, name + ':digital-in')
        self._rescue_aux = MutableDecopInteger(client, name + ':rescue-aux')
        self._rescue_fiber = MutableDecopInteger(client, name + ':rescue-fiber')
        self._diode = Diode(client, name + ':diode')
        self._boost = Boost(client, name + ':boost')
        self._shg = Shg(client, name + ':shg')
        self._beam = Beam(client, name + ':beam')

    @property
    def label(self) -> 'DecopString':
        return self._label

    @property
    def type(self) -> 'DecopString':
        return self._type

    @property
    def remote_id(self) -> 'DecopInteger':
        return self._remote_id

    @property
    def multidiode_id(self) -> 'DecopInteger':
        return self._multidiode_id

    @property
    def enable(self) -> 'MutableDecopBoolean':
        return self._enable

    @property
    def cw(self) -> 'MutableDecopBoolean':
        return self._cw

    @property
    def ready(self) -> 'DecopBoolean':
        return self._ready

    @property
    def fault(self) -> 'DecopBoolean':
        return self._fault

    @property
    def clip(self) -> 'DecopBoolean':
        return self._clip

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def level(self) -> 'MutableDecopReal':
        return self._level

    @property
    def raw_level(self) -> 'MutableDecopInteger':
        return self._raw_level

    @property
    def analog_mode(self) -> 'MutableDecopBoolean':
        return self._analog_mode

    @property
    def use_ttl(self) -> 'MutableDecopBoolean':
        return self._use_ttl

    @property
    def fine(self) -> 'Fine':
        return self._fine

    @property
    def entime(self) -> 'DecopInteger':
        return self._entime

    @property
    def entime_txt(self) -> 'DecopString':
        return self._entime_txt

    @property
    def ontime(self) -> 'DecopInteger':
        return self._ontime

    @property
    def ontime_txt(self) -> 'DecopString':
        return self._ontime_txt

    @property
    def internal100(self) -> 'MutableDecopReal':
        return self._internal100

    @property
    def analog_in(self) -> 'DecopInteger':
        return self._analog_in

    @property
    def digital_in(self) -> 'DecopInteger':
        return self._digital_in

    @property
    def rescue_aux(self) -> 'MutableDecopInteger':
        return self._rescue_aux

    @property
    def rescue_fiber(self) -> 'MutableDecopInteger':
        return self._rescue_fiber

    @property
    def diode(self) -> 'Diode':
        return self._diode

    @property
    def boost(self) -> 'Boost':
        return self._boost

    @property
    def shg(self) -> 'Shg':
        return self._shg

    @property
    def beam(self) -> 'Beam':
        return self._beam

    def reset_clip(self) -> None:
        self.__client.exec(self.__name + ':reset-clip')

    def store_config(self) -> None:
        self.__client.exec(self.__name + ':store-config')

    def gen_lookup(self) -> None:
        self.__client.exec(self.__name + ':gen-lookup')

    def disp_lookup(self) -> None:
        self.__client.exec(self.__name + ':disp-lookup')

    def store_lookup(self) -> None:
        self.__client.exec(self.__name + ':store-lookup')

    def load_lookup(self) -> None:
        self.__client.exec(self.__name + ':load-lookup')

    def clear_lookup(self) -> None:
        self.__client.exec(self.__name + ':clear-lookup')

    def check_lookup(self) -> float:
        return self.__client.exec(self.__name + ':check-lookup', return_type=float)

    def gen_splitter_lookup(self, fiber: int) -> None:
        assert isinstance(fiber, int), f"expected type 'int' for parameter 'fiber', got '{type(fiber)}'"
        self.__client.exec(self.__name + ':gen-splitter-lookup', fiber)

    def clear_splitter_lookup(self, fiber: int) -> None:
        assert isinstance(fiber, int), f"expected type 'int' for parameter 'fiber', got '{type(fiber)}'"
        self.__client.exec(self.__name + ':clear-splitter-lookup', fiber)

    def load_splitter_lookup(self) -> None:
        self.__client.exec(self.__name + ':load-splitter-lookup')

    def disp_splitter_lookup(self) -> str:
        return self.__client.exec(self.__name + ':disp-splitter-lookup', output_type=str)

    def store_splitter_lookup(self) -> None:
        self.__client.exec(self.__name + ':store-splitter-lookup')

    def set_internal100(self) -> None:
        self.__client.exec(self.__name + ':set-internal100')

    def set_external100(self, power: float) -> None:
        assert isinstance(power, float), f"expected type 'float' for parameter 'power', got '{type(power)}'"
        self.__client.exec(self.__name + ':set-external100', power)


class Fine:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._enable = MutableDecopBoolean(client, name + ':enable')
        self._a = MutableDecopReal(client, name + ':a')
        self._b = MutableDecopReal(client, name + ':b')

    @property
    def enable(self) -> 'MutableDecopBoolean':
        return self._enable

    @property
    def a(self) -> 'MutableDecopReal':
        return self._a

    @property
    def b(self) -> 'MutableDecopReal':
        return self._b


class Diode:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._biascur = MutableDecopReal(client, name + ':biascur')
        self._chsel = DecopInteger(client, name + ':chsel')
        self._comparator = DecopBoolean(client, name + ':comparator')
        self._compcur = MutableDecopReal(client, name + ':compcur')
        self._cur = DecopReal(client, name + ':cur')
        self._curampl = MutableDecopReal(client, name + ':curampl')
        self._cursetfactor = MutableDecopInteger(client, name + ':cursetfactor')
        self._diode_type = MutableDecopString(client, name + ':diode-type')
        self._emisel = DecopInteger(client, name + ':emisel')
        self._hfmf = DecopInteger(client, name + ':hfmf')
        self._hfmp = DecopInteger(client, name + ':hfmp')
        self._ldcr = DecopInteger(client, name + ':ldcr')
        self._maxcur = DecopReal(client, name + ':maxcur')
        self._modamp = DecopInteger(client, name + ':modamp')
        self._oscenable = MutableDecopBoolean(client, name + ':oscenable')
        self._r_disable = MutableDecopBoolean(client, name + ':r-disable')
        self._sm_ch2 = DecopBoolean(client, name + ':sm-ch2')
        self._sm_ch5 = DecopBoolean(client, name + ':sm-ch5')
        self._volt = DecopReal(client, name + ':volt')

    @property
    def biascur(self) -> 'MutableDecopReal':
        return self._biascur

    @property
    def chsel(self) -> 'DecopInteger':
        return self._chsel

    @property
    def comparator(self) -> 'DecopBoolean':
        return self._comparator

    @property
    def compcur(self) -> 'MutableDecopReal':
        return self._compcur

    @property
    def cur(self) -> 'DecopReal':
        return self._cur

    @property
    def curampl(self) -> 'MutableDecopReal':
        return self._curampl

    @property
    def cursetfactor(self) -> 'MutableDecopInteger':
        return self._cursetfactor

    @property
    def diode_type(self) -> 'MutableDecopString':
        return self._diode_type

    @property
    def emisel(self) -> 'DecopInteger':
        return self._emisel

    @property
    def hfmf(self) -> 'DecopInteger':
        return self._hfmf

    @property
    def hfmp(self) -> 'DecopInteger':
        return self._hfmp

    @property
    def ldcr(self) -> 'DecopInteger':
        return self._ldcr

    @property
    def maxcur(self) -> 'DecopReal':
        return self._maxcur

    @property
    def modamp(self) -> 'DecopInteger':
        return self._modamp

    @property
    def oscenable(self) -> 'MutableDecopBoolean':
        return self._oscenable

    @property
    def r_disable(self) -> 'MutableDecopBoolean':
        return self._r_disable

    @property
    def sm_ch2(self) -> 'DecopBoolean':
        return self._sm_ch2

    @property
    def sm_ch5(self) -> 'DecopBoolean':
        return self._sm_ch5

    @property
    def volt(self) -> 'DecopReal':
        return self._volt


class Boost:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._analog_dac = DecopInteger(client, name + ':analog-dac')
        self._cur = DecopReal(client, name + ':cur')
        self._curampl = MutableDecopReal(client, name + ':curampl')
        self._diode_type = DecopString(client, name + ':diode-type')
        self._maxcur = DecopReal(client, name + ':maxcur')

    @property
    def analog_dac(self) -> 'DecopInteger':
        return self._analog_dac

    @property
    def cur(self) -> 'DecopReal':
        return self._cur

    @property
    def curampl(self) -> 'MutableDecopReal':
        return self._curampl

    @property
    def diode_type(self) -> 'DecopString':
        return self._diode_type

    @property
    def maxcur(self) -> 'DecopReal':
        return self._maxcur

    def store_config(self) -> None:
        self.__client.exec(self.__name + ':store-config')


class Shg:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._temp = SettableDecopReal(client, name + ':temp')
        self._opt_step = MutableDecopReal(client, name + ':opt-step')
        self._opt_delay = MutableDecopInteger(client, name + ':opt-delay')
        self._opt_timeout = MutableDecopInteger(client, name + ':opt-timeout')
        self._opt_tolerance = MutableDecopReal(client, name + ':opt-tolerance')

    @property
    def temp(self) -> 'SettableDecopReal':
        return self._temp

    @property
    def opt_step(self) -> 'MutableDecopReal':
        return self._opt_step

    @property
    def opt_delay(self) -> 'MutableDecopInteger':
        return self._opt_delay

    @property
    def opt_timeout(self) -> 'MutableDecopInteger':
        return self._opt_timeout

    @property
    def opt_tolerance(self) -> 'MutableDecopReal':
        return self._opt_tolerance

    def optimize(self) -> None:
        self.__client.exec(self.__name + ':optimize')

    def store_config(self) -> None:
        self.__client.exec(self.__name + ':store-config')


class Beam:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._drive_a = Elliptec(client, name + ':drive-a')
        self._drive_b = Elliptec(client, name + ':drive-b')
        self._drive_c = Elliptec(client, name + ':drive-c')
        self._splitter_attenuator = MutableDecopReal(client, name + ':splitter-attenuator')
        self._splitter_delay = MutableDecopInteger(client, name + ':splitter-delay')
        self._splitter_lookup_delay = MutableDecopInteger(client, name + ':splitter-lookup-delay')
        self._splitter_lookup_step = MutableDecopInteger(client, name + ':splitter-lookup-step')
        self._splitter_step_back = MutableDecopInteger(client, name + ':splitter-step-back')
        self._splitter_step_fwd = MutableDecopInteger(client, name + ':splitter-step-fwd')
        self._splitter_step_minimum = MutableDecopInteger(client, name + ':splitter-step-minimum')
        self._splitter_max_steps = MutableDecopInteger(client, name + ':splitter-max-steps')
        self._splitter_increase_tolerance_after_steps = MutableDecopInteger(client, name + ':splitter-increase-tolerance-after-steps')
        self._splitter_increase_tolerance_every_steps = MutableDecopInteger(client, name + ':splitter-increase-tolerance-every-steps')
        self._splitter_ratio = MutableDecopReal(client, name + ':splitter-ratio')
        self._splitter_damping_factor = MutableDecopReal(client, name + ':splitter-damping-factor')
        self._splitter_ratio_tol = MutableDecopReal(client, name + ':splitter-ratio-tol')
        self._splitter_level = MutableDecopReal(client, name + ':splitter-level')
        self._splitter_power_set = DecopInteger(client, name + ':splitter-power-set')
        self._splitter_wait_in_target = MutableDecopInteger(client, name + ':splitter-wait-in-target')
        self._splitter_switched_at_fiber1 = DecopBoolean(client, name + ':splitter-switched-at-fiber1')
        self._splitter_switched_at_fiber2 = DecopBoolean(client, name + ':splitter-switched-at-fiber2')
        self._splitter_debug = MutableDecopBoolean(client, name + ':splitter-debug')
        self._splitter_data = DecopBinary(client, name + ':splitter-data')
        self._splitter_available = MutableDecopBoolean(client, name + ':splitter-available')

    @property
    def drive_a(self) -> 'Elliptec':
        return self._drive_a

    @property
    def drive_b(self) -> 'Elliptec':
        return self._drive_b

    @property
    def drive_c(self) -> 'Elliptec':
        return self._drive_c

    @property
    def splitter_attenuator(self) -> 'MutableDecopReal':
        return self._splitter_attenuator

    @property
    def splitter_delay(self) -> 'MutableDecopInteger':
        return self._splitter_delay

    @property
    def splitter_lookup_delay(self) -> 'MutableDecopInteger':
        return self._splitter_lookup_delay

    @property
    def splitter_lookup_step(self) -> 'MutableDecopInteger':
        return self._splitter_lookup_step

    @property
    def splitter_step_back(self) -> 'MutableDecopInteger':
        return self._splitter_step_back

    @property
    def splitter_step_fwd(self) -> 'MutableDecopInteger':
        return self._splitter_step_fwd

    @property
    def splitter_step_minimum(self) -> 'MutableDecopInteger':
        return self._splitter_step_minimum

    @property
    def splitter_max_steps(self) -> 'MutableDecopInteger':
        return self._splitter_max_steps

    @property
    def splitter_increase_tolerance_after_steps(self) -> 'MutableDecopInteger':
        return self._splitter_increase_tolerance_after_steps

    @property
    def splitter_increase_tolerance_every_steps(self) -> 'MutableDecopInteger':
        return self._splitter_increase_tolerance_every_steps

    @property
    def splitter_ratio(self) -> 'MutableDecopReal':
        return self._splitter_ratio

    @property
    def splitter_damping_factor(self) -> 'MutableDecopReal':
        return self._splitter_damping_factor

    @property
    def splitter_ratio_tol(self) -> 'MutableDecopReal':
        return self._splitter_ratio_tol

    @property
    def splitter_level(self) -> 'MutableDecopReal':
        return self._splitter_level

    @property
    def splitter_power_set(self) -> 'DecopInteger':
        return self._splitter_power_set

    @property
    def splitter_wait_in_target(self) -> 'MutableDecopInteger':
        return self._splitter_wait_in_target

    @property
    def splitter_switched_at_fiber1(self) -> 'DecopBoolean':
        return self._splitter_switched_at_fiber1

    @property
    def splitter_switched_at_fiber2(self) -> 'DecopBoolean':
        return self._splitter_switched_at_fiber2

    @property
    def splitter_debug(self) -> 'MutableDecopBoolean':
        return self._splitter_debug

    @property
    def splitter_data(self) -> 'DecopBinary':
        return self._splitter_data

    @property
    def splitter_available(self) -> 'MutableDecopBoolean':
        return self._splitter_available

    def splitter_switch(self, fiber: int) -> int:
        assert isinstance(fiber, int), f"expected type 'int' for parameter 'fiber', got '{type(fiber)}'"
        return self.__client.exec(self.__name + ':splitter-switch', fiber, return_type=int)

    def splitter_rescue(self, array_size: int, step_size: int) -> None:
        assert isinstance(array_size, int), f"expected type 'int' for parameter 'array_size', got '{type(array_size)}'"
        assert isinstance(step_size, int), f"expected type 'int' for parameter 'step_size', got '{type(step_size)}'"
        self.__client.exec(self.__name + ':splitter-rescue', array_size, step_size)

    def optimize(self) -> int:
        return self.__client.exec(self.__name + ':optimize', return_type=int)

    def rescue(self) -> int:
        return self.__client.exec(self.__name + ':rescue', return_type=int)

    def store_config(self) -> None:
        self.__client.exec(self.__name + ':store-config')


class Elliptec:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._fwdfreq = MutableDecopInteger(client, name + ':fwdfreq')
        self._backfreq = MutableDecopInteger(client, name + ':backfreq')
        self._frequency = MutableDecopInteger(client, name + ':frequency')
        self._moves = MutableDecopInteger(client, name + ':moves')
        self._travel = MutableDecopReal(client, name + ':travel')
        self._step = MutableDecopInteger(client, name + ':step')

    @property
    def fwdfreq(self) -> 'MutableDecopInteger':
        return self._fwdfreq

    @property
    def backfreq(self) -> 'MutableDecopInteger':
        return self._backfreq

    @property
    def frequency(self) -> 'MutableDecopInteger':
        return self._frequency

    @property
    def moves(self) -> 'MutableDecopInteger':
        return self._moves

    @property
    def travel(self) -> 'MutableDecopReal':
        return self._travel

    @property
    def step(self) -> 'MutableDecopInteger':
        return self._step

    def findfreqs(self) -> str:
        return self.__client.exec(self.__name + ':findfreqs', output_type=str)

    def store_config(self) -> None:
        self.__client.exec(self.__name + ':store-config')

    def move(self, time: int) -> None:
        assert isinstance(time, int), f"expected type 'int' for parameter 'time', got '{type(time)}'"
        self.__client.exec(self.__name + ':move', time)

    def fwd(self) -> None:
        self.__client.exec(self.__name + ':fwd')

    def back(self) -> None:
        self.__client.exec(self.__name + ':back')

    def run(self, frequency: int) -> None:
        assert isinstance(frequency, int), f"expected type 'int' for parameter 'frequency', got '{type(frequency)}'"
        self.__client.exec(self.__name + ':run', frequency)

    def stop(self) -> None:
        self.__client.exec(self.__name + ':stop')


class AllLasers:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._enable = MutableDecopBoolean(client, name + ':enable')
        self._enable_led = DecopBoolean(client, name + ':enable-led')
        self._cw = MutableDecopBoolean(client, name + ':cw')
        self._analog_mode = MutableDecopBoolean(client, name + ':analog-mode')
        self._analog_switch_mode = MutableDecopBoolean(client, name + ':analog-switch-mode')
        self._analog_switch_fiber = MutableDecopInteger(client, name + ':analog-switch-fiber')
        self._use_ttl = MutableDecopBoolean(client, name + ':use-ttl')
        self._ttl_active_high = MutableDecopBoolean(client, name + ':ttl-active-high')
        self._ttl_master_mode = MutableDecopBoolean(client, name + ':ttl-master-mode')
        self._digital_over_analog = DecopBoolean(client, name + ':digital-over-analog')
        self._ready = DecopBoolean(client, name + ':ready')
        self._fault = DecopBoolean(client, name + ':fault')

    @property
    def enable(self) -> 'MutableDecopBoolean':
        return self._enable

    @property
    def enable_led(self) -> 'DecopBoolean':
        return self._enable_led

    @property
    def cw(self) -> 'MutableDecopBoolean':
        return self._cw

    @property
    def analog_mode(self) -> 'MutableDecopBoolean':
        return self._analog_mode

    @property
    def analog_switch_mode(self) -> 'MutableDecopBoolean':
        return self._analog_switch_mode

    @property
    def analog_switch_fiber(self) -> 'MutableDecopInteger':
        return self._analog_switch_fiber

    @property
    def use_ttl(self) -> 'MutableDecopBoolean':
        return self._use_ttl

    @property
    def ttl_active_high(self) -> 'MutableDecopBoolean':
        return self._ttl_active_high

    @property
    def ttl_master_mode(self) -> 'MutableDecopBoolean':
        return self._ttl_master_mode

    @property
    def digital_over_analog(self) -> 'DecopBoolean':
        return self._digital_over_analog

    @property
    def ready(self) -> 'DecopBoolean':
        return self._ready

    @property
    def fault(self) -> 'DecopBoolean':
        return self._fault

    def reset_clip(self) -> None:
        self.__client.exec(self.__name + ':reset-clip')

    def store_config(self) -> None:
        self.__client.exec(self.__name + ':store-config')

    def switch_fiber(self, fiber: int) -> int:
        assert isinstance(fiber, int), f"expected type 'int' for parameter 'fiber', got '{type(fiber)}'"
        return self.__client.exec(self.__name + ':switch-fiber', fiber, return_type=int)


class Tec:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._enable = MutableDecopBoolean(client, name + ':enable')
        self._status = DecopInteger(client, name + ':status')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._fault = DecopBoolean(client, name + ':fault')
        self._temp = SettableDecopReal(client, name + ':temp')
        self._kp = MutableDecopInteger(client, name + ':kp')
        self._ki = MutableDecopInteger(client, name + ':ki')
        self._kd = MutableDecopInteger(client, name + ':kd')
        self._calculated_error = DecopInteger(client, name + ':calculated-error')
        self._proportional_pwm = DecopInteger(client, name + ':proportional-pwm')
        self._integral_pwm = DecopInteger(client, name + ':integral-pwm')
        self._integral = DecopInteger(client, name + ':integral')
        self._pwm_set = DecopInteger(client, name + ':pwm-set')
        self._pwm = MutableDecopInteger(client, name + ':pwm')
        self._max_pwm = MutableDecopInteger(client, name + ':max-pwm')
        self._available = MutableDecopBoolean(client, name + ':available')

    @property
    def enable(self) -> 'MutableDecopBoolean':
        return self._enable

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def fault(self) -> 'DecopBoolean':
        return self._fault

    @property
    def temp(self) -> 'SettableDecopReal':
        return self._temp

    @property
    def kp(self) -> 'MutableDecopInteger':
        return self._kp

    @property
    def ki(self) -> 'MutableDecopInteger':
        return self._ki

    @property
    def kd(self) -> 'MutableDecopInteger':
        return self._kd

    @property
    def calculated_error(self) -> 'DecopInteger':
        return self._calculated_error

    @property
    def proportional_pwm(self) -> 'DecopInteger':
        return self._proportional_pwm

    @property
    def integral_pwm(self) -> 'DecopInteger':
        return self._integral_pwm

    @property
    def integral(self) -> 'DecopInteger':
        return self._integral

    @property
    def pwm_set(self) -> 'DecopInteger':
        return self._pwm_set

    @property
    def pwm(self) -> 'MutableDecopInteger':
        return self._pwm

    @property
    def max_pwm(self) -> 'MutableDecopInteger':
        return self._max_pwm

    @property
    def available(self) -> 'MutableDecopBoolean':
        return self._available

    def store_config(self) -> None:
        self.__client.exec(self.__name + ':store-config')


class Dx5100:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._fw_ver = DecopString(client, name + ':fw-ver')
        self._serial_number = DecopString(client, name + ':serial-number')

    @property
    def fw_ver(self) -> 'DecopString':
        return self._fw_ver

    @property
    def serial_number(self) -> 'DecopString':
        return self._serial_number


class TecDx:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._enable = MutableDecopBoolean(client, name + ':enable')
        self._status = DecopInteger(client, name + ':status')
        self._status_txt = DecopString(client, name + ':status-txt')
        self._temp = SettableDecopReal(client, name + ':temp')
        self._temp_min = MutableDecopReal(client, name + ':temp-min')
        self._temp_max = MutableDecopReal(client, name + ':temp-max')
        self._kp = MutableDecopReal(client, name + ':kp')
        self._ki = MutableDecopReal(client, name + ':ki')
        self._kd = MutableDecopReal(client, name + ':kd')
        self._calibration = Thermistor(client, name + ':calibration')
        self._auto_enable = MutableDecopBoolean(client, name + ':auto-enable')

    @property
    def enable(self) -> 'MutableDecopBoolean':
        return self._enable

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def status_txt(self) -> 'DecopString':
        return self._status_txt

    @property
    def temp(self) -> 'SettableDecopReal':
        return self._temp

    @property
    def temp_min(self) -> 'MutableDecopReal':
        return self._temp_min

    @property
    def temp_max(self) -> 'MutableDecopReal':
        return self._temp_max

    @property
    def kp(self) -> 'MutableDecopReal':
        return self._kp

    @property
    def ki(self) -> 'MutableDecopReal':
        return self._ki

    @property
    def kd(self) -> 'MutableDecopReal':
        return self._kd

    @property
    def calibration(self) -> 'Thermistor':
        return self._calibration

    @property
    def auto_enable(self) -> 'MutableDecopBoolean':
        return self._auto_enable

    def store_config(self) -> None:
        self.__client.exec(self.__name + ':store-config')


class Thermistor:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name

    def get(self) -> Tuple[bool, float, float, float, float, float, float]:
        return self.__client.get(self.__name)

    def set(self, polynomial: bool, a0: float, a1: float, a2: float, a3: float, a4: float, a5: float) -> None:
        assert isinstance(polynomial, bool), f"expected type 'bool' for 'polynomial', got '{type(polynomial)}'"
        assert isinstance(a0, float), f"expected type 'float' for 'a0', got '{type(a0)}'"
        assert isinstance(a1, float), f"expected type 'float' for 'a1', got '{type(a1)}'"
        assert isinstance(a2, float), f"expected type 'float' for 'a2', got '{type(a2)}'"
        assert isinstance(a3, float), f"expected type 'float' for 'a3', got '{type(a3)}'"
        assert isinstance(a4, float), f"expected type 'float' for 'a4', got '{type(a4)}'"
        assert isinstance(a5, float), f"expected type 'float' for 'a5', got '{type(a5)}'"
        self.__client.set(self.__name, polynomial, a0, a1, a2, a3, a4, a5)


class Powermon:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._int = DecopReal(client, name + ':int')
        self._int_2 = DecopReal(client, name + ':int-2')
        self._cal = DecopReal(client, name + ':cal')
        self._splitter = DecopReal(client, name + ':splitter')
        self._fiber = DecopReal(client, name + ':fiber')
        self._ext = DecopReal(client, name + ':ext')
        self._ext_bandwidth = MutableDecopInteger(client, name + ':ext-bandwidth')
        self._signal = DecopReal(client, name + ':signal')
        self._signal_source = MutableDecopString(client, name + ':signal-source')
        self._ext_address = MutableDecopString(client, name + ':ext-address')
        self._ext_wavelength = MutableDecopReal(client, name + ':ext-wavelength')
        self._ext_udelay = MutableDecopInteger(client, name + ':ext-udelay')

    @property
    def int(self) -> 'DecopReal':
        return self._int

    @property
    def int_2(self) -> 'DecopReal':
        return self._int_2

    @property
    def cal(self) -> 'DecopReal':
        return self._cal

    @property
    def splitter(self) -> 'DecopReal':
        return self._splitter

    @property
    def fiber(self) -> 'DecopReal':
        return self._fiber

    @property
    def ext(self) -> 'DecopReal':
        return self._ext

    @property
    def ext_bandwidth(self) -> 'MutableDecopInteger':
        return self._ext_bandwidth

    @property
    def signal(self) -> 'DecopReal':
        return self._signal

    @property
    def signal_source(self) -> 'MutableDecopString':
        return self._signal_source

    @property
    def ext_address(self) -> 'MutableDecopString':
        return self._ext_address

    @property
    def ext_wavelength(self) -> 'MutableDecopReal':
        return self._ext_wavelength

    @property
    def ext_udelay(self) -> 'MutableDecopInteger':
        return self._ext_udelay


class Adg2188:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._close_all = DecopInteger(client, name + ':close-all')

    @property
    def close_all(self) -> 'DecopInteger':
        return self._close_all


class Shutter:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._available = DecopBoolean(client, name + ':available')
        self._cmd = MutableDecopBoolean(client, name + ':cmd')
        self._fp_input_enabled = MutableDecopBoolean(client, name + ':fp-input-enabled')
        self._fp_input = DecopBoolean(client, name + ':fp-input')
        self._open = DecopBoolean(client, name + ':open')
        self._delay = MutableDecopInteger(client, name + ':delay')

    @property
    def available(self) -> 'DecopBoolean':
        return self._available

    @property
    def cmd(self) -> 'MutableDecopBoolean':
        return self._cmd

    @property
    def fp_input_enabled(self) -> 'MutableDecopBoolean':
        return self._fp_input_enabled

    @property
    def fp_input(self) -> 'DecopBoolean':
        return self._fp_input

    @property
    def open(self) -> 'DecopBoolean':
        return self._open

    @property
    def delay(self) -> 'MutableDecopInteger':
        return self._delay

    def store_config(self) -> None:
        self.__client.exec(self.__name + ':store-config')


class Switch:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._raw_trigger = DecopBoolean(client, name + ':raw-trigger')
        self._trigger = DecopBoolean(client, name + ':trigger')
        self._level = DecopReal(client, name + ':level')
        self._ad_value = DecopInteger(client, name + ':ad-value')
        self._ad_offset = MutableDecopInteger(client, name + ':ad-offset')

    @property
    def raw_trigger(self) -> 'DecopBoolean':
        return self._raw_trigger

    @property
    def trigger(self) -> 'DecopBoolean':
        return self._trigger

    @property
    def level(self) -> 'DecopReal':
        return self._level

    @property
    def ad_value(self) -> 'DecopInteger':
        return self._ad_value

    @property
    def ad_offset(self) -> 'MutableDecopInteger':
        return self._ad_offset

    def determine_ad_offset(self) -> None:
        self.__client.exec(self.__name + ':determine-ad-offset')

    def store_config(self) -> None:
        self.__client.exec(self.__name + ':store-config')


class Buzzer:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._welcome = MutableDecopString(client, name + ':welcome')

    @property
    def welcome(self) -> 'MutableDecopString':
        return self._welcome

    def play_welcome(self) -> None:
        self.__client.exec(self.__name + ':play-welcome')

    def play(self, melody: str) -> None:
        assert isinstance(melody, str), f"expected type 'str' for parameter 'melody', got '{type(melody)}'"
        self.__client.exec(self.__name + ':play', melody)


class Laserclass:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._released = DecopBoolean(client, name + ':released')
        self._status = DecopInteger(client, name + ':status')
        self._type = MutableDecopInteger(client, name + ':type')
        self._interlock_emergency = DecopBoolean(client, name + ':interlock-emergency')

    @property
    def released(self) -> 'DecopBoolean':
        return self._released

    @property
    def status(self) -> 'DecopInteger':
        return self._status

    @property
    def type(self) -> 'MutableDecopInteger':
        return self._type

    @property
    def interlock_emergency(self) -> 'DecopBoolean':
        return self._interlock_emergency


class Ipconfig:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._ip_addr = DecopString(client, name + ':ip-addr')
        self._net_mask = DecopString(client, name + ':net-mask')
        self._mac_addr = DecopString(client, name + ':mac-addr')
        self._dhcp = DecopBoolean(client, name + ':dhcp')
        self._cmd_port = DecopInteger(client, name + ':cmd-port')
        self._mon_port = DecopInteger(client, name + ':mon-port')
        self._secondary_controller = IpconfigSecController(client, name + ':secondary-controller')

    @property
    def ip_addr(self) -> 'DecopString':
        return self._ip_addr

    @property
    def net_mask(self) -> 'DecopString':
        return self._net_mask

    @property
    def mac_addr(self) -> 'DecopString':
        return self._mac_addr

    @property
    def dhcp(self) -> 'DecopBoolean':
        return self._dhcp

    @property
    def cmd_port(self) -> 'DecopInteger':
        return self._cmd_port

    @property
    def mon_port(self) -> 'DecopInteger':
        return self._mon_port

    @property
    def secondary_controller(self) -> 'IpconfigSecController':
        return self._secondary_controller

    def set_dhcp(self) -> None:
        self.__client.exec(self.__name + ':set-dhcp')

    def set_ip(self, ip_addr: str, net_mask: str) -> None:
        assert isinstance(ip_addr, str), f"expected type 'str' for parameter 'ip_addr', got '{type(ip_addr)}'"
        assert isinstance(net_mask, str), f"expected type 'str' for parameter 'net_mask', got '{type(net_mask)}'"
        self.__client.exec(self.__name + ':set-ip', ip_addr, net_mask)

    def apply(self) -> None:
        self.__client.exec(self.__name + ':apply')


class IpconfigSecController:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._ip_addr = DecopString(client, name + ':ip-addr')
        self._net_mask = DecopString(client, name + ':net-mask')
        self._mac_addr = DecopString(client, name + ':mac-addr')
        self._dhcp = DecopBoolean(client, name + ':dhcp')

    @property
    def ip_addr(self) -> 'DecopString':
        return self._ip_addr

    @property
    def net_mask(self) -> 'DecopString':
        return self._net_mask

    @property
    def mac_addr(self) -> 'DecopString':
        return self._mac_addr

    @property
    def dhcp(self) -> 'DecopBoolean':
        return self._dhcp


class Optparams:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._initial_stepsize = MutableDecopInteger(client, name + ':initial-stepsize')
        self._minimum_stepsize = MutableDecopInteger(client, name + ':minimum-stepsize')
        self._min_power_ext = MutableDecopReal(client, name + ':min-power-ext')
        self._min_power_fiber = MutableDecopReal(client, name + ':min-power-fiber')
        self._min_power_cal = MutableDecopInteger(client, name + ':min-power-cal')
        self._debug = MutableDecopBoolean(client, name + ':debug')
        self._step_delay = MutableDecopInteger(client, name + ':step-delay')
        self._averaging = MutableDecopInteger(client, name + ':averaging')

    @property
    def initial_stepsize(self) -> 'MutableDecopInteger':
        return self._initial_stepsize

    @property
    def minimum_stepsize(self) -> 'MutableDecopInteger':
        return self._minimum_stepsize

    @property
    def min_power_ext(self) -> 'MutableDecopReal':
        return self._min_power_ext

    @property
    def min_power_fiber(self) -> 'MutableDecopReal':
        return self._min_power_fiber

    @property
    def min_power_cal(self) -> 'MutableDecopInteger':
        return self._min_power_cal

    @property
    def debug(self) -> 'MutableDecopBoolean':
        return self._debug

    @property
    def step_delay(self) -> 'MutableDecopInteger':
        return self._step_delay

    @property
    def averaging(self) -> 'MutableDecopInteger':
        return self._averaging

    def store_config(self) -> None:
        self.__client.exec(self.__name + ':store-config')


class Scripts:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._boot = Script(client, name + ':boot')
        self._console = Script(client, name + ':console')
        self._misc = Script(client, name + ':misc')

    @property
    def boot(self) -> 'Script':
        return self._boot

    @property
    def console(self) -> 'Script':
        return self._console

    @property
    def misc(self) -> 'Script':
        return self._misc


class Script:
    def __init__(self, client: Client, name: str) -> None:
        self.__client = client
        self.__name = name
        self._busy = DecopBoolean(client, name + ':busy')
        self._size = DecopInteger(client, name + ':size')

    @property
    def busy(self) -> 'DecopBoolean':
        return self._busy

    @property
    def size(self) -> 'DecopInteger':
        return self._size

    def txt(self) -> str:
        return self.__client.exec(self.__name + ':txt', return_type=str)

    def disp(self) -> str:
        return self.__client.exec(self.__name + ':disp', output_type=str)

    def store(self, newtxt: str) -> None:
        assert isinstance(newtxt, str), f"expected type 'str' for parameter 'newtxt', got '{type(newtxt)}'"
        self.__client.exec(self.__name + ':store', newtxt)

    def read(self) -> bytes:
        return self.__client.exec(self.__name + ':read', output_type=bytes)

    def write(self, input_stream: bytes) -> None:
        assert isinstance(input_stream, bytes), f"expected type 'bytes' for parameter 'input_stream', got '{type(input_stream)}'"
        self.__client.exec(self.__name + ':write', input_stream=input_stream)

    def exec(self) -> None:
        self.__client.exec(self.__name + ':exec')

    def start(self) -> None:
        self.__client.exec(self.__name + ':start')

    def stop(self) -> None:
        self.__client.exec(self.__name + ':stop')


class FLE:
    def __init__(self, connection: Connection) -> None:
        self.__client = Client(connection)
        self._laser1 = Laser(self.__client, 'laser1')
        self._laser2 = Laser(self.__client, 'laser2')
        self._laser3 = Laser(self.__client, 'laser3')
        self._laser4 = Laser(self.__client, 'laser4')
        self._laser5 = Laser(self.__client, 'laser5')
        self._laser6 = Laser(self.__client, 'laser6')
        self._laser7 = Laser(self.__client, 'laser7')
        self._all = AllLasers(self.__client, 'all')
        self._tec_d = Tec(self.__client, 'tec-d')
        self._tec_l = Tec(self.__client, 'tec-l')
        self._dx5100 = Dx5100(self.__client, 'dx5100')
        self._tec_c = TecDx(self.__client, 'tec-c')
        self._tec_p = TecDx(self.__client, 'tec-p')
        self._powermon = Powermon(self.__client, 'powermon')
        self._interlock = DecopBoolean(self.__client, 'interlock')
        self._adg2188_digital = Adg2188(self.__client, 'adg2188-digital')
        self._adg2188_analog = Adg2188(self.__client, 'adg2188-analog')
        self._shutter1 = Shutter(self.__client, 'shutter1')
        self._shutter2 = Shutter(self.__client, 'shutter2')
        self._switch = Switch(self.__client, 'switch')
        self._voltage = DecopReal(self.__client, 'voltage')
        self._current = DecopReal(self.__client, 'current')
        self._base_temp = DecopReal(self.__client, 'base-temp')
        self._ambient_temp = DecopReal(self.__client, 'ambient-temp')
        self._buzzer = Buzzer(self.__client, 'buzzer')
        self._tan = DecopInteger(self.__client, 'tan')
        self._uptime = DecopInteger(self.__client, 'uptime')
        self._uptime_txt = DecopString(self.__client, 'uptime-txt')
        self._time = MutableDecopString(self.__client, 'time')
        self._fw_ver = DecopString(self.__client, 'fw-ver')
        self._fw_ver_secondary_controller = DecopString(self.__client, 'fw-ver-secondary-controller')
        self._decof_ver = DecopString(self.__client, 'decof-ver')
        self._system_software = DecopString(self.__client, 'system-software')
        self._serial_number = DecopString(self.__client, 'serial-number')
        self._hostname = MutableDecopString(self.__client, 'hostname')
        self._system_type = DecopString(self.__client, 'system-type')
        self._system_model = DecopString(self.__client, 'system-model')
        self._system_label = MutableDecopString(self.__client, 'system-label')
        self._ul = MutableDecopInteger(self.__client, 'ul')
        self._laser_class = Laserclass(self.__client, 'laser-class')
        self._net_conf = Ipconfig(self.__client, 'net-conf')
        self._echo = MutableDecopBoolean(self.__client, 'echo')
        self._opt_params = Optparams(self.__client, 'opt-params')
        self._sw_watchdog_enable = MutableDecopBoolean(self.__client, 'sw-watchdog-enable')
        self._sw_watchdog_counter = DecopInteger(self.__client, 'sw-watchdog-counter')
        self._sw_watchdog_loop = DecopInteger(self.__client, 'sw-watchdog-loop')
        self._sw_watchdog_last = DecopInteger(self.__client, 'sw-watchdog-last')
        self._script = Scripts(self.__client, 'script')

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args):
        self.close()

    def open(self) -> None:
        self.__client.open()

    def close(self) -> None:
        self.__client.close()

    def run(self, timeout: int = None) -> None:
        self.__client.run(timeout)

    def stop(self) -> None:
        self.__client.stop()

    def poll(self) -> None:
        self.__client.poll()

    @property
    def laser1(self) -> 'Laser':
        return self._laser1

    @property
    def laser2(self) -> 'Laser':
        return self._laser2

    @property
    def laser3(self) -> 'Laser':
        return self._laser3

    @property
    def laser4(self) -> 'Laser':
        return self._laser4

    @property
    def laser5(self) -> 'Laser':
        return self._laser5

    @property
    def laser6(self) -> 'Laser':
        return self._laser6

    @property
    def laser7(self) -> 'Laser':
        return self._laser7

    @property
    def all(self) -> 'AllLasers':
        return self._all

    @property
    def tec_d(self) -> 'Tec':
        return self._tec_d

    @property
    def tec_l(self) -> 'Tec':
        return self._tec_l

    @property
    def dx5100(self) -> 'Dx5100':
        return self._dx5100

    @property
    def tec_c(self) -> 'TecDx':
        return self._tec_c

    @property
    def tec_p(self) -> 'TecDx':
        return self._tec_p

    @property
    def powermon(self) -> 'Powermon':
        return self._powermon

    @property
    def interlock(self) -> 'DecopBoolean':
        return self._interlock

    @property
    def adg2188_digital(self) -> 'Adg2188':
        return self._adg2188_digital

    @property
    def adg2188_analog(self) -> 'Adg2188':
        return self._adg2188_analog

    @property
    def shutter1(self) -> 'Shutter':
        return self._shutter1

    @property
    def shutter2(self) -> 'Shutter':
        return self._shutter2

    @property
    def switch(self) -> 'Switch':
        return self._switch

    @property
    def voltage(self) -> 'DecopReal':
        return self._voltage

    @property
    def current(self) -> 'DecopReal':
        return self._current

    @property
    def base_temp(self) -> 'DecopReal':
        return self._base_temp

    @property
    def ambient_temp(self) -> 'DecopReal':
        return self._ambient_temp

    @property
    def buzzer(self) -> 'Buzzer':
        return self._buzzer

    @property
    def tan(self) -> 'DecopInteger':
        return self._tan

    @property
    def uptime(self) -> 'DecopInteger':
        return self._uptime

    @property
    def uptime_txt(self) -> 'DecopString':
        return self._uptime_txt

    @property
    def time(self) -> 'MutableDecopString':
        return self._time

    @property
    def fw_ver(self) -> 'DecopString':
        return self._fw_ver

    @property
    def fw_ver_secondary_controller(self) -> 'DecopString':
        return self._fw_ver_secondary_controller

    @property
    def decof_ver(self) -> 'DecopString':
        return self._decof_ver

    @property
    def system_software(self) -> 'DecopString':
        return self._system_software

    @property
    def serial_number(self) -> 'DecopString':
        return self._serial_number

    @property
    def hostname(self) -> 'MutableDecopString':
        return self._hostname

    @property
    def system_type(self) -> 'DecopString':
        return self._system_type

    @property
    def system_model(self) -> 'DecopString':
        return self._system_model

    @property
    def system_label(self) -> 'MutableDecopString':
        return self._system_label

    @property
    def ul(self) -> 'MutableDecopInteger':
        return self._ul

    @property
    def laser_class(self) -> 'Laserclass':
        return self._laser_class

    @property
    def net_conf(self) -> 'Ipconfig':
        return self._net_conf

    @property
    def echo(self) -> 'MutableDecopBoolean':
        return self._echo

    @property
    def opt_params(self) -> 'Optparams':
        return self._opt_params

    @property
    def sw_watchdog_enable(self) -> 'MutableDecopBoolean':
        return self._sw_watchdog_enable

    @property
    def sw_watchdog_counter(self) -> 'DecopInteger':
        return self._sw_watchdog_counter

    @property
    def sw_watchdog_loop(self) -> 'DecopInteger':
        return self._sw_watchdog_loop

    @property
    def sw_watchdog_last(self) -> 'DecopInteger':
        return self._sw_watchdog_last

    @property
    def script(self) -> 'Scripts':
        return self._script

    def hello(self) -> None:
        self.__client.exec('hello')

    def fw_update(self, input_stream: bytes) -> None:
        assert isinstance(input_stream, bytes), f"expected type 'bytes' for parameter 'input_stream', got '{type(input_stream)}'"
        self.__client.exec('fw-update', input_stream=input_stream)

    def save_counters(self) -> int:
        return self.__client.exec('save-counters', return_type=int)

    def debuglog(self) -> str:
        return self.__client.exec('debuglog', output_type=str)

    def servicelog(self) -> str:
        return self.__client.exec('servicelog', output_type=str)

    def errorlog(self) -> str:
        return self.__client.exec('errorlog', output_type=str)

    def summary(self) -> str:
        return self.__client.exec('summary', output_type=str)

    def service_report(self) -> bytes:
        return self.__client.exec('service-report', output_type=bytes)

    def restore_factory_settings(self) -> None:
        self.__client.exec('restore-factory-settings')

    def reboot_device(self) -> None:
        self.__client.exec('reboot-device')

    def change_ul(self, ul: UserLevel, password: Optional[str] = None) -> int:
        assert isinstance(ul, UserLevel), f"expected type 'UserLevel' for parameter 'ul', got '{type(ul)}'"
        assert isinstance(password, str) or password is None, f"expected type 'str' or 'None' for parameter 'password', got '{type(password)}'"
        return self.__client.change_ul(ul, password)

    def change_password(self, passwd: str) -> None:
        assert isinstance(passwd, str), f"expected type 'str' for parameter 'passwd', got '{type(passwd)}'"
        self.__client.exec('change-password', passwd)

    def read_config(self) -> bytes:
        return self.__client.exec('read-config', output_type=bytes)

    def read_config_slave(self) -> bytes:
        return self.__client.exec('read-config-slave', output_type=bytes)

