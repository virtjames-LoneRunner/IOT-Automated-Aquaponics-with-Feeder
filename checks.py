def check_if_pump_needs_on(settings_data, new_data):
    min_temp = settings_data[1]
    max_temp = settings_data[2]
    min_water_level = settings_data[3]
    max_water_level = settings_data[4]
    pH_level = settings_data[5]
    DO_level = settings_data[6]

    temperature = new_data[0]
    new_pH_level = new_data[1]
    new_water_level = new_data[2]
    new_DO_level = new_data[4]

    return_status = False

    if min_temp < temperature < max_temp:
        return_status = False
    else:
        return_status = True

    if min_water_level < new_water_level < max_water_level:
        return_status = False
    else:
        return_status = True

    if (pH_level - 1) < new_pH_level < (pH_level + 1):
        return_status = False
    else:
        return_status = True

    # uncomment the following line if DO is attached

    # if (DO_level - 1) < new_DO_level < (DO_level + 1):
    #     return_status = False
    # else:
    #     return_status = True

    return return_status


def check_if_sols_needs_on(settings_data, new_data):
    min_temp = settings_data[1]
    max_temp = settings_data[2]
    min_water_level = settings_data[3]
    max_water_level = settings_data[4]
    pH_level = settings_data[5]
    DO_level = settings_data[6]

    temperature = new_data[0]
    new_pH_level = new_data[1]
    new_water_level = new_data[2]
    new_DO_level = new_data[4]

    sol_in = False
    sol_out = False

    if temperature < min_temp:
        sol_in = True
        sol_out = True
    else:
        sol_in = False
        sol_out = False

    if new_water_level < min_water_level:
        sol_in = True
        sol_out = False
    elif new_water_level > max_water_level:
        sol_in = False
        sol_out = True
    else:
        sol_in = False
        sol_out = False

    if (pH_level - 1) < new_pH_level < (pH_level + 1):
        sol_in = False
        sol_out = False
    else:
        sol_in = True
        sol_out = True

    # uncomment the following line if DO is attached

    # if (DO_level - 1) < new_DO_level < (DO_level + 1):
    #     sol_in = False
    #     sol_out = False
    # else:
    #     sol_in = True
    #     sol_out = True

    return sol_in, sol_out
