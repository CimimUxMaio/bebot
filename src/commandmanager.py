import exceptions


class ICommand():
    def __init__(self, func, **cmd_info):
        super().__init__()
        self.__name = func.__name__
        self.__description = cmd_info.get("description", "")
        self.__parameters = cmd_info.get("parameters", [])
        self.__optionals = cmd_info.get("optionals", [])
        self.__func = func
    
    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def shape_description_formated(self):
        name_str = f"**{self.__name}**"
        parameters_str = ' '.join([f"<{param_name}>" for param_name in self.__parameters])
        optionals_str = ' '.join([f"<{optional_name}, default={default}>" for optional_name, default in self.__optionals])
        return f"{name_str} {parameters_str} {optionals_str}"

    @property
    def parameters(self):
        return self.__parameters

    async def __call__(self, ctx, *args):
        self.check_parameters(args)
        await self.__func(ctx, *args)
        
    def check_parameters(self, args):
        if len(args) < len(self.parameters):
            missing = self.parameters[len(args):]
            raise exceptions.MissingParameters(*missing)
            


class ICommandManager:
    def __init__(self):
        self.__commands = {}

    @property
    def commands(self):
        return self.__commands

    def icommand(self, **cmd_info):
        def decorator(command_func):
            cmd = ICommand(command_func, **cmd_info)
            self.add_command(cmd)
            return cmd

        return decorator

    def add_command(self, command):
        self.__commands[command.name] = command

    def __getitem__(self, command_name):
        return self.commands[command_name]



INSTANCE = ICommandManager()