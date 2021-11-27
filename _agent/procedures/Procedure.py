from _agent.procedures.steps.Step import Step


class Procedure:
    _steps: list

    def when(self, step: Step):
        self._steps = [step]
        return self

    def then(self, step: Step):
        self._steps.append(step)
        return self

    def run(self):
        current_step = None
        result = None
        try:
            for step in self._steps:
                current_step = step
                bf = step.before(result)
                app = step.apply(bf)
                result = step.after(app)
        except Exception as e:
            print(f"stop on step=[{current_step}] with last result=[{result}] and exception=[{e}]")
        return result
