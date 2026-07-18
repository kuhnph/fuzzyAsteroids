"""
Generic fuzzy controller.

This file should stay reusable across:
- vehicle control
- pseudo-target control
- asteroid navigation
- future GA-tuned controllers
"""


class FuzzyController:
    def __init__(self, input_variables, output_variables, rules, defuzzifier):
        """
        Parameters
        ----------
        input_variables : list[FuzzyVariable]
            Fuzzy input variables.

        output_variables : list[FuzzyVariable]
            Fuzzy output variables.

        rules : list[FuzzyRule]
            Fuzzy rule base.

        defuzzifier : function
            Function used to convert fuzzy output activations
            into crisp values.
        """
        self.input_variables = {
            variable.name: variable
            for variable in input_variables
        }

        self.output_variables = {
            variable.name: variable
            for variable in output_variables
        }

        self.rules = rules
        self.defuzzifier = defuzzifier

    def evaluate(self, crisp_inputs):
        """
        Run fuzzy inference.

        Parameters
        ----------
        crisp_inputs : dict
            Example:
            {
                "heading_error": -25.0,
                "distance_error": 400.0,
                "speed": 1.2,
            }

        Returns
        -------
        dict
            Example:
            {
                "desired_speed": 1.8,
                "desired_turn_rate": -120.0,
            }
        """

        fuzzified_inputs = self._fuzzify_inputs(crisp_inputs)
        output_activations = self._initialize_output_activations()

        for rule in self.rules:
            firing_strength = rule.evaluate(fuzzified_inputs)

            for output_name, output_set_name in rule.consequents:
                current_strength = output_activations[output_name][output_set_name]

                output_activations[output_name][output_set_name] = max(
                    current_strength,
                    firing_strength,
                )

        crisp_outputs = {}

        for output_name, activations in output_activations.items():
            output_variable = self.output_variables[output_name]

            crisp_outputs[output_name] = self.defuzzifier(
                output_variable,
                activations,
            )

        return crisp_outputs

    def _fuzzify_inputs(self, crisp_inputs):
        fuzzified_inputs = {}

        for variable_name, variable in self.input_variables.items():
            if variable_name not in crisp_inputs:
                raise KeyError(
                    f"Missing crisp input '{variable_name}' "
                    f"for fuzzy controller."
                )

            crisp_value = crisp_inputs[variable_name]
            fuzzified_inputs[variable_name] = variable.fuzzify(crisp_value)

        return fuzzified_inputs

    def _initialize_output_activations(self):
        output_activations = {}

        for variable_name, variable in self.output_variables.items():
            output_activations[variable_name] = {}

            for set_name in variable.sets:
                output_activations[variable_name][set_name] = 0.0

        return output_activations