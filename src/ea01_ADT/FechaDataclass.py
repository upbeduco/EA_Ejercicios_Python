from dataclasses import dataclass


@dataclass(order=True)
class Fecha:
    """
    Abstract Data Type representing a date with day, month, and year.

    This class represents a Gregorian calendar date and provides methods for
    validation, date arithmetic, and date calculations.

    Attributes
    ----------
    _dia : int
        Day of the month (1-31, depending on month and leap year)
    _mes : int
        Month of the year (1-12)
    _año : int
        Year (must be positive)

    Raises
    ------
    ValueError
        If the date is invalid (invalid day, month, or year)
    """

    _año: int
    _mes: int
    _dia: int

    def __post_init__(self):
        """Validate the date upon initialization."""
        self._validar_fecha()

    def _validar_fecha(self) -> None:
        """
        Validate the date components.

        Raises
        ------
        ValueError
            If any date component is invalid
        """
        if self._año < 1:
            raise ValueError(f"Año debe ser positivo: {self._año}")

        if not 1 <= self._mes <= 12:
            raise ValueError(f"Mes debe estar entre 1 y 12: {self._mes}")

        dias_en_mes = self._dias_en_mes(self._mes, self._año)
        if not 1 <= self._dia <= dias_en_mes:
            raise ValueError(
                f"Día debe estar entre 1 y {dias_en_mes} para {self._mes}/{self._año}: {self._dia}"
            )

    @staticmethod
    def _es_bisiesto(año: int) -> bool:
        """
        Determine if a year is a leap year.

        Parameters
        ----------
        año : int
            The year to check

        Returns
        -------
        bool
            True if the year is a leap year, False otherwise
        """
        return (año % 4 == 0 and año % 100 != 0) or (año % 400 == 0)

    @staticmethod
    def _dias_en_mes(mes: int, año: int) -> int:
        """
        Get the number of days in a given month.

        Parameters
        ----------
        mes : int
            The month (1-12)
        año : int
            The year

        Returns
        -------
        int
            Number of days in the specified month
        """
        if mes in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        elif mes in [4, 6, 9, 11]:
            return 30
        elif mes == 2:
            return 29 if Fecha._es_bisiesto(año) else 28
        else:
            return 0

    def dia_del_año(self) -> int:
        """
        Calculate the day of the year (1-366).

        Returns
        -------
        int
            The day number within the year (1 = January 1st, 366 = December 31st in leap year)
        """
        dias = 0
        for mes in range(1, self._mes):
            dias += self._dias_en_mes(mes, self._año)
        dias += self._dia
        return dias

    def es_bisiesto(self) -> bool:
        """
        Check if the year of this date is a leap year.

        Returns
        -------
        bool
            True if this year is a leap year, False otherwise
        """
        return self._es_bisiesto(self._año)

    @property
    def dia(self) -> int:
        """Get the day of the month."""
        return self._dia

    @property
    def mes(self) -> int:
        """Get the month."""
        return self._mes

    @property
    def año(self) -> int:
        """Get the year."""
        return self._año

    def __str__(self) -> str:
        """Return a formatted string representation of the date."""
        return f"{self._dia:02d}/{self._mes:02d}/{self._año}"

    def __repr__(self) -> str:
        """Return a detailed string representation of the date."""
        return f"Fecha({self._año}, {self._mes}, {self._dia})"


if __name__ == '__main__':
    # Test 1: Basic creation and string representation
    f1 = Fecha(2022, 5, 20)
    f2 = Fecha(1999, 1, 1)
    f3 = Fecha(1642, 12, 25)
    print(f"Fecha 1: {f1} (repr: {f1!r})")
    print(f"Fecha 2: {f2} (repr: {f2!r})")
    print(f"Fecha 3: {f3} (repr: {f3!r})")
    print()

    # Test 2: Day of year calculation
    print("Pruebas de día del año:")
    assert f1.dia_del_año() == 140, "20/05/2022 debe ser día 140"
    assert Fecha(2022, 1, 1).dia_del_año() == 1, "01/01 debe ser día 1"
    assert Fecha(2022, 12, 31).dia_del_año() == 365, "31/12/2022 debe ser día 365"
    print(f"  {f1} es el día {f1.dia_del_año()} del año")
    print(f"  Fecha(2022, 1, 1) es el día {Fecha(2022, 1, 1).dia_del_año()}")
    print(f"  Fecha(2022, 12, 31) es el día {Fecha(2022, 12, 31).dia_del_año()}")
    print()

    # Test 3: Leap year detection
    print("Pruebas de años bisiestos:")
    assert Fecha(2000, 1, 1).es_bisiesto() is True, "2000 es bisiesto"
    assert Fecha(2004, 1, 1).es_bisiesto() is True, "2004 es bisiesto"
    assert Fecha(2001, 1, 1).es_bisiesto() is False, "2001 no es bisiesto"
    assert Fecha(1900, 1, 1).es_bisiesto() is False, "1900 no es bisiesto"
    print(f"  2000 es bisiesto: {Fecha(2000, 1, 1).es_bisiesto()}")
    print(f"  2004 es bisiesto: {Fecha(2004, 1, 1).es_bisiesto()}")
    print(f"  2001 es bisiesto: {Fecha(2001, 1, 1).es_bisiesto()}")
    print()

    # Test 4: Day of year in leap year
    print("Pruebas en año bisiesto (2020):")
    f_leap = Fecha(2020, 12, 31)
    assert f_leap.dia_del_año() == 366, "31/12/2020 debe ser día 366"
    print(f"  {f_leap} es el día {f_leap.dia_del_año()} del año (bisiesto)")
    print()

    # Test 5: Validation - invalid dates
    print("Pruebas de validación:")
    try:
        Fecha(2022, 13, 1)
        assert False, "Debe rechazar mes 13"
    except ValueError as e:
        print(f"  ✓ Rechazado mes 13: {e}")

    try:
        Fecha(2022, 2, 30)
        assert False, "Debe rechazar 30 de febrero"
    except ValueError as e:
        print(f"  ✓ Rechazado 30/02: {e}")

    try:
        Fecha(2021, 2, 29)
        assert False, "Debe rechazar 29 de febrero en año no bisiesto"
    except ValueError as e:
        print(f"  ✓ Rechazado 29/02/2021 (no bisiesto): {e}")

    try:
        Fecha(0, 1, 1)
        assert False, "Debe rechazar año 0"
    except ValueError as e:
        print(f"  ✓ Rechazado año 0: {e}")

    try:
        Fecha(2022, 1, 0)
        assert False, "Debe rechazar día 0"
    except ValueError as e:
        print(f"  ✓ Rechazado día 0: {e}")

    print()

    # Test 6: Date comparison
    print("Pruebas de comparación:")
    f_old = Fecha(2000, 1, 1)
    f_new = Fecha(2022, 5, 20)
    assert f_old < f_new, "2000/01/01 debe ser menor que 2022/05/20"
    assert f_new > f_old, "2022/05/20 debe ser mayor que 2000/01/01"
    assert Fecha(2022, 5, 20) == Fecha(2022, 5, 20), "Fechas iguales deben ser iguales"
    print(f"  {f_old} < {f_new}: {f_old < f_new}")
    print(f"  {f_new} > {f_old}: {f_new > f_old}")
    print()

    print("✓ Todos los tests pasaron exitosamente")

