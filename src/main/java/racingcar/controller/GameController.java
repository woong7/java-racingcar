package racingcar.controller;

import racingcar.builder.CarBuilder;
import racingcar.repository.CarRepository;
import racingcar.domain.Car;
import racingcar.util.CarNameParser;
import racingcar.view.*;

import java.util.*;
import java.util.concurrent.ThreadLocalRandom;
import java.util.stream.Collectors;

public class GameController {
    private static final String NOT_FOUND_CARS_MESSAGE = "[ERROR] 자동차를 찾을 수 없습니다.";

    private static final int RANDOM_RANGE = 10;
    private static final int PIVOT_NUMBER = 4;

    private InputView inputView;
    private OutputView outputView;
    private CarRepository carRepository;
    private int roundNumber;

    public GameController(InputView inputView, OutputView outputView, CarRepository carRepository) {
        this.inputView = inputView;
        this.outputView = outputView;
        this.carRepository = carRepository;
    }

    public GameController(CarRepository carRepository) {
        this.carRepository = carRepository;
    }

    public void play() {
        setGame();
        playGame();
        inputView.terminate();
        outputView.showGameResult(getWinners());
    }

    private void setGame() {
        setCars();
        setRoundNumbers();
    }

    private void setCars() {
        outputView.printAskCarNameInputMessage();

        String input = inputView.readCarNamesInput();
        String[] strings = CarNameParser.parseCarNameInputs(input);
        List<String> carNames = Arrays.asList(strings);

        List<Car> cars = new ArrayList<>();
        CarBuilder carBuilder = new CarBuilder();
        carNames.forEach(x -> {
            Car car = carBuilder.setCarName(x).build();
            cars.add(car);
        });

        carRepository.addCars(cars);
    }


    private void setRoundNumbers() {
        outputView.printAskRoundNumberMessage();
        roundNumber = inputView.readRoundNumberInput();
    }

    private void playGame() {
        outputView.printExecutionResultMessage();
        for (int i = 0; i < roundNumber; i++) {
            playRound();
        }
    }

    private void playRound() {
        moveCars();
        List<Car> cars = carRepository.findAll();
        outputView.showCurrentStatus(cars);
    }

    private void moveCars() {
        for (Car car : carRepository.findAll()) {
            car.moveOrHold(isMove());
        }
    }

    private boolean isMove() {
        return ThreadLocalRandom.current().nextInt(RANDOM_RANGE) < PIVOT_NUMBER;
    }

    public List<Car> getWinners() {
        List<Car> cars = carRepository.findAll();

        Car maxCar = cars.stream()
                .max(Car::compareTo)
                .stream()
                .findAny()
                .orElseThrow(() -> new RuntimeException(NOT_FOUND_CARS_MESSAGE));

        List<Car> winners = cars.stream()
                .filter(car -> car.isSamePosition(maxCar))
                .collect(Collectors.toList());

        return winners;
    }
}
