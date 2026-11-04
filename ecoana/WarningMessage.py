import warnings

def warn_parallel(capacity, equipment, upper, eqnum, Cb, unit="", model=""):
    if eqnum >= 2:
        warnings.warn(
            f"The capacity {capacity:,.1f} {unit} exceeds the upper limit of the "
            f"{model} model, {equipment} capacity: ({upper:,.0f} {unit}). "
            f"The equipment is represented as {eqnum} identical parallel units. "
            f"Cb = ${Cb:,.0f} (= {eqnum} x ${Cb/eqnum:,.0f})",
            UserWarning,
            stacklevel=3,
        )

def _u(unit):
    return unit if unit else "(correlation unit)"

def _label(model, equipment, eqptype):
    return f"{model} model, {equipment}" + (f" ({eqptype})" if eqptype else "")

def warn_below(capacity, lower, equipment="", eqptype=None, model="", unit="", extrapolated=False):
    # Size below the lower limit of the correlation: evaluated at the lower limit (default) or extrapolated.
    action = "the correlation was extrapolated" if extrapolated else "the cost was evaluated at the lower limit"
    warnings.warn(
        f"The capacity {capacity:,.4g} {_u(unit)} is below the lower limit of the {_label(model, equipment, eqptype)} "
        f"correlation ({lower:,.4g} {_u(unit)}); {action}.",
        UserWarning,
        stacklevel=5,
    )

def warn_above(capacity, upper, equipment="", eqptype=None, model="", unit="", eqnum=1):
    # Size above the upper limit of the correlation: identical parallel units (eqnum >= 2) or extrapolated.
    if eqnum >= 2:
        action = (f"the equipment is represented as {eqnum} identical parallel units of "
                  f"{capacity/eqnum:,.4g} {_u(unit)} each")
    else:
        action = "the correlation was extrapolated"
    warnings.warn(
        f"The capacity {capacity:,.4g} {_u(unit)} exceeds the upper limit of the {_label(model, equipment, eqptype)} "
        f"correlation ({upper:,.4g} {_u(unit)}); {action}.",
        UserWarning,
        stacklevel=5,
    )

def warn_LowPressure(pressure, lowerP, equipment="", model=""):
    warnings.warn(
        f"The pressure {pressure:,.1f} bar is below the lower limit of the {model} model, {equipment} "
        f"({lowerP:,.1f} bar); the pressure factor was evaluated at the lower limit.",
        UserWarning,
        stacklevel=3,
    )
        