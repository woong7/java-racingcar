package study;

import org.assertj.core.internal.Strings;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.ValueSource;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.HashSet;
import java.util.Set;

public class SetTest {
    private Set<Integer> numbers;

    @BeforeEach
    void setUp() {
        numbers = new HashSet<>();
        numbers.add(1);
        numbers.add(1);
        numbers.add(2);
        numbers.add(3);
    }

    // Test Case 구현
    @Test
    @DisplayName("요구사항 1")
    void size() {
        assertThat(numbers.size()).isEqualTo(3);
    }


    @DisplayName("요구사항 2")
    @ParameterizedTest
    @ValueSource(ints = {1, 2, 3})
    void isContain_ShouldReturnTrueForNumberInNumbers(int input) {
        assertTrue(numbers.contains(input));
    }

    @DisplayName("요구사항 3")
    @ParameterizedTest
    @CsvSource(value = {"1:true", "2:true", "3:true", "4:false", "5:false"}, delimiter = ':')
    void isSmallerThanFour(int input, boolean expected) {
        //assertEquals(expected, input < 4);
        assertThat(numbers.contains(input)).isEqualTo(expected);
    }
}
