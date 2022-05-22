from typing import Optional, Union



class Debugger:
    ...

class Csv:
    def __init__(
        self, path, name, debugger: Union[Debugger, Optional[None]] = Debugger
    ) -> None:
        ...
