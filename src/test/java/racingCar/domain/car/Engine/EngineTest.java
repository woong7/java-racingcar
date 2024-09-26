package racingCar.domain.car.Engine;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;
import racingCar.domain.car.Engine2.Engine2;

class EngineTest {

    @Test
    public void fixed_엔진_테스트() {
        // given, when
        Engine movableEngine = new FixedEngine(9);
        Engine nonMovableEngine = new FixedEngine(3);

        // then
        assertThat(movableEngine.movable()).isEqualTo(true);
        assertThat(nonMovableEngine.movable()).isEqualTo(false);
    }

    @Test
    public void engine2_테스트() {
        //given, when
        Engine fakeEngine = new Engine() {
            @Override
            public boolean movable() {
                return true;
            }
        };
        Engine2 movingEngine = new Engine2(9);
        Engine2 notMovingEngine = new Engine2(3);

        //then
        assertThat(movingEngine.isMove()).isTrue();
        assertThat(notMovingEngine.isMove()).isFalse();
    }

}