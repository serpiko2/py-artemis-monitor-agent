from _agent.procedures.steps.Step import Step
import functools

class Procedure:
    _steps: list

    def when(self, step: Step):
        self._steps = [step]
        return self

    def then(self, step: Step):
        self._steps.append(step)
        return self

    def run(self, *params):
        current_step = None
        result = None
        try:
            for step in self._steps:
                result = step.after(*step.apply(*step.before(*params)))
        except Exception as e:
            print(f"stop on step=[{current_step}] with last result=[{result}] and exception=[{e}]")
        return result


def exec(fun, **params):
    return fun(params)
