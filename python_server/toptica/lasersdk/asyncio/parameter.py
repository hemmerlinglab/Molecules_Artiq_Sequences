from __future__ import annotations

from typing import Optional
from typing import Union

from typing import TYPE_CHECKING
from typing import cast

if TYPE_CHECKING:
    from .client import Client
    from .client import Subscription

__all__ = [

    'DecopBinary',
    'DecopBoolean',
    'DecopInteger',
    'DecopReal',
    'DecopString',

    'MutableDecopBinary',
    'MutableDecopBoolean',
    'MutableDecopInteger',
    'MutableDecopReal',
    'MutableDecopString',

    'SettableDecopBinary',
    'SettableDecopBoolean',
    'SettableDecopInteger',
    'SettableDecopReal',
    'SettableDecopString',
]


class DecopBoolean:
    """A read-only boolean parameter.

    Args:
        client (Client):
            A client that is used to access the parameter.

        name (str):
            The fully qualified name of the parameter (e.g. 'laser1:amp:ontime').

    """

    def __init__(self, client: Client, name: str) -> None:
        self._client = client
        self._name = name

    @property
    def name(self) -> str:
        """str: The fully qualified name of the parameter."""
        return self._name

    async def get(self) -> bool:
        """Returns the current value of the parameter.

        Returns:
            bool: The current value of the parameter.

        """
        result = cast(bool, await self._client.get(self._name, bool))
        return result

    async def subscribe(self, interval: Optional[int] = None) -> Subscription:
        """Creates a subscription to the value changes of the parameter.

        Args:
            interval (Optional[int]):
                The minimum update interval (in milliseconds).

        Returns:
            Subscription: A subscription to the value changes of the parameter.

        """
        return await self._client.subscribe(self._name, bool, interval)


class MutableDecopBoolean:
    """A read/write DeCoP boolean parameter.

    Args:
        client (Client):
            A DeCoP client that is used to access the parameter on a device.

        name (str):
            The fully qualified name of the parameter (e.g. 'laser1:amp:ontime').

    """

    def __init__(self, client: Client, name: str) -> None:
        self._client = client
        self._name = name

    @property
    def name(self) -> str:
        """str: The fully qualified name of the parameter."""
        return self._name

    async def get(self) -> bool:
        """Returns the current value of the parameter.

        Returns:
            bool: The current value of the parameter.

        """
        result = cast(bool, await self._client.get(self._name, bool))
        return result

    async def set(self, value: bool) -> int:
        """Updates the value of the parameter.

        Args:
            value (bool): The new value of the parameter.

        Returns:
            int: Zero if successful or a positive integer indicating a warning.

        Raises:
            UnavailableError: If the connection is closed or the command line is not available.
            DecopError: If the device returned an error when setting the new value.

        """
        assert isinstance(value, bool), f"expected type 'bool' for 'value', got '{type(value)}'"
        return await self._client.set(self._name, value)

    async def subscribe(self, interval: Optional[int] = None) -> Subscription:
        """Creates a subscription to the value changes of the parameter.

        Args:
            interval (Optional[int]):
                The minimum update interval (in milliseconds).

        Returns:
            Subscription: A subscription to the value changes of the parameter.

        """
        return await self._client.subscribe(self._name, bool, interval)


class SettableDecopBoolean:
    """A settable DeCoP boolean parameter.

    Args:
        client (Client):
            A DeCoP client that is used to access the parameter on a device.

        name (str):
            The fully qualified name of the parameter (e.g. 'laser1:amp:ontime').

    """

    def __init__(self, client: Client, name: str) -> None:
        self._client = client
        self._name = name

    @property
    def name(self) -> str:
        """str: The fully qualified name of the parameter."""
        return self._name

    async def get(self) -> bool:
        """Returns the current value of the parameter.

        Returns:
            bool: The current value of the parameter.

        """
        result = cast(bool, await self._client.get(self._name, bool))
        return result

    async def get_set_value(self) -> bool:
        """Returns the current set-value of the parameter.

        Returns:
            bool: The current set-value of the parameter.

        """
        result = cast(bool, await self._client.get_set_value(self._name, bool))
        return result

    async def set(self, value: bool) -> int:
        """Updates the value of the parameter.

        Args:
            value (bool): The new value of the parameter.

        Returns:
            int: Zero if successful or a positive integer indicating a warning.

        Raises:
            UnavailableError: If the connection is closed or the command line is not available.
            DecopError: If the device returned an error when setting the new value.

        """
        assert isinstance(value, bool), f"expected type 'bool' for 'value', got '{type(value)}'"
        return await self._client.set(self._name, value)

    async def subscribe(self, interval: Optional[int] = None) -> Subscription:
        """Creates a subscription to the value changes of the parameter.

        Args:
            interval (Optional[int]):
                The minimum update interval (in milliseconds).

        Returns:
            Subscription: A subscription to the value changes of the parameter.

        """
        return await self._client.subscribe(self._name, bool, interval)


class DecopInteger:
    """A read-only DeCoP integer parameter.

    Args:
        client (Client):
            A DeCoP client that is used to access the parameter on a device.

        name (str):
            The fully qualified name of the parameter (e.g. 'laser1:amp:ontime').

    """

    def __init__(self, client: Client, name: str) -> None:
        self._client = client
        self._name = name

    @property
    def name(self) -> str:
        """str: The fully qualified name of the parameter."""
        return self._name

    async def get(self) -> int:
        """Returns the current value of the parameter.

        Returns:
            int: The current value of the parameter.

        """
        result = cast(int, await self._client.get(self._name, int))
        return result

    async def subscribe(self, interval: Optional[int] = None, threshold: Optional[int] = None) -> Subscription:
        """Creates a subscription to the value changes of the parameter.

        Args:
            interval (Optional[int]):
                The minimum update interval (in milliseconds).

            threshold (Optional[int]):
                The minimum change of the value for an update.

        Returns:
            Subscription: A subscription to the value changes of the parameter.

        """
        return await self._client.subscribe(self._name, int, interval, threshold)


class MutableDecopInteger:
    """A read/write DeCoP integer parameter.

    Args:
        client (Client):
            A DeCoP client that is used to access the parameter on a device.

        name (str):
            The fully qualified name of the parameter (e.g. 'laser1:amp:ontime').

    """

    def __init__(self, client: Client, name: str) -> None:
        self._client = client
        self._name = name

    @property
    def name(self) -> str:
        """str: The fully qualified name of the parameter."""
        return self._name

    async def get(self) -> int:
        """Returns the current value of the parameter.

        Returns:
            int: The current value of the parameter.

        """
        result = cast(int, await self._client.get(self._name, int))
        return result

    async def set(self, value: int) -> int:
        """Updates the value of the parameter.

        Args:
            value (int): The new value of the parameter.

        Returns:
            int: Zero if successful or a positive integer indicating a warning.

        Raises:
            UnavailableError: If the connection is closed or the command line is not available.
            DecopError: If the device returned an error when setting the new value.

        """
        assert isinstance(value, int), f"expected type 'int' for 'value', got '{type(value)}'"
        return await self._client.set(self._name, value)

    async def subscribe(self, interval: Optional[int] = None, threshold: Optional[int] = None) -> Subscription:
        """Creates a subscription to the value changes of the parameter.

        Args:
            interval (Optional[int]):
                The minimum update interval (in milliseconds).

            threshold (Optional[int]):
                The minimum change of the value for an update.

        Returns:
            Subscription: A subscription to the value changes of the parameter.

        """
        return await self._client.subscribe(self._name, int, interval, threshold)


class SettableDecopInteger:
    """A settable DeCoP integer parameter.

    Args:
        client (Client):
            A DeCoP client that is used to access the parameter on a device.

        name (str):
            The fully qualified name of the parameter (e.g. 'laser1:amp:ontime').

    """

    def __init__(self, client: Client, name: str) -> None:
        self._client = client
        self._name = name

    @property
    def name(self) -> str:
        """str: The fully qualified name of the parameter."""
        return self._name

    async def get(self) -> int:
        """Returns the current value of the parameter.

        Returns:
            int: The current value of the parameter.

        """
        result = cast(int, await self._client.get(self._name, int))
        return result

    async def get_set_value(self) -> int:
        """Returns the current set-value of the parameter.

        Returns:
            int: The current set-value of the parameter.

        """
        result = cast(int, await self._client.get_set_value(self._name, int))
        return result

    async def set(self, value: int) -> int:
        """Updates the value of the parameter.

        Args:
            value (int): The new value of the parameter.

        Returns:
            int: Zero if successful or a positive integer indicating a warning.

        Raises:
            UnavailableError: If the connection is closed or the command line is not available.
            DecopError: If the device returned an error when setting the new value.

        """
        assert isinstance(value, int), f"expected type 'int' for 'value', got '{type(value)}'"
        return await self._client.set(self._name, value)

    async def subscribe(self, interval: Optional[int] = None, threshold: Optional[int] = None) -> Subscription:
        """Creates a subscription to the value changes of the parameter.

        Args:
            interval (Optional[int]):
                The minimum update interval (in milliseconds).

            threshold (Optional[int]):
                The minimum change of the value for an update.

        Returns:
            Subscription: A subscription to the value changes of the parameter.

        """
        return await self._client.subscribe(self._name, int, interval, threshold)


class DecopReal:
    """A read-only DeCoP floating point parameter.

    Args:
        client (Client):
            A DeCoP client that is used to access the parameter on a device.

        name (str):
            The fully qualified name of the parameter (e.g. 'laser1:amp:ontime').

    """

    def __init__(self, client: Client, name: str) -> None:
        self._client = client
        self._name = name

    @property
    def name(self) -> str:
        """str: The fully qualified name of the parameter."""
        return self._name

    async def get(self) -> float:
        """Returns the current value of the parameter.

        Returns:
            float: The current value of the parameter.

        """
        result = cast(float, await self._client.get(self._name, float))
        return result

    async def subscribe(self, interval: Optional[int] = None, threshold: Optional[float] = None) -> Subscription:
        """Creates a subscription to the value changes of the parameter.

        Args:
            interval (Optional[int]):
                The minimum update interval (in milliseconds).

            threshold (Optional[float]):
                The minimum change of the value for an update.

        Returns:
            Subscription: A subscription to updates of the parameter.

        """
        return await self._client.subscribe(self._name, float, interval, threshold)


class MutableDecopReal:
    """A read/write DeCoP floating point parameter.

    Args:
        client (Client):
            A DeCoP client that is used to access the parameter on a device.

        name (str):
            The fully qualified name of the parameter (e.g. 'laser1:amp:ontime').

    """

    def __init__(self, client: Client, name: str) -> None:
        self._client = client
        self._name = name

    @property
    def name(self) -> str:
        """str: The fully qualified name of the parameter."""
        return self._name

    async def get(self) -> float:
        """Returns the current value of the parameter.

        Returns:
            float: The current value of the parameter.

        """
        result = cast(float, await self._client.get(self._name, float))
        return result

    async def set(self, value: Union[int, float]) -> int:
        """Updates the value of the parameter.

        Args:
            value Union[int, float]: The new value of the parameter.

        Returns:
            int: Zero if successful or a positive integer indicating a warning.

        Raises:
            UnavailableError: If the connection is closed or the command line is not available.
            DecopError: If the device returned an error when setting the new value.

        """
        assert isinstance(value, (int, float)), f"expected type 'int' or 'float' for 'value', got '{type(value)}'"
        return await self._client.set(self._name, float(value))

    async def subscribe(self, interval: Optional[int] = None, threshold: Optional[float] = None) -> Subscription:
        """Creates a subscription to the value changes of the parameter.

        Args:
            interval (Optional[int]):
                The minimum update interval (in milliseconds).

            threshold (Optional[float]):
                The minimum change of the value for an update.

        Returns:
            Subscription: A subscription to the value changes of the parameter.

        """
        return await self._client.subscribe(self._name, float, interval, threshold)


class SettableDecopReal:
    """A settable DeCoP floating point parameter.

    Args:
        client (Client):
            A DeCoP client that is used to access the parameter on a device.

        name (str):
            The fully qualified name of the parameter (e.g. 'laser1:amp:ontime').

    """

    def __init__(self, client: Client, name: str) -> None:
        self._client = client
        self._name = name

    @property
    def name(self) -> str:
        """str: The fully qualified name of the parameter."""
        return self._name

    async def get(self) -> float:
        """Returns the current value of the parameter.

        Returns:
            float: The current value of the parameter.

        """
        result = cast(float, await self._client.get(self._name, float))
        return result

    async def get_set_value(self) -> float:
        """Returns the current set-value of the parameter.

        Returns:
            float: The current set-value of the parameter.

        """
        result = cast(float, await self._client.get_set_value(self._name, float))
        return result

    async def set(self, value: Union[int, float]) -> int:
        """Updates the value of the parameter.

        Args:
            value Union[int, float]: The new value of the parameter.

        Returns:
            int: Zero if successful or a positive integer indicating a warning.

        Raises:
            UnavailableError: If the connection is closed or the command line is not available.
            DecopError: If the device returned an error when setting the new value.

        """
        assert isinstance(value, (int, float)), f"expected type 'int' or 'float' for 'value', got '{type(value)}'"
        return await self._client.set(self._name, float(value))

    async def subscribe(self, interval: Optional[int] = None, threshold: Optional[float] = None) -> Subscription:
        """Creates a subscription to the value changes of the parameter.

        Args:
            interval (Optional[int]):
                The minimum update interval (in milliseconds).

            threshold (Optional[float]):
                The minimum change of the value for an update.

        Returns:
            Subscription: A subscription to the value changes of the parameter.

        """
        return await self._client.subscribe(self._name, float, interval, threshold)


class DecopString:
    """A read-only DeCoP string parameter.

    Args:
        client (Client):
            A DeCoP client that is used to access the parameter on a device.

        name (str):
            The fully qualified name of the parameter (e.g. 'laser1:amp:ontime').

    """

    def __init__(self, client: Client, name: str) -> None:
        self._client = client
        self._name = name

    @property
    def name(self) -> str:
        """str: The fully qualified name of the parameter."""
        return self._name

    async def get(self) -> str:
        """Returns the current value of the parameter.

        Returns:
            str: The current value of the parameter.

        """
        result = cast(str, await self._client.get(self._name, str))
        return result

    async def subscribe(self, interval: Optional[int] = None) -> Subscription:
        """Creates a subscription to the value changes of the parameter.

        Args:
            interval (Optional[int]):
                The minimum update interval (in milliseconds).

        Returns:
            Subscription: A subscription to the value changes of the parameter.

        """
        return await self._client.subscribe(self._name, str, interval)


class MutableDecopString:
    """A read/write DeCoP string parameter.

    Args:
        client (Client):
            A DeCoP client that is used to access the parameter on a device.

        name (str):
            The fully qualified name of the parameter (e.g. 'laser1:amp:ontime').

    """

    def __init__(self, client: Client, name: str) -> None:
        self._client = client
        self._name = name

    @property
    def name(self) -> str:
        """str: The fully qualified name of the parameter."""
        return self._name

    async def get(self) -> str:
        """Returns the current value of the parameter.

        Returns:
            str: The current value of the parameter.

        """
        result = cast(str, await self._client.get(self._name, str))
        return result

    async def set(self, value: str) -> int:
        """Updates the value of the parameter.

        Args:
            value (str): The new value of the parameter.

        Returns:
            int: Zero if successful or a positive integer indicating a warning.

        Raises:
            UnavailableError: If the connection is closed or the command line is not available.
            DecopError: If the device returned an error when setting the new value.

        """
        assert isinstance(value, str), f"expected type 'str' for 'value', got '{type(value)}'"
        return await self._client.set(self._name, value)

    async def subscribe(self, interval: Optional[int] = None) -> Subscription:
        """Creates a subscription to the value changes of the parameter.

        Args:
            interval (Optional[int]):
                The minimum update interval (in milliseconds).

        Returns:
            Subscription: A subscription to the value changes of the parameter.

        """
        return await self._client.subscribe(self._name, str, interval)


class SettableDecopString:
    """A settable DeCoP string parameter.

    Args:
        client (Client):
            A DeCoP client that is used to access the parameter on a device.

        name (str):
            The fully qualified name of the parameter (e.g. 'laser1:amp:ontime').

    """

    def __init__(self, client: Client, name: str) -> None:
        self._client = client
        self._name = name

    @property
    def name(self) -> str:
        """str: The fully qualified name of the parameter."""
        return self._name

    async def get(self) -> str:
        """Returns the current value of the parameter.

        Returns:
            str: The current value of the parameter.

        """
        result = cast(str, await self._client.get(self._name, str))
        return result

    async def get_set_value(self) -> str:
        """Returns the current set-value of the parameter.

        Returns:
            str: The current set-value of the parameter.

        """
        result = cast(str, await self._client.get_set_value(self._name, str))
        return result

    async def set(self, value: str) -> int:
        """Updates the value of the parameter.

        Args:
            value (str): The new value of the parameter.

        Returns:
            int: Zero if successful or a positive integer indicating a warning.

        Raises:
            UnavailableError: If the connection is closed or the command line is not available.
            DecopError: If the device returned an error when setting the new value.

        """
        assert isinstance(value, str), f"expected type 'str' for 'value', got '{type(value)}'"
        return await self._client.set(self._name, value)

    async def subscribe(self, interval: Optional[int] = None) -> Subscription:
        """Creates a subscription to the value changes of the parameter.

        Args:
            interval (Optional[int]):
                The minimum update interval (in milliseconds).

        Returns:
            Subscription: A subscription to the value changes of the parameter.

        """
        return await self._client.subscribe(self._name, str, interval)


class DecopBinary:
    """A read-only DeCoP binary parameter.

    Args:
        client (Client):
            A DeCoP client that is used to access the parameter on a device.

        name (str):
            The fully qualified name of the parameter (e.g. 'laser1:amp:ontime').

    """

    def __init__(self, client: Client, name: str) -> None:
        self._client = client
        self._name = name

    @property
    def name(self) -> str:
        """str: The fully qualified name of the parameter."""
        return self._name

    async def get(self) -> bytes:
        """Returns the current value of the parameter.

        Returns:
            bytes: The current value of the parameter.

        """
        result = cast(bytes, await self._client.get(self._name, bytes))
        return result

    async def subscribe(self, interval: Optional[int] = None) -> Subscription:
        """Creates a subscription to the value changes of the parameter.

        Args:
            interval (Optional[int]):
                The minimum update interval (in milliseconds).

        Returns:
            Subscription: A subscription to the value changes of the parameter.

        """
        return await self._client.subscribe(self._name, bytes, interval)


class MutableDecopBinary:
    """A read/write DeCoP binary parameter.

    Args:
        client (Client):
            A DeCoP client that is used to access the parameter on a device.

        name (str):
            The fully qualified name of the parameter (e.g. 'laser1:amp:ontime').

    """

    def __init__(self, client: Client, name: str) -> None:
        self._client = client
        self._name = name

    @property
    def name(self) -> str:
        """str: The fully qualified name of the parameter."""
        return self._name

    async def get(self) -> bytes:
        """Returns the current value of the parameter.

        Returns:
            bytes: The current value of the parameter.

        """
        result = cast(bytes, await self._client.get(self._name, bytes))
        return result

    async def set(self, value: Union[bytes, bytearray]) -> int:
        """Updates the value of the parameter.

        Args:
            value (Union[bytes, bytearray]): The new value of the parameter.

        Returns:
            int: Zero if successful or a positive integer indicating a warning.

        Raises:
            UnavailableError: If the connection is closed or the command line is not available.
            DecopError: If the device returned an error when setting the new value.

        """
        assert isinstance(value, (bytes, bytearray)), \
            f"expected type 'bytes' or 'bytearray' for 'value', got '{type(value)}'"
        return await self._client.set(self._name, value)

    async def subscribe(self, interval: Optional[int] = None) -> Subscription:
        """Creates a subscription to the value changes of the parameter.

        Args:
            interval (Optional[int]):
                The minimum update interval (in milliseconds).

        Returns:
            Subscription: A subscription to updates of the parameter.

        """
        return await self._client.subscribe(self._name, bytes, interval)


class SettableDecopBinary:
    """A settable DeCoP binary parameter.

     Args:
         client (Client):
            A DeCoP client that is used to access the parameter on a device

         name (str):
            The fully qualified name of the parameter (e.g. 'laser1:amp:ontime')

     """

    def __init__(self, client: Client, name: str) -> None:
        self._client = client
        self._name = name

    @property
    def name(self) -> str:
        """str: The fully qualified name of the parameter."""
        return self._name

    async def get(self) -> bytes:
        """Returns the current value of the parameter.

        Returns:
            bytes: The current value of the parameter.

        """
        result = cast(bytes, await self._client.get(self._name, bytes))
        return result

    async def get_set_value(self) -> bytes:
        """Returns the current set-value of the parameter.

        Returns:
            bytes: The current set-value of the parameter.

        """
        result = cast(bytes, await self._client.get_set_value(self._name, bytes))
        return result

    async def set(self, value: Union[bytes, bytearray]) -> int:
        """Updates the value of the parameter.

        Args:
            value (Union[bytes, bytearray]): The new value of the parameter.

        Returns:
            int: Zero if successful or a positive integer indicating a warning.

        Raises:
            UnavailableError: If the connection is closed or the command line is not available.
            DecopError: If the device returned an error when setting the new value.

        """
        assert isinstance(value, (bytes, bytearray)), \
            f"expected type 'bytes' or 'bytearray' for 'value', got '{type(value)}'"
        return await self._client.set(self._name, value)

    async def subscribe(self, interval: Optional[int] = None) -> Subscription:
        """Creates a subscription to the value changes of the parameter.

        Args:
            interval (Optional[int]):
                The minimum update interval (in milliseconds).

        Returns:
            Subscription: A subscription to the value changes of the parameter.

        """
        return await self._client.subscribe(self._name, bytes, interval)
