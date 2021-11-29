from async import Job


class __JobStub(Job):

    @staticmethod
    def execute(loop: bool, callback: callable, fallback: callable, params):
        """ Unimplemented job stub - use this as a reference structure
            :param:
                `loop`:`true or false to make it loop`
                `callback`:`the callback to be executed to handle the non blocking function response`
                `fallback`:`the fallback to be executed to handle the non blocking function error`
                `params`:`an object that holds the parameters for the function to run`
        """
        print(f"running an unimplemented job stub entrypoint: {loop, callback, fallback, params}")
        # we should do something awesome and non-blocking here!
        # return false to not loop
        return loop

    def __init__(self,
                 params,
                 delay: int = 0,
                 loop=False):
        super().__init__(delay, loop, params)
        self.success = None
        self.failed = None

    def callback(self, reply):
        print(f"{reply}")
        self.success = True
        pass

    def fallback(self, error):
        print(f"{error}")
        self.failed = True
        pass