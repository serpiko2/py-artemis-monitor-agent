from _agent.procedures.steps.Step import Step


def _run(step, *params):
    return step.after(*step.apply(*step.before(*params)))


class Procedure:
    _steps: list

    def when(self, step: Step):
        self._steps = [step]
        return self

    def then(self, step: Step):
        self._steps.append(step)
        return self

    def run(self, **params):
        current_step = None
        result = params
        try:
            for step in self._steps:
                current_step = step
                result = _run(step, result)
        except Exception as e:
            print(f"stop on step=[{current_step}] with exception=[{e}]")
