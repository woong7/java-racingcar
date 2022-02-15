package racingcar.util;

import racingcar.validator.CarNameValidator;

public class CarNameParser {
    public static void parseCarNameInputs(String inputs) {
        CarNameValidator carNameValidator = new CarNameValidator();
        inputs = inputs.replaceAll(" ", "");
        String[] carNames = inputs.split(",");
        for (String carName : carNames) {
            carNameValidator.validateCarName(carName);
        }
    }
}
