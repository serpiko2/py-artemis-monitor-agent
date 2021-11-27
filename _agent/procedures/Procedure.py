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
        result = {}
        try:
            for step in self._steps:
                current_step = step
                print(f"result{result}")
                bf = step.before(**result)
                print(f"before{bf}")
                app = step.apply(**bf)
                print(f"app{app}")
                result = step.after(**app)
                print(f"final_result{result}")
        except Exception as e:
            print(f"stop on step=[{current_step}] with last result=[{result}] and exception=[{e}]")
        return result
